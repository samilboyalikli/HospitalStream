# For now, I will code the city and age assignment mechanisms. 

import random

cities = ["Houston","Dallas","Jersey City","Washington","Boston"]

random_age = random.randint(0,18)
random_city = random.choice(cities)
print(random_city, random_age)

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