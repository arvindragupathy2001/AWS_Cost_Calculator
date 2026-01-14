"""
Comprehensive Diagnostic Test Suite
Tests each service individually and reports detailed results
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_service(name, endpoint, payload):
    """Test a single service and print detailed results"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")
    print(f"Endpoint: {endpoint}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=payload, timeout=10)
        print(f"\nHTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            
            if data.get('success'):
                pricing_data = data.get('data', [])
                print(f"Records returned: {len(pricing_data)}")
                
                if pricing_data:
                    first = pricing_data[0]
                    print(f"\nFirst result:")
                    print(json.dumps(first, indent=2))
                    
                    # Check for $0 pricing
                    prices = first.get('prices', [])
                    if prices:
                        amount = prices[0].get('amount', '0')
                        monthly = prices[0].get('monthly_cost', 0)
                        print(f"\n💰 Hourly Price: ${amount}")
                        if monthly:
                            print(f"💰 Monthly Cost: ${monthly}")
                        
                        if float(amount) == 0 and monthly == 0:
                            print("⚠️  WARNING: Pricing is $0!")
                    else:
                        print("⚠️  WARNING: No pricing information!")
                else:
                    print("❌ ERROR: No pricing data returned!")
            else:
                print(f"❌ ERROR: {data.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    print(f"{'='*60}\n")


def run_diagnostic_tests():
    """Run comprehensive diagnostic tests"""
    print(f"\n{'#'*60}")
    print("AWS PRICING CALCULATOR - COMPREHENSIVE DIAGNOSTIC TESTS")
    print(f"{'#'*60}\n")
    
    # Test EC2
    test_service(
        "EC2 - t2.micro Linux",
        "/api/pricing/ec2",
        {
            "instanceType": "t2.micro",
            "region": "US East (N. Virginia)",
            "operatingSystem": "Linux",
            "tenancy": "Shared"
        }
    )
    
    test_service(
        "EC2 - m5.large Windows",
        "/api/pricing/ec2",
        {
            "instanceType": "m5.large",
            "region": "US East (N. Virginia)",
            "operatingSystem": "Windows",
            "tenancy": "Shared"
        }
    )
    
    # Test RDS
    test_service(
        "RDS - db.t3.micro MySQL Single-AZ",
        "/api/pricing/rds",
        {
            "instanceType": "db.t3.micro",
            "region": "US East (N. Virginia)",
            "databaseEngine": "MySQL",
            "deploymentOption": "Single-AZ"
        }
    )
    
    # Test S3
    test_service(
        "S3 - 100GB Standard",
        "/api/pricing/s3",
        {
            "storageClass": "General Purpose",
            "region": "US East (N. Virginia)",
            "storageGB": 100
        }
    )
    
    # Test VPC
    test_service(
        "VPC - NAT Gateway",
        "/api/pricing/vpc",
        {
            "component": "NatGateway",
            "region": "US East (N. Virginia)",
            "quantity": 1
        }
    )
    
    # Test ALB
    test_service(
        "ALB - Application Load Balancer",
        "/api/pricing/alb",
        {
            "region": "US East (N. Virginia)",
            "quantity": 1
        }
    )
    
    # Test Route53
    test_service(
        "Route53 - Hosted Zone",
        "/api/pricing/route53",
        {
            "component": "HostedZone",
            "quantity": 1
        }
    )
    
    print(f"\n{'#'*60}")
    print("DIAGNOSTIC TESTS COMPLETE")
    print(f"{'#'*60}\n")


if __name__ == "__main__":
    print("\nMake sure the Flask server is running on http://localhost:5000")
    input("Press Enter to start diagnostic tests...")
    run_diagnostic_tests()
