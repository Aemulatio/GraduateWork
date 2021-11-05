import base64
import json

base = base64.b64encode(
    "https://img-cdn.hltv.org/playerbodyshot/XjTF3SIIO8xuGqQZiBAGBd.png?ixlib=java-2.1.0&w=400&s=d9e874f4a6899cf8bc89b91546b67974".encode())

print(base)

f = open("../Data/New/teams.json")
# jj = f.read()
# js = json.loads(jj)
# print(js)
# print("---")
# print(js.keys())
# print(type(json.loads(f.read())))
print(json.loads(f.read()).keys())
# print(type(js))
