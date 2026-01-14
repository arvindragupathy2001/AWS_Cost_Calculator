"""
Debug test - Check if bulk pricing client is working
"""

from bulk_pricing import get_bulk_pricing_client

print("Testing bulk pricing client directly...")

client = get_bulk_pricing_client()

print(f"\nClient object: {client}")
print(f"Pricing data keys: {client.pricing_data.keys()}")
print(f"\nEC2 data available: {'EC2' in client.pricing_data}")

if 'EC2' in client.pricing_data:
    ec2_data = client.pricing_data['EC2']
    print(f"EC2 regions: {ec2_data.keys()}")
    
    if 'US East (N. Virginia)' in ec2_data:
        us_east = ec2_data['US East (N. Virginia)']
        print(f"US East instances: {list(us_east.keys())[:5]}")
        print(f"t2.micro pricing: {us_east.get('t2.micro')}")

print("\n\nTesting find_ec2_pricing method...")
result = client.find_ec2_pricing('t2.micro', 'US East (N. Virginia)', 'Linux')
print(f"Result: {result}")

if result:
    print(f"\nPrice: {result[0]['prices'][0]['amount']}")
