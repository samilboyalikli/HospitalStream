# TODO
# Some blood values of age ranges is same, we can join thats.

from kafka import KafkaProducer
import random
import pandas
import time
import json
import sys

# progress time indicates the running time of the producer.
progress_time = 600


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
    """
    Ideal Values for 0-2 Age Range: 6000-17500
    Ideal Values for 2-12 Age Range: 5000-15000
    Ideal Values for 12-18 Age Range: 4500-13500
    """
    if age >= 0 and age <= 2:
        return random.randint(4000,19000)
    elif age >= 2 and age <= 12:
        return random.randint(3000,17000)
    else: 
        return random.randint(3000,15000)


def rbc_for_children(age):
    """
    Ideal Values for 0-2 Age Range: 3900000-5500000
    Ideal Values for 2-12 Age Range: 4000000-5200000
    Ideal Values for 12-18 Age Range: 4100000-5600000
    """
    if age >= 0 and age <= 2:
        return random.randint(3500000,6500000)
    elif age >= 2 and age <= 12:
        return random.randint(3800000,5500000)
    else: 
        return random.randint(3800000,6000000)


def hb_for_children(age,gender):
    """
    Ideal Values for 0-2 Age Range: 10.0-14.0
    Ideal Values for 2-12 Age Range: 11.5-15.5
    Ideal Values for 12-18 Age Boys: 13.0-16.0
    Ideal Values for 12-18 Age Girls: 12.0-15.0
    """
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
    """
    Ideal Values for 0-2 Age Range: 33-43
    Ideal Values for 2-12 Age Range: 34-42
    Ideal Values for 12-18 Age Boys: 40-50
    Ideal Values for 12-18 Age Girls: 36-45
    """
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
    """
    Ideal Values for All Age Range: 150000-450000
    """
    if age >= 0 and age <= 2:
        return random.randint(125000,475000)
    elif age >= 2 and age <= 12:
        return random.randint(125000,475000)
    else: 
        return random.randint(125000,475000)


def mcv_for_children(age):
    """
    Ideal Values for 0-2 Age Range: 70-86
    Ideal Values for 2-12 Age Range: 75-87
    Ideal Values for 12-18 Age Range: 80-96
    """
    if age >= 0 and age <= 2:
        return random.randint(65,90)
    elif age >= 2 and age <= 12:
        return random.randint(70,95)
    else: 
        return random.randint(75,100)


def mch_for_children(age):
    """
    Ideal Values for 0-2 Age Range: 24-30
    Ideal Values for 2-12 Age Range: 26-32
    Ideal Values for 12-18 Age Range: 28-34
    """
    if age >= 0 and age <= 2:
        return random.randint(20,35)
    elif age >= 2 and age <= 12:
        return random.randint(20,37)
    else: 
        return random.randint(20,40)


def mchc_for_children(age):
    """
    Ideal Values for 0-2 Age Range: 30-36
    Ideal Values for 2-18 Age Range: 32-36
    """
    if age >= 0 and age <= 2:
        return random.randint(25,40)
    elif age >= 2 and age <= 12:
        return random.randint(30,40)
    else: 
        return random.randint(30,40)


def wbc_for_adult():
    """
    Ideal Values: 4000-11000
    """
    return random.randint(3000,12000)


def rbc_for_adult(gender):
    """
    Ideal Values for Male: 4700000-6100000
    Ideal Values for Female: 4200000-5400000
    """
    if gender == "MALE":
        return random.randint(4500000,6500000)
    else: return random.randint(3700000,5700000)


def hb_for_adult(gender):
    """
    Ideal Values for Male: 13.5-17.5
    Ideal Values for Female: 12.0-15.5
    """
    if gender == "MALE":
        return round(random.uniform(12.0,19.0),1)
    else: return round(random.uniform(10.0,17.0),1)


def hm_for_adult(gender):
    """
    Ideal Values for Male: 41-50
    Ideal Values for Female: 36-44
    """
    if gender == "MALE":
        return random.randint(35,55)
    else: return random.randint(30,50)


def mcv_for_adult():
    """
    Ideal Values: 80-100
    """
    return random.randint(70,120)


def mch_for_adult():
    """
    Ideal Values: 27-33
    """
    return random.randint(20,40)


def mchc_for_adult():
    """
    Ideal Values: 32-36
    """
    return random.randint(25,40)


def wbc_for_senior():
    """
    Ideal Values: 4000-11000
    """
    return random.randint(3000,12000)


def rbc_for_senior(gender):
    """
    Ideal Values for Male: 4500000-5900000
    Ideal Values for Female: 4100000-5100000
    """
    if gender == "MALE":
        return random.randint(4000000,7000000)
    else: return random.randint(3500000,6000000)


def hb_for_senior(gender):
    """
    Ideal Values for Male: 13.0-17.0
    Ideal Values for Female: 12.0-15.0
    """
    if gender == "MALE":
        return round(random.uniform(11.0,19.0),1)
    else: return round(random.uniform(10.0,17.0),1)


def hm_for_senior(gender):
    """
    Ideal Values for Male: 39-50
    Ideal Values for Female: 36-46
    """
    if gender == "MALE":
        return random.randint(30,60)
    else: return random.randint(25,55)


def mcv_for_senior():
    """
    Ideal Values: 80-100
    """
    return random.randint(70,110)


def mch_for_senior():
    """
    Ideal Values: 27-33 
    """
    return random.randint(20,40)


def mchc_for_senior():
    """
    Ideal Values: 32-36
    """
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
        "bloodValues":blood_values_of_patience,
        "Hospital":"ATLANTA HOSPITAL",
        "Gender":gender_of_patience,
        "Time":readable_time(timestamp=time.time())
    }


producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
start_time = time.time()
message_count = 0

try:
    print("Producer started...")
    while time.time() - start_time < progress_time:
        case = case_production()
        turn = random.randint(0, 2)
        if turn == 1:
            time.sleep(5)
        producer.send("raw_stream", case)
        print(f"Sent: {case}")
        message_count = message_count + 1
        time.sleep(0.5)
except Exception as e:
    print(f"An error occured:\n{e}")
finally:
    sys.stdout.flush()
    producer.send("raw_stream", f"Send {message_count} messages from Atlanta Hospital.")
    producer.send("raw_stream", "info - Atlanta stream finished.")
    producer.send("raw_stream", "info - a producer finished.")
    producer.close()
    print("Producer finished.")
