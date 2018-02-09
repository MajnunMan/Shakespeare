import json


d = []
with open('truncated.json') as json_file:  
    data = json.load(json_file)
    for row in data:
        d.append([row["text"], row["user"]["followers_count"]])

print(d[109])
assert False
print(data[0]["user"]["friends_count"])
print(data[3]["user"]["followers_count"])
print(data[1]["user"]["favourites_count"])
print(data[1]["user"]["statuses_count"])
print(data[1]["user"]["listed_count"])
print(data[12]["retweet_count"])