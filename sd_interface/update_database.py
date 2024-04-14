import requests

url = "http://127.0.0.1:8081/v1/api/play"
post_data = {
        "waypoints": [{"latitude": 39.5291, "longitude": -119.8146, "clue": "Eldorado", "_id": "661acbbf944eaed13d747eb0"}, {"latitude": 39.5445, "longitude": -119.8159, "clue": "Student Union", "_id": "661acbbf944eaed13d747eb1"}, {"latitude": 39.5247, "longitude": -119.8116, "clue": "Post Office", "_id": "661acbbf944eaed13d747eb2"}, {"latitude": 39.5287, "longitude": -119.808, "clue": "Ballpark", "_id": "661acbbf944eaed13d747eb3"}],
    }
headers = {'Content-Type': 'application/json'}
id = "1"
response = requests.post(f"http://127.0.0.1:8081/v1/api/create/", json=post_data, headers=headers)
if response.status_code == 200:
    print("Successfully created new item:", response.json())
else:
    print("Failed to create item", response.status_code)

# api_data = requests.get(f"http://127.0.0.1:8081/questscape/v1/api/play/{id}")
# print(api_data)