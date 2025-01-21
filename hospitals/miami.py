from kafka import KafkaProducer
import random
import pandas
import time
import json
import sys


def select_random_from_csv(file_path, row_count):
    row = random.randint(0, row_count)
    return pandas.read_csv(file_path, header=None, skiprows=row, nrows=1)


def age():
    age_ranges = ["child","adult","senior"]
    age_weights = [1,10,15]
    random_age_ranges = random.choices(age_ranges, weights=age_weights, k=1)
    if random_age_ranges[0] == "child":
        age = random.randint(0,18)
    elif random_age_ranges[0] == "adult":
        age = random.randint(18,65)
    else:
        age = random.randint(65,80)
    return age


def wbc_for_children(age):
    if age >= 0 and age <= 2:
        return random.randint(4000,19000)
    elif age >= 2 and age <= 12:
        return random.randint(3000,17000)
    else: 
        return random.randint(3000,15000)


def rbc_for_children(age):
    if age >= 0 and age <= 2:
        return random.randint(3500000,6500000)
    elif age >= 2 and age <= 12:
        return random.randint(3800000,5500000)
    else: 
        return random.randint(3800000,6000000)


def hb_for_children(age,gender):
    if age >= 0 and age <= 2:
        return round(random.uniform(9.0,15.0),1)
    elif age >= 2 and age <= 12:
        return round(random.uniform(10.0,16.0),1)
    else: 
        if gender == "MALE":
            return round(random.uniform(12.0,17.0),1)
        else:
            return round(random.uniform(11.0,16.0),1)    


def hm_for_children(age,gender):
    if age >= 0 and age <= 2:
        return random.randint(30,45)
    elif age >= 2 and age <= 12:
        return random.randint(30,45)
    else: 
        if gender == "MALE":
            return random.randint(35,55)
        else:
            return random.randint(32,47)    


def platelet_for_children(age):
    if age >= 0 and age <= 2:
        return random.randint(125000,475000)
    elif age >= 2 and age <= 12:
        return random.randint(125000,475000)
    else: 
        return random.randint(125000,475000)


def mcv_for_children(age):
    if age >= 0 and age <= 2:
        return random.randint(65,90)
    elif age >= 2 and age <= 12:
        return random.randint(70,95)
    else: 
        return random.randint(75,100)


def mch_for_children(age):
    if age >= 0 and age <= 2:
        return random.randint(20,35)
    elif age >= 2 and age <= 12:
        return random.randint(20,37)
    else: 
        return random.randint(20,40)


def mchc_for_children(age):
    if age >= 0 and age <= 2:
        return random.randint(25,40)
    elif age >= 2 and age <= 12:
        return random.randint(30,40)
    else: 
        return random.randint(30,40)


def wbc_for_adult():
    return random.randint(3000,12000)


def rbc_for_adult(gender):
    if gender == "MALE":
        return random.randint(4500000,6500000)
    else: return random.randint(3700000,5700000)


def hb_for_adult(gender):
    if gender == "MALE":
        return round(random.uniform(12.0,19.0),1)
    else: return round(random.uniform(10.0,17.0),1)


def hm_for_adult(gender):
    if gender == "MALE":
        return random.randint(35,55)
    else: return random.randint(30,50)


def mcv_for_adult():
    return random.randint(70,120)


def mch_for_adult():
    return random.randint(20,40)


def mchc_for_adult():
    return random.randint(25,40)


def wbc_for_senior():
    return random.randint(3000,12000)


def rbc_for_senior(gender):
    if gender == "MALE":
        return random.randint(4000000,7000000)
    else: return random.randint(3500000,6000000)


def hb_for_senior(gender):
    if gender == "MALE":
        return round(random.uniform(11.0,19.0),1)
    else: return round(random.uniform(10.0,17.0),1)


def hm_for_senior(gender):
    if gender == "MALE":
        return random.randint(30,60)
    else: return random.randint(25,55)


def mcv_for_senior():
    return random.randint(70,110)


def mch_for_senior():
    return random.randint(20,40)


def mchc_for_senior():
    return random.randint(25,45)


def cbc(age):
    if age >= 0 and age <= 18:
        return "child"
    elif age >= 18 and age <= 65:
        return "adult"
    else: return "senior"


def children_values(age, gender):
    return {
        "WBC":wbc_for_children(age),
        "RBC":rbc_for_children(age),
        "Hb":hb_for_children(age,gender=gender),
        "Hct":f"{hm_for_children(age,gender=gender)}%",
        "MCV":mcv_for_children(age),
        "MCH":mch_for_children(age),
        "MCHC":f"{mchc_for_children(age)}%"
    }


def adult_values(gender):
    return {
        "WBC":wbc_for_adult(),
        "RBC":rbc_for_adult(gender=gender),
        "Hb":hb_for_adult(gender=gender),
        "Hct":f"{hm_for_adult(gender=gender)}%",
        "MCV":mcv_for_adult(),
        "MCH":mch_for_adult(),
        "MCHC":f"{mchc_for_adult()}%"
    }


def senior_values(gender):
    return {
        "WBC":wbc_for_senior(),
        "RBC":rbc_for_senior(gender=gender),
        "Hb":hb_for_senior(gender=gender),
        "Hct":f"{hm_for_senior(gender=gender)}%",
        "MCV":mcv_for_senior(),
        "MCH":mch_for_senior(),
        "MCHC":f"{mchc_for_senior()}%"
    }


def blood_values(age_range,age,gender):
    if age_range == "child":
        return children_values(age, gender=gender)
    elif age_range == "adult":
        return adult_values(gender=gender)
    else: return senior_values(gender=gender)


def readable_time(timestamp):
    local_time = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", local_time)


def case_production():
    age_of_patience = age()
    gender_of_patience = select_random_from_csv("gender_name.csv", 13962).iloc[0, 0].upper()
    age_range = cbc(age_of_patience)
    blood_values_of_patience = blood_values(age_range=age_range, age=age_of_patience, gender=gender_of_patience)
    return {
        "Name":select_random_from_csv("gender_name.csv", 13962).iloc[0, 1].upper(),
        "Surname":select_random_from_csv('last_name.csv', 380410).iloc[0, 0].upper(),  
        "Age":age_of_patience,
        "cbc":age_range,
        "blood values":blood_values_of_patience,
        "Hospital":"MIAMI HOSPITAL",
        "Gender":gender_of_patience,
        "Time":readable_time(timestamp=time.time())
    }


producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
start_time = time.time()

try:
    print("Producer started...")
    while time.time() - start_time < 120:
        case = case_production()
        turn = random.randint(0, 2)
        if turn == 1:
            time.sleep(5)
        producer.send("hospital_kafka", case)
        print(f"Sent: {case}")
        time.sleep(0.5)
except Exception as e:
    print(f"An error occured:\n{e}")
finally:
    sys.stdout.flush()
    producer.send("hospital_kafka", "info - Producer finished.")
    producer.close()
    print("Producer finished.")
