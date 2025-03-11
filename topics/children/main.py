from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, struct, to_json, when
from pyspark.sql.types import StructField, StructType, StringType, TimestampType, IntegerType, FloatType

spark = SparkSession.builder.appName("KafkaSparkStreaming").config("spark.sql.session.timeZone", "UTC").getOrCreate()

kafka_df = spark.readStream.format("kafka") \
            .option("kafka.bootstrap.servers", "kafka:9092") \
            .option("subscribe", "children") \
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
    cbc = cbc.withColumn("status(WBC)"
                        ,when((cbc.Age<=2)&(cbc.bloodValues["WBC"]>=6000)&(cbc.bloodValues["WBC"]<=17500),True)
                        .when((cbc.Age>2)&(cbc.Age<=12)&(cbc.bloodValues["WBC"]>=5000)&(cbc.bloodValues["WBC"]<=15000), True)
                        .when((cbc.Age>12)&(cbc.Age<18)&(cbc.bloodValues["WBC"]>=4500)&(cbc.bloodValues["WBC"]<=13500), True)
                        .otherwise(False))
    cbc = cbc.withColumn("status(RBC)"
                        ,when((cbc.Age<=2)&(cbc.bloodValues["RBC"]>=3900000)&(cbc.bloodValues["RBC"]<=5500000),True)
                        .when((cbc.Age>2)&(cbc.Age<=12)&(cbc.bloodValues["RBC"]>=4000000)&(cbc.bloodValues["RBC"]<=5200000), True)
                        .when((cbc.Age>12)&(cbc.Age<18)&(cbc.bloodValues["RBC"]>=4100000)&(cbc.bloodValues["RBC"]<=5600000), True)
                        .otherwise(False))
    cbc = cbc.withColumn("status(Hb)"
                        ,when((cbc.Age<=2)&(cbc.bloodValues["Hb"]>=10.0)&(cbc.bloodValues["Hb"]<=14.0), True)
                        .when((cbc.Age>2)&(cbc.Age<=12)&(cbc.bloodValues["Hb"]>=11.5)&(cbc.bloodValues["Hb"]<=15.5), True)
                        .when((cbc.Age>12)&(cbc.Age<18)&(cbc.Gender=="MALE")&(cbc.bloodValues["Hb"]>=13.0)&(cbc.bloodValues["Hb"]<=16.0), True)
                        .when((cbc.Age>12)&(cbc.Age<18)&(cbc.Gender=="FEMALE")&(cbc.bloodValues["Hb"]>=12.0)&(cbc.bloodValues["Hb"]<=15.0), True)
                        .otherwise(False))
    cbc = cbc.withColumn("status(Hct)"
                        ,when((cbc.Age<=2)&(cbc.bloodValues["Hct"]>=33)&(cbc.bloodValues["Hct"]<=43), True)
                        .when((cbc.Age>2)&(cbc.Age<=12)&(cbc.bloodValues["Hct"]>=34)&(cbc.bloodValues["Hct"]<=42), True)
                        .when((cbc.Age>12)&(cbc.Age<18)&(cbc.Gender=="MALE")&(cbc.bloodValues["Hct"]>=40)&(cbc.bloodValues["Hct"]<=50), True)
                        .when((cbc.Age>12)&(cbc.Age<18)&(cbc.Gender=="FEMALE")&(cbc.bloodValues["Hct"]>=36)&(cbc.bloodValues["Hct"]<=45), True)
                        .otherwise(False))
    cbc = cbc.withColumn("status(MCV)"
                        ,when((cbc.Age<=2)&(cbc.bloodValues["MCV"]>=70)&(cbc.bloodValues["MCV"]<=86),True)
                        .when((cbc.Age>2)&(cbc.Age<=12)&(cbc.bloodValues["MCV"]>=75)&(cbc.bloodValues["MCV"]<=87), True)
                        .when((cbc.Age>12)&(cbc.Age<18)&(cbc.bloodValues["MCV"]>=80)&(cbc.bloodValues["MCV"]<=96), True)
                        .otherwise(False))
    cbc = cbc.withColumn("status(MCH)"
                        ,when((cbc.Age<=2)&(cbc.bloodValues["MCH"]>=24)&(cbc.bloodValues["MCH"]<=30),True)
                        .when((cbc.Age>2)&(cbc.Age<=12)&(cbc.bloodValues["MCH"]>=26)&(cbc.bloodValues["MCH"]<=32), True)
                        .when((cbc.Age>12)&(cbc.Age<18)&(cbc.bloodValues["MCH"]>=28)&(cbc.bloodValues["MCH"]<=34), True)
                        .otherwise(False))
    cbc = cbc.withColumn("status(MCHC)"
                        ,when((cbc.Age<=2)&(cbc.bloodValues["MCHC"]>=30)&(cbc.bloodValues["MCHC"]<=36),True)
                        .when((cbc.Age>2)&(cbc.Age<18)&(cbc.bloodValues["MCHC"]>=32)&(cbc.bloodValues["MCHC"]<=36), True)
                        .otherwise(False))
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
