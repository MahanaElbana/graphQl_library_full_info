import json
with open("jsonData.json", mode="r") as j_object:
   data = json.load(j_object)
print(data[0]['__comment2__'])
