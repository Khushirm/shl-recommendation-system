import requests


url = "http://127.0.0.1:5000/recommend"

payload = {
    "query": "Looking to hire a Java developer for cognitive testing within 45 minutes"
}

response = requests.post(url, json=payload)

print("Status code:", response.status_code)
print("Response:", response.json())
