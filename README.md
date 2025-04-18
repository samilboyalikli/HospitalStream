# HOSPITAL SIMULATION  
A Simple Simulation of Live Data Streaming for 13 Hospitals  

## Overview  
This project simulates a small portion of hospitals’ live data streams. Orchestrated with Docker Compose, the system uses Apache Spark’s batch engine to generate fake data. It then feeds that data into a Kafka topic to create a streaming pipeline and analyzes it in two layers: the first layer with Apache Kafka, and the second layer with Spark’s Structured Streaming.  

## Project Goals  
While working with Apache Spark, I struggled to find live data streams where I could pull data without worrying about internet stability, security or unpredictable complexity. As a result, I began generating fake data using Spark’s batch modules. I programmed those batches into a continuous stream and wrote live analytics on top using Spark’s Structured Streaming.

The primary goal of this project is to simulate a live data stream with minimal risk and complexity. The secondary goals are:
1. To build a variety of live analytics—from the simplest to the most complex—on that stream.  
2. To gain a hands‑on understanding of Apache Kafka and Apache Spark.  
3. To deepen my knowledge of Docker orchestration via Docker Compose.  

## Use Cases  
This project is useful if you want to:  
1. Create a real‑time data stream.  
2. Experiment with analytics on a real‑time stream.  
3. Understand how Docker Compose orchestrates multi‑container applications.  
4. Generate fake data using Apache Spark.  
5. Write analytics on a live Kafka stream.  

## Project Architecture  
![Main Schema of Project.](/assets/main_schema.jpeg "Main Schema of Project.")  

### Producer  
In this component, we generate fake patient records and send them to a live stream called **Raw Stream**. Data generation is implemented with Apache Spark in the `hospitals` directory of the source code.  

**Producer Files:**  
```  
hospitals  
├─ atlanta.py  
├─ boston.py  
├─ chicago.py  
├─ dallas.py  
├─ detroit.py  
├─ Dockerfile  
├─ gender_name.csv  
├─ houston.py  
├─ jersey.py  
├─ last_name.csv  
├─ miami.py  
├─ newyork.py  
├─ phoenix.py  
├─ requirements.txt  
├─ sanfrancisco.py  
├─ seattle.py  
└─ washington.py  
```  

### Raw Stream  
![Raw Stream Topic.](/assets/raw_stream.png "Raw Stream Topic.")  

The generated records are written to a Kafka topic named **raw_stream**. This keeps the raw data intact and readily available for alternative processing or coding experiments.  

### Analyzer  
This part of the project has three main tasks:  
1. The **distributor** reads from **raw_stream** and routes each record, based on age, into one of three topics: **children**, **adult**, or **senior**.  
2. The **topics** modules consume from those three age‑based topics, perform analysis on the records, and apply flags.  
3. The flagged records are then written to the **analyzed_stream** topic.  

**Analyzer Files:**  
```
distributor  
├─ distributor.py  
├─ Dockerfile  
└─ requirements.txt  

topics  
├─ adult  
│   ├─ Dockerfile  
│   ├─ entrypoint.sh  
│   └─ main.py  
├─ children  
│   ├─ Dockerfile  
│   ├─ entrypoint.sh  
│   └─ main.py  
└─ senior  
    ├─ Dockerfile  
    ├─ entrypoint.sh  
    └─ main.py  
```  

### Analyzed Stream  
![Analyzed Stream Topic.](/assets/analyzed_stream.png "Analyzed Stream Topic.")  

Flagged (analyzed) records are written to a Kafka topic named **analyzed_stream**. At this stage, the data is processed and annotated, ready for consumption. To improve readability, a separate consumer application is provided.  

### Consumer  
![Output of Consumer.](/assets/consumer_output.png "Output of Consumer.")  

The **consumer** directory contains code that reads from **analyzed_stream** and presents the records in the terminal with simple visual cues. Flags added by the analytics modules determine the coloring of each entry, providing an at‑a‑glance view of processed data.  

**Consumer Files:**  
```  
consumer  
├─ Dockerfile  
├─ main.py  
└─ requirements.txt  
```  

## Kafka Topics  
![Topic Schema of Project.](/assets/topic_schema.jpeg "Topic Schema of Project.")  

This project uses five Kafka topics:  
- **raw_stream**: holds unprocessed (raw) records.  
- **children**: contains records for patients under 18.  
- **adult**: contains records for patients aged 18–65.  
- **senior**: contains records for patients over 65.  
- **analyzed_stream**: contains processed and flagged results from **raw_stream**.  

## Anatomy of Fake Records  
Each record represents a patient’s blood test and is structured as a dictionary. It begins with eight keys/values and expands with additional flags during analysis. Below are the fields for raw and analyzed streams.

#### Raw Stream Record  
```py
{
  "Name": "patient_first_name",
  "Surname": "patient_last_name",
  "Age": patient_age,
  "cbc": "age_group",
  "bloodValues": { blood_values },
  "Hospital": "hospital_name",
  "Gender": "patient_gender",
  "Time": timestamp_generated_by_producer
}
```
- **Name**: Patient’s first name (string)  
- **Surname**: Patient’s last name (string)  
- **Age**: Patient’s age (integer)  
- **cbc**: Patient’s age bracket (string) – for convenience during development  
- **bloodValues**: A nested dictionary of blood test values (dictionary)  
- **Hospital**: Name of the hospital where the test was performed (string)  
- **Gender**: Patient’s gender (string)  
- **Time**: Timestamp when the fake record was generated (timestamp)  

##### Blood Values Dictionary  
```py
{
  "WBC": white_blood_cell_count,
  "RBC": red_blood_cell_count,
  "Hb": hemoglobin,
  "Hct": hematocrit_percent,
  "MCV": mean_corpuscular_volume,
  "MCH": mean_corpuscular_hemoglobin,
  "MCHC": mean_corpuscular_hemoglobin_concentration
}
```
- **WBC** (white blood cells, leukocytes)  
- **RBC** (red blood cells, erythrocytes)  
- **Hb** (hemoglobin)  
- **Hct** (hematocrit %)  
- **MCV** (mean corpuscular volume)  
- **MCH** (mean corpuscular hemoglobin)  
- **MCHC** (mean corpuscular hemoglobin concentration)  

*(Each metric has its own normal ranges by age/gender, used later for flagging.)*  

#### Analyzed Stream Record  
```py
{
  "Name": "patient_first_name",
  "Surname": "patient_last_name",
  "Age": patient_age,
  "bloodValues": { blood_values },
  "Hospital": "hospital_name",
  "Gender": "patient_gender",
  "Time": timestamp_generated_by_producer,
  "status(WBC)":  wbc_flag,
  "status(RBC)":  rbc_flag,
  "status(Hb)":   hb_flag,
  "status(Hct)":  hct_flag,
  "status(MCV)":  mcv_flag,
  "status(MCH)":  mch_flag,
  "status(MCHC)": mchc_flag
}
```
- **`Status(WBC)`** indicates the result of the WBC analysis. For children aged 0–2 years, the ideal range is 6,000–17,500; for children aged 2–12 years, 5,000–15,000; and for those aged 12–18 years, 4,500–13,500. In adults (regardless of gender), the range is 4,000–11,000, and for individuals over 65 it remains the same, 4,000–11,000. If the WBC value falls within the ideal range, the `Status(WBC)` flag is set to `True`; otherwise it is `False` (boolean).

- **`Status(RBC)`** indicates the result of the RBC analysis. For children aged 0–2 years, the ideal range is 3,900,000–5,500,000; for children aged 2–12 years, 4,000,000–5,200,000; and for those aged 12–18 years, 4,100,000–5,600,000. In adults, the ideal range is 4,700,000–6,100,000 for males and 4,200,000–5,400,000 for females. For females over 65, it is 4,100,000–5,100,000, and for males over 65, 4,500,000–5,900,000. If the RBC value falls within the ideal range, the `Status(RBC)` flag is set to `True`; otherwise it is `False` (boolean).

- **`Status(Hb)`** indicates the result of the Hb analysis. For children aged 0–2 years, the ideal range is 10.0–14.0 g/dL; for ages 2–12, 11.5–15.5 g/dL; and for those aged 12–18, it varies by sex—12.0–15.0 g/dL for girls and 13.0–16.0 g/dL for boys. In adult males (18–65), the ideal range is 13.5–17.5 g/dL, while in adult females it is 12.0–15.5 g/dL. For seniors, the ideal range is 12.0–15.0 g/dL for women and 13.0–17.0 g/dL for men. If the Hb value falls within the ideal range, the `Status(Hb)` flag is set to `True`; otherwise it is `False` (boolean).

- **`Status(Hm)`** indicates the result of the Hm (hematocrit) analysis. For children aged 0–2 years, the ideal range is 33–43 %; for ages 2–12, 34–42 %; and for those aged 12–18, it varies by sex—36–45 % for girls and 40–50 % for boys. In adult males (18–65), the ideal range is 41–50 %, while in adult females it is 36–44 %. For seniors, the ideal range is 36–46 % for women and 39–50 % for men. If the Hm value falls within the ideal range, the `Status(Hm)` flag is set to `True`; otherwise it is `False` (boolean).

- **`Status(MCV)`** indicates the result of the MCV analysis. For children aged 0–2 years, the ideal range is 70–86 fL; for ages 2–12, 75–87 fL; and for those aged 12–18, 80–96 fL. In adults and seniors (both genders, > 18), the ideal range is 80–100 fL. If the MCV value falls within the ideal range, the `Status(MCV)` flag is set to `True`; otherwise it is `False` (boolean).

- **`Status(MCH)`** indicates the result of the MCH analysis. For children aged 0–2 years, the ideal range is 24–30 pg; for ages 2–12, 26–32 pg; and for those aged 12–18, 28–34 pg. In adults and seniors (both genders, > 18), the ideal range is 27–33 pg. If the MCH value falls within the ideal range, the `Status(MCH)` flag is set to `True`; otherwise it is `False` (boolean).

- **`Status(MCHC)`** indicates the result of the MCHC analysis. For children aged 0–2 years, the ideal range is 30–36 %; for ages 2–18, 32–36 %; and in adults and seniors (both genders, > 18), the ideal range remains 32–36 %. If the MCHC value falls within the ideal range, the `Status(MCHC)` flag is set to `True`; otherwise it is `False` (boolean).