import requests

BASE = "http://127.0.0.1:5000/"

data = [{"name":"jhon", "views":1000, "likes":100},
        {"name":"patric", "views":2000, "likes":200},
        {"name":"sarah", "views":3000, "likes":300}]

for i in range(len(data)):
    response = requests.put(BASE + "hotels/" + str(i), data[i])
    print(response.json())

input()
#response = requests.delete(BASE+"hotels/0")
#print(response)
input()
# response =requests.get(BASE + "hotels/2")
# print(response.json())