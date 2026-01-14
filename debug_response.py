"""
Debug test to see exact response structure
"""
import requests
import json

BASE_URL = "http://localhost:5000"

services = [
    ("S3", "/api/pricing/s3", {
        "storageClass": "General Purpose",
        "region": "US East (N. Virginia)",
        "storageGB": 100
    }),
    ("VPC", "/api/pricing/vpc", {
        "component": "NatGateway",
        "region": "US East (N. Virginia)",
        "quantity": 1
    })
]

for name, endpoint, payload in services:
    print(f"\n{'='*60}")
    print(f"{name} Response:")
    print(f"{'='*60}")
    r = requests.post(f'{BASE_URL}{endpoint}', json=payload)
    data = r.json()
    print(json.dumps(data, indent=2))
