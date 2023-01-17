# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Trying to test the PUT functionality of requests
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Created by Felix Bo Caspersen, s183319 on Tue Jan 17 2023

import requests

pload = {"username": "Olivia", "password": "123"}
response = requests.post("https://httpbin.org/post", data=pload)

print(f"Content of the thing PUT: \n{response.content}\n")
print(f"The thing we PUT, but as a json: \n{response.json()}\n")
