"""
Automated Test Suite for AWS Pricing Calculator

Tests all major functionality including:
- Credential detection and fallback
- Pricing queries for all 6 services
- Cart operations (add, remove, clear, total)
- CSV export
- Error handling
"""

import requests
import json
import time
from typing import Dict, List

# Configuration
BASE_URL = "http://localhost:5000"
TIMEOUT = 120  # Longer timeout for bulk pricing downloads


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class TestRunner:
    """Test runner with results tracking"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def test(self, name: str, func):
        """Run a single test"""
        print(f"\n{Colors.BLUE}Testing:{Colors.RESET} {name}...")
        try:
            func()
            print(f"{Colors.GREEN}✓ PASS{Colors.RESET}")
            self.passed += 1
            self.tests.append((name, True, None))
        except AssertionError as e:
            print(f"{Colors.RED}✗ FAIL{Colors.RESET}: {str(e)}")
            self.failed += 1
            self.tests.append((name, False, str(e)))
        except Exception as e:
            print(f"{Colors.RED}✗ ERROR{Colors.RESET}: {str(e)}")
            self.failed += 1
            self.tests.append((name, False, f"Exception: {str(e)}"))
    
    def print_summary(self):
        """Print test summary"""
        total = self.passed + self.failed
        print(f"\n{'='*70}")
        print(f"{Colors.BOLD}TEST SUMMARY{Colors.RESET}")
        print(f"{'='*70}")
        print(f"Total Tests: {total}")
        print(f"{Colors.GREEN}Passed: {self.passed}{Colors.RESET}")
        print(f"{Colors.RED}Failed: {self.failed}{Colors.RESET}")
        print(f"Success Rate: {(self.passed/total*100):.1f}%" if total > 0 else "N/A")
        print(f"{'='*70}\n")
        
        if self.failed > 0:
            print(f"{Colors.RED}Failed Tests:{Colors.RESET}")
            for name, passed, error in self.tests:
                if not passed:
                    print(f"  - {name}: {error}")


# Initialize test runner
runner = TestRunner()


def assert_response_ok(response, message=""):
    """Assert HTTP response is successful"""
    assert response.status_code == 200, f"HTTP {response.status_code}: {message}"


def assert_json_success(data: Dict):
    """Assert JSON response indicates success"""
    assert data.get('success') == True, f"API returned success=False: {data.get('error', 'Unknown error')}"


# ==================== CONNECTION TESTS ====================

def test_server_running():
    """Test that server is running"""
    response = requests.get(f"{BASE_URL}/", timeout=5)
    assert_response_ok(response, "Server not responding")
    assert "AWS Cost Calculator" in response.text


def test_connection_status():
    """Test AWS connection endpoint"""
    response = requests.get(f"{BASE_URL}/api/test-connection", timeout=5)
    assert_response_ok(response)
    data = response.json()
    # May succeed or fail depending on credentials, just verify it responds
    assert 'success' in data


# ==================== PRICING API TESTS ====================

def test_ec2_pricing():
    """Test EC2 pricing query"""
    payload = {
        "instanceType": "t2.micro",
        "region": "US East (N. Virginia)",
        "operatingSystem": "Linux",
        "tenancy": "Shared"
    }
    print("  (First query may take 30-60s to download pricing data...)")
    response = requests.post(f"{BASE_URL}/api/pricing/ec2", json=payload, timeout=TIMEOUT)
    assert_response_ok(response)
    data = response.json()
    assert_json_success(data)
    assert 'data' in data
    assert 'count' in data


def test_rds_pricing():
    """Test RDS pricing query"""
    payload = {
        "instanceType": "db.t3.micro",
        "region": "US East (N. Virginia)",
        "databaseEngine": "MySQL",
        "deploymentOption": "Single-AZ"
    }
    print("  (May take time if RDS pricing not cached...)")
    response = requests.post(f"{BASE_URL}/api/pricing/rds", json=payload, timeout=TIMEOUT)
    assert_response_ok(response)
    data = response.json()
    assert_json_success(data)


def test_s3_pricing():
    """Test S3 pricing query"""
    payload = {
        "storageClass": "General Purpose",
        "region": "US East (N. Virginia)",
        "storageGB": 100
    }
    response = requests.post(f"{BASE_URL}/api/pricing/s3", json=payload, timeout=TIMEOUT)
    assert_response_ok(response)
    data = response.json()
    assert_json_success(data)


def test_vpc_pricing():
    """Test VPC pricing query"""
    payload = {
        "component": "NatGateway",
        "region": "US East (N. Virginia)",
        "quantity": 1
    }
    response = requests.post(f"{BASE_URL}/api/pricing/vpc", json=payload, timeout=TIMEOUT)
    assert_response_ok(response)
    data = response.json()
    # VPC pricing might not always return data, just verify API works
    assert 'success' in data


def test_alb_pricing():
    """Test ALB pricing query"""
    payload = {
        "region": "US East (N. Virginia)",
        "quantity": 1
    }
    response = requests.post(f"{BASE_URL}/api/pricing/alb", json=payload, timeout=TIMEOUT)
    assert_response_ok(response)
    data = response.json()
    assert 'success' in data


def test_route53_pricing():
    """Test Route53 pricing query"""
    payload = {
        "component": "HostedZone",
        "quantity": 1
    }
    response = requests.post(f"{BASE_URL}/api/pricing/route53", json=payload, timeout=TIMEOUT)
    assert_response_ok(response)
    data = response.json()
    assert 'success' in data


# ==================== CART TESTS ====================

def test_cart_clear():
    """Test clearing cart"""
    response = requests.delete(f"{BASE_URL}/api/cart/clear", timeout=5)
    assert_response_ok(response)
    data = response.json()
    assert_json_success(data)


def test_cart_empty():
    """Test getting empty cart"""
    response = requests.get(f"{BASE_URL}/api/cart/items", timeout=5)
    assert_response_ok(response)
    data = response.json()
    assert_json_success(data)
    assert data['count'] == 0


def test_cart_add_item():
    """Test adding item to cart"""
    item = {
        "service": "EC2",
        "resourceType": "t2.micro",
        "specifications": "1 vCPU, 1GB RAM, Linux",
        "region": "US East (N. Virginia)",
        "quantity": 1,
        "hourlyCost": 0.0116,
        "monthlyCost": 8.468
    }
    response = requests.post(f"{BASE_URL}/api/cart/add", json=item, timeout=5)
    assert_response_ok(response)
    data = response.json()
    assert_json_success(data)
    assert data['cartCount'] == 1


def test_cart_get_items():
    """Test getting cart items"""
    response = requests.get(f"{BASE_URL}/api/cart/items", timeout=5)
    assert_response_ok(response)
    data = response.json()
    assert_json_success(data)
    assert data['count'] >= 1
    assert len(data['items']) >= 1


def test_cart_total():
    """Test getting cart total"""
    response = requests.get(f"{BASE_URL}/api/cart/total", timeout=5)
    assert_response_ok(response)
    data = response.json()
    assert_json_success(data)
    assert 'total' in data
    assert data['total'] > 0


def test_cart_add_multiple():
    """Test adding multiple items"""
    items = [
        {
            "service": "RDS",
            "resourceType": "db.t3.micro",
            "specifications": "MySQL, Single-AZ",
            "region": "US East (N. Virginia)",
            "quantity": 1,
            "hourlyCost": 0.017,
            "monthlyCost": 12.41
        },
        {
            "service": "S3",
            "resourceType": "Storage",
            "specifications": "100 GB, Standard",
            "region": "US East (N. Virginia)",
            "quantity": 1,
            "hourlyCost": 0.003,
            "monthlyCost": 2.30
        }
    ]
    
    for item in items:
        response = requests.post(f"{BASE_URL}/api/cart/add", json=item, timeout=5)
        assert_response_ok(response)
    
    # Verify count
    response = requests.get(f"{BASE_URL}/api/cart/items", timeout=5)
    data = response.json()
    assert data['count'] >= 3


def test_cart_remove_item():
    """Test removing item from cart"""
    # Get current items
    response = requests.get(f"{BASE_URL}/api/cart/items", timeout=5)
    data = response.json()
    
    if data['count'] > 0:
        item_id = data['items'][0]['id']
        
        # Remove the item
        response = requests.delete(f"{BASE_URL}/api/cart/remove/{item_id}", timeout=5)
        assert_response_ok(response)
        result = response.json()
        assert_json_success(result)


# ==================== EXPORT TESTS ====================

def test_csv_export():
    """Test CSV export"""
    # First ensure cart has items
    response = requests.get(f"{BASE_URL}/api/cart/items", timeout=5)
    data = response.json()
    
    if data['count'] == 0:
        # Add a test item
        test_cart_add_item()
    
    # Export CSV
    response = requests.get(f"{BASE_URL}/api/export/csv", timeout=10)
    assert_response_ok(response)
    assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'
    assert 'attachment' in response.headers.get('Content-Disposition', '')
    
    # Verify CSV content
    csv_content = response.text
    assert 'AWS Cost Estimate Report' in csv_content
    assert 'Service' in csv_content
    assert 'Total Monthly Cost' in csv_content


# ==================== ERROR HANDLING TESTS ====================

def test_invalid_endpoint():
    """Test 404 error handling"""
    response = requests.get(f"{BASE_URL}/api/nonexistent", timeout=5)
    assert response.status_code == 404


def test_invalid_cart_remove():
    """Test removing non-existent cart item"""
    response = requests.delete(f"{BASE_URL}/api/cart/remove/invalid-id", timeout=5)
    assert_response_ok(response)
    # Should succeed but not actually remove anything


# ==================== RUN ALL TESTS ====================

def run_all_tests():
    """Run complete test suite"""
    print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}AWS PRICING CALCULATOR - AUTOMATED TEST SUITE{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"\nTesting server at: {BASE_URL}")
    print(f"Timeout: {TIMEOUT}s")
    print(f"\n{Colors.YELLOW}Note: First-time pricing queries may take 30-60s to download data{Colors.RESET}")
    
    # Connection Tests
    print(f"\n{Colors.BOLD}--- CONNECTION TESTS ---{Colors.RESET}")
    runner.test("Server Running", test_server_running)
    runner.test("Connection Status API", test_connection_status)
    
    # Pricing API Tests
    print(f"\n{Colors.BOLD}--- PRICING API TESTS ---{Colors.RESET}")
    runner.test("EC2 Pricing Query", test_ec2_pricing)
    runner.test("RDS Pricing Query", test_rds_pricing)
    runner.test("S3 Pricing Query", test_s3_pricing)
    runner.test("VPC Pricing Query", test_vpc_pricing)
    runner.test("ALB Pricing Query", test_alb_pricing)
    runner.test("Route53 Pricing Query", test_route53_pricing)
    
    # Cart Tests
    print(f"\n{Colors.BOLD}--- CART FUNCTIONALITY TESTS ---{Colors.RESET}")
    runner.test("Clear Cart", test_cart_clear)
    runner.test("Get Empty Cart", test_cart_empty)
    runner.test("Add Item to Cart", test_cart_add_item)
    runner.test("Get Cart Items", test_cart_get_items)
    runner.test("Get Cart Total", test_cart_total)
    runner.test("Add Multiple Items", test_cart_add_multiple)
    runner.test("Remove Cart Item", test_cart_remove_item)
    
    # Export Tests
    print(f"\n{Colors.BOLD}--- EXPORT TESTS ---{Colors.RESET}")
    runner.test("CSV Export", test_csv_export)
    
    # Error Handling Tests
    print(f"\n{Colors.BOLD}--- ERROR HANDLING TESTS ---{Colors.RESET}")
    runner.test("404 Not Found", test_invalid_endpoint)
    runner.test("Invalid Cart Remove", test_invalid_cart_remove)
    
    # Print summary
    runner.print_summary()
    
    return runner.passed, runner.failed


if __name__ == "__main__":
    try:
        passed, failed = run_all_tests()
        
        # Exit with appropriate code
        exit(0 if failed == 0 else 1)
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrupted by user{Colors.RESET}")
        exit(130)
    except Exception as e:
        print(f"\n\n{Colors.RED}Fatal error: {e}{Colors.RESET}")
        exit(1)
