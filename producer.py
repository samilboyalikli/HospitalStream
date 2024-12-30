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


def city():
    cities = ["Houston","Dallas","Jersey City","Washington","Boston"]
    city = random.choice(cities)
    return city


def case_production():
    case_dict = {
        "Name":select_random_from_csv("gender_name.csv", 13962).iloc[0, 1].upper(),
        "Surname":select_random_from_csv('last_name.csv', 380410).iloc[0, 0].upper(),
        "Age":age(),
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
