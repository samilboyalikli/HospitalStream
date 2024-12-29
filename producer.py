# For now, I will code the city and age assignment mechanisms. 

import random

cities = ["Houston","Dallas","Jersey City","Washington","Boston"]
age_ranges = ["child","adult","senior"]
age_weights = [1,10,15]
random_age_ranges = random.choices(age_ranges, weights=age_weights, k=1)

if random_age_ranges[0] == "child":
    age = random.randint(0,18)
elif random_age_ranges[0] == "adult":
    age = random.randint(18,65)
else:
    age = random.randint(65,80)
    
city = random.choice(cities)
print(city, age)

#--------------------------------------------------------------------
# import socket
# import time
# 
# host = "127.0.0.1"
# port = 5005
# start_time = time.time()
# 
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     try: 
#         s.connect((host, port))
#         s.sendall("producer connected".encode('utf-8'))
#         while time.time() - start_time < 60:
#             number = random.randint(0,100)
#             message = f"{number}\n"
#             s.sendall(message.encode('utf-8'))
#             print(f"Sent: {number}")
#             time.sleep(1)
#     except Exception as e:
#         print(f"There is a problem. Problem is:\n{e}")
#-------------------------------------------------------------------