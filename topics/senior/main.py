from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, struct, to_json, when, regexp_replace
from pyspark.sql.types import StructField, StructType, StringType, TimestampType, IntegerType, FloatType

spark = SparkSession.builder.appName("KafkaSparkStreaming").config("spark.sql.session.timeZone", "UTC").getOrCreate()

kafka_df = spark.readStream.format("kafka") \
            .option("kafka.bootstrap.servers", "kafka:9092") \
            .option("subscribe", "senior") \
            .option("startingOffsets", "earliest") \
            .load()

json_schema = StructType([
    StructField("Name", StringType(), True),
    StructField("Surname", StringType(), True),
    StructField("Age", IntegerType(), True),
    StructField("bloodValues", StructType([
        StructField("WBC", IntegerType(), True),
        StructField("RBC", IntegerType(), True),
        StructField("Hb", FloatType(), True),
        StructField("Hct", StringType(), True),
        StructField("MCV", IntegerType(), True),
        StructField("MCH", IntegerType(), True),
        StructField("MCHC", StringType(), True)])),
    StructField("Hospital", StringType(), True),
    StructField("Gender", StringType(), True),
    StructField("Time", TimestampType(), True)
])


def values_tied_on_gender(df,value_name,min_for_male,max_for_male,min_for_female,max_for_female):
    df = df.withColumn(f"status({value_name})"
        ,when((df.Gender=="MALE")&(df.bloodValues[value_name]>=min_for_male)&(df.bloodValues[value_name]<=max_for_male),True)
        .otherwise(
            when((df.Gender=="FEMALE")&(df.bloodValues[value_name]>=min_for_female)&(df.bloodValues[value_name]<=max_for_female),True)
            .otherwise(False)
        ))
    return df


def gender_neutral_values(df,value_name,min,max):
    df = df.withColumn(f"status({value_name})",when((
        df.bloodValues[value_name]>=min)&(df.bloodValues[value_name]<=max),True).otherwise(False))
    return df


def blood_values_analysis(cbc):
    cbc = gender_neutral_values(df=cbc,value_name="WBC",min=4000,max=11000)
    cbc = values_tied_on_gender(df=cbc,value_name="RBC",min_for_male=4500000,max_for_male=5900000,min_for_female=4100000,max_for_female=5100000)
    cbc = values_tied_on_gender(df=cbc,value_name="Hb",min_for_male=13.0,max_for_male=17.0,min_for_female=12.0,max_for_female=15.0)
    cbc = cbc.withColumn(f"status(Hct)"
        ,when((cbc.Gender=="MALE")&
            (regexp_replace(cbc.bloodValues["Hct"],"%","").cast(IntegerType())>=39)&
            (regexp_replace(cbc.bloodValues["Hct"],"%","").cast(IntegerType())<=50),True)
        .otherwise(
            when((cbc.Gender=="FEMALE")&
                (regexp_replace(cbc.bloodValues["Hct"],"%","").cast(IntegerType())>=36)&
                (regexp_replace(cbc.bloodValues["Hct"],"%","").cast(IntegerType())<=46),True)
            .otherwise(False)))
    cbc = gender_neutral_values(df=cbc,value_name="MCV",min=80,max=100)
    cbc = gender_neutral_values(df=cbc,value_name="MCH",min=27,max=33)
    cbc = cbc.withColumn(f"status(MCHC)",
                        when((regexp_replace(cbc.bloodValues["MCHC"],"%","").cast(IntegerType())>=32)&
                            (regexp_replace(cbc.bloodValues["MCHC"],"%","").cast(IntegerType())>=36),True).otherwise(False))
    return cbc


parsed_df = kafka_df.selectExpr("CAST(value AS STRING)").select(from_json(col("value"), json_schema).alias("data")).select("data.*")
cbc = blood_values_analysis(parsed_df)
cbc = cbc.withWatermark("Time", "1 minutes")

query = cbc.select(to_json(struct("*")).alias("value")).writeStream.format("kafka") \
                    .option("kafka.bootstrap.servers","kafka:9092") \
                    .option("topic","analyzed_stream") \
                    .option("checkpointLocation","/tmp/spark-checkpoints") \
                    .outputMode("append") \
                    .trigger(processingTime="30 seconds") \
                    .start()

query.awaitTermination()
