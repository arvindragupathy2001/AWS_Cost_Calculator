import requests
import json

# Quick test
print("Testing EC2 pricing...")
r = requests.post('http://localhost:5000/api/pricing/ec2', json={
    "instanceType": "t2.micro",
    "region": "US East (N. Virginia)",
    "operatingSystem": "Linux",
    "tenancy": "Shared"
})
print(f"Status: {r.status_code}")
data = r.json()
print(f"Success: {data.get('success')}")
if data.get('data'):
    print(f"Price: {data['data'][0]['prices'][0]['amount']}")
    print(json.dumps(data['data'][0], indent=2))
else:
    print(f"Error: {data.get('error')}")
