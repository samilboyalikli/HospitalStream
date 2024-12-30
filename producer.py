import random
import pandas
import socket
import time
import json


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
        value = random.randint(4000,19000)
        return value
    elif age >= 2 and age <= 12:
        value = random.randint(3000,17000)
        return value
    else: 
        value = random.randint(3000,15000)
        return value


def rbc_for_children(age):
    if age >= 0 and age <= 2:
        value = random.randint(3500000,6500000)
        return value
    elif age >= 2 and age <= 12:
        value = random.randint(3800000,5500000)
        return value
    else: 
        value = random.randint(3800000,6000000)
        return value

def hb_for_children(age,gender):
    if age >= 0 and age <= 2:
        value = random.randint(9.0,15.0)
        return value
    elif age >= 2 and age <= 12:
        value = random.randint(10.0,16.0)
        return value
    else: 
        if gender == "MALE":
            value = random.randint(12.0,17.0)
            return value
        else:
            value = random.randint(11.0,16.0)
            return value    


def hm_for_children(age,gender):
    if age >= 0 and age <= 2:
        value = random.randint(30,45)
        return value
    elif age >= 2 and age <= 12:
        value = random.randint(30,45)
        return value
    else: 
        if gender == "MALE":
            value = random.randint(35,55)
            return value
        else:
            value = random.randint(32,47)
            return value    


def platelet_for_children(age):
    if age >= 0 and age <= 2:
        value = random.randint(125000,475000)
        return value
    elif age >= 2 and age <= 12:
        value = random.randint(125000,475000)
        return value
    else: 
        value = random.randint(125000,475000)
        return value


def mcv_for_children(age):
    if age >= 0 and age <= 2:
        value = random.randint(65,90)
        return value
    elif age >= 2 and age <= 12:
        value = random.randint(70,95)
        return value
    else: 
        value = random.randint(75,100)
        return value


def mch_for_children(age):
    if age >= 0 and age <= 2:
        value = random.randint(20,35)
        return value
    elif age >= 2 and age <= 12:
        value = random.randint(20,37)
        return value
    else: 
        value = random.randint(20,40)
        return value


def mchc_for_children(age):
    if age >= 0 and age <= 2:
        value = random.randint(25,40)
        return value
    elif age >= 2 and age <= 12:
        value = random.randint(30,40)
        return value
    else: 
        value = random.randint(30,40)
        return value


def cbc(age):
    if age >= 0 and age <= 18:
        return "child"
    elif age >= 18 and age <= 65:
        return "adult"
    else: return "senior"


# "wbc":wbc_for_children(age),
# "rbc":rbc_for_children(age),
# "hb":hb_for_children(age,gender),
# "hm":hm_for_children(age,gender),
# "mcv":mcv_for_children(age),
# "mch":mch_for_children(age),
# "mchc":mchc_for_children(age)


def children_values():
    return {
        "wbc":"water blood cell",
        "rbc":"red blood cell",
        "hb":"hemoglobin",
        "hm":"hematocrit",
        "mcv":"mean corpuscular volume",
        "mch":"mean corpuscular hemoglobin",
        "mchc":"mean corpuscular hemoglobin concentration"
    }


def adult_values():
    return {
        "wbc":"water blood cell",
        "rbc":"red blood cell",
        "hb":"hemoglobin",
        "hm":"hematocrit",
        "mcv":"mean corpuscular volume",
        "mch":"mean corpuscular hemoglobin",
        "mchc":"mean corpuscular hemoglobin concentration"
    }


def senior_values():
    return {
        "wbc":"water blood cell",
        "rbc":"red blood cell",
        "hb":"hemoglobin",
        "hm":"hematocrit",
        "mcv":"mean corpuscular volume",
        "mch":"mean corpuscular hemoglobin",
        "mchc":"mean corpuscular hemoglobin concentration"
    }


def blood_values(age_range):
    if age_range == "child":
        return children_values()
    elif age_range == "adult":
        return adult_values()
    else: return senior_values()


def city():
    cities = ["Houston","Dallas","Jersey City","Washington","Boston"]
    city = random.choice(cities)
    return city


def case_production():
    age_of_patience = age()
    age_range = cbc(age_of_patience)
    case_dict = {
        "Name":select_random_from_csv("gender_name.csv", 13962).iloc[0, 1].upper(),
        "Surname":select_random_from_csv('last_name.csv', 380410).iloc[0, 0].upper(),  
        "Age":age_of_patience,
        "cbc":age_range,
        "blood values": {blood_values()},
        "Hospital":city().upper(),
        "Gender":select_random_from_csv("gender_name.csv", 13962).iloc[0, 0].upper()
    }
    return case_dict


host = "127.0.0.1"
port = 5005
start_time = time.time()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try: 
        s.connect((host, port))
        s.sendall("producer connected".encode('utf-8'))
        while time.time() - start_time < 60:
            case_json = json.dumps(case_production())
            case = case_json.encode('utf-8')
            turn = random.randint(0,2)
            if turn == 1:
                time.sleep(5)
            s.sendall(case)
            print(f"Sent: {case}")
            time.sleep(0.5)
    except Exception as e:
        print(f"There is a problem. Problem is:\n{e}")
