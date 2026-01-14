"""
Quick Service Test - Test all 6 services
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_service(name, endpoint, payload):
    print(f"\n{'='*50}")
    print(f"Testing: {name}")
    print(f"{'='*50}")
    try:
        r = requests.post(f'{BASE_URL}{endpoint}', json=payload, timeout=10)
        data = r.json()
        print(f"Status: {r.status_code}")
        print(f"Success: {data.get('success')}")
        if data.get('success') and data.get('data'):
            price_info = data['data'][0]['prices'][0]
            print(f"✅ Price: ${price_info.get('amount')}/hr")
            monthly = price_info.get('monthly_cost', float(price_info.get('amount', 0)) * 730)
            print(f"✅ Monthly: ${monthly:.2f}")
        else:
            print(f"❌ Error: {data.get('error', 'No pricing data')}")
    except Exception as e:
        print(f"❌ Exception: {e}")

print("\n🧪 TESTING ALL 6 AWS SERVICES")
print("Region: US East (N. Virginia)\n")

# Test EC2
test_service("EC2", "/api/pricing/ec2", {
    "instanceType": "t2.micro",
    "region": "US East (N. Virginia)",
    "operatingSystem": "Linux",
    "tenancy": "Shared"
})

# Test RDS
test_service("RDS", "/api/pricing/rds", {
    "instanceType": "db.t3.micro",
    "region": "US East (N. Virginia)",
    "databaseEngine": "MySQL",
    "deploymentOption": "Single-AZ"
})

# Test S3
test_service("S3", "/api/pricing/s3", {
    "storageClass": "General Purpose",
    "region": "US East (N. Virginia)",
    "storageGB": 100
})

# Test VPC
test_service("VPC", "/api/pricing/vpc", {
    "component": "NatGateway",
    "region": "US East (N. Virginia)",
    "quantity": 1
})

# Test ALB
test_service("ALB", "/api/pricing/alb", {
    "region": "US East (N. Virginia)",
    "quantity": 1
})

# Test Route53
test_service("Route53", "/api/pricing/route53", {
    "component": "HostedZone",
    "quantity": 1
})

print("\n" + "="*50)
print("TEST COMPLETE")
print("="*50 + "\n")
