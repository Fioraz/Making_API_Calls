import requests

response = requests.get(url="http://api.open-notify.org/iss-now.json")

print(response)
print(response.status_code)    # Check the http status of response: if 1XX - hold on,
# 2XX - here you go, 3XX - Go away (no permission), 4XX - You screwed up (not found),
# 5XX - I screwed up (server issue)

response.raise_for_status()     # raise an exception

all_data = response.json()  # All the data in the dictionary
data = response.json()["iss_position"]  # Data of the specified key
print(all_data)
print(data)

longitude = response.json()["iss_position"]["longitude"]
latitude = response.json()["iss_position"]["latitude"]

iss_position = (longitude, latitude)
print(iss_position)


