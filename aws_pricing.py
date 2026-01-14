"""
AWS Pricing API Integration Module

This module provides functions to interact with the AWS Pricing API
to retrieve pricing information for various AWS services.
Supports both AWS API (with credentials) and public bulk pricing (no credentials).
"""

import boto3
import json
from typing import Dict, List, Optional
from botocore.exceptions import ClientError, BotoCoreError, NoCredentialsError
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AWSPricingClient:
    """Client for interacting with AWS Pricing API with bulk pricing fallback"""
    
    def __init__(self, region_name: str = 'us-east-1', use_bulk_fallback: bool = True):
        """
        Initialize the AWS Pricing client.
        
        Args:
            region_name: AWS region (Pricing API is accessed via us-east-1)
            use_bulk_fallback: If True, fall back to bulk pricing when credentials unavailable
        """
        self.use_bulk_pricing = False
        self.bulk_client = None
        
        try:
            self.client = boto3.client('pricing', region_name=region_name)
            # Test if credentials work
            self.client.describe_services(MaxResults=1)
            logger.info("✅ AWS Pricing API initialized with credentials")
        except (NoCredentialsError, ClientError) as e:
            if use_bulk_fallback:
                logger.warning("⚠️  No AWS credentials found, using public bulk pricing")
                from bulk_pricing import get_bulk_pricing_client
                self.bulk_client = get_bulk_pricing_client()
                self.use_bulk_pricing = True
                self.client = None
            else:
                raise Exception(f"Failed to initialize AWS Pricing client: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to initialize AWS Pricing client: {str(e)}")

    
    def get_services(self) -> List[str]:
        """
        Get a list of available AWS services.
        
        Returns:
            List of service codes
        """
        try:
            response = self.client.describe_services(MaxResults=100)
            services = [service['ServiceCode'] for service in response.get('Services', [])]
            return sorted(services)
        except (ClientError, BotoCoreError) as e:
            raise Exception(f"Error fetching services: {str(e)}")
    
    def get_service_attributes(self, service_code: str) -> List[Dict]:
        """
        Get attributes for a specific service.
        
        Args:
            service_code: AWS service code (e.g., 'AmazonEC2')
            
        Returns:
            List of attribute names and values
        """
        try:
            response = self.client.describe_services(
                ServiceCode=service_code,
                MaxResults=1
            )
            
            if not response.get('Services'):
                return []
            
            attributes = response['Services'][0].get('AttributeNames', [])
            return attributes
        except (ClientError, BotoCoreError) as e:
            raise Exception(f"Error fetching service attributes: {str(e)}")
    
    def get_products(self, service_code: str, filters: Optional[List[Dict]] = None, max_results: int = 100) -> List[Dict]:
        """
        Get products and pricing for a specific service.
        
        Args:
            service_code: AWS service code (e.g., 'AmazonEC2')
            filters: List of filter dictionaries with Type, Field, and Value
            max_results: Maximum number of results to return
            
        Returns:
            List of product pricing information
        """
        try:
            params = {
                'ServiceCode': service_code,
                'MaxResults': max_results
            }
            
            if filters:
                params['Filters'] = filters
            
            response = self.client.get_products(**params)
            
            products = []
            for price_item in response.get('PriceList', []):
                # Parse the JSON string
                product_data = json.loads(price_item)
                products.append(product_data)
            
            return products
        except (ClientError, BotoCoreError) as e:
            raise Exception(f"Error fetching products: {str(e)}")
    
    def get_ec2_pricing(self, instance_type: str = 't2.micro', region: str = 'US East (N. Virginia)', 
                        operating_system: str = 'Linux', tenancy: str = 'Shared') -> List[Dict]:
        """
        Get EC2 instance pricing.
        
        Args:
            instance_type: EC2 instance type (e.g., 't2.micro')
            region: AWS region location
            operating_system: Operating system (Linux, Windows, etc.)
            tenancy: Tenancy type (Shared, Dedicated, Host)
            
        Returns:
            List of pricing information for the instance
        """
        # Use bulk pricing if in fallback mode
        if self.use_bulk_pricing:
            return self.bulk_client.find_ec2_pricing(instance_type, region, operating_system)
        
        # Use AWS API
        filters = [
            {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
            {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': operating_system},
            {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': tenancy},
            {'Type': 'TERM_MATCH', 'Field': 'preInstalledSw', 'Value': 'NA'},
            {'Type': 'TERM_MATCH', 'Field': 'capacitystatus', 'Value': 'Used'}
        ]
        
        return self.get_products('AmazonEC2', filters, max_results=10)
    
    def get_rds_pricing(self, instance_type: str = 'db.t3.micro', region: str = 'US East (N. Virginia)',
                        database_engine: str = 'MySQL', deployment_option: str = 'Single-AZ') -> List[Dict]:
        """
        Get RDS instance pricing.
        
        Args:
            instance_type: RDS instance type (e.g., 'db.t3.micro')
            region: AWS region location
            database_engine: Database engine (MySQL, PostgreSQL, etc.)
            deployment_option: Deployment option (Single-AZ, Multi-AZ)
            
        Returns:
            List of pricing information for the RDS instance
        """
        # Use bulk pricing if in fallback mode
        if self.use_bulk_pricing:
            return self.bulk_client.find_rds_pricing(instance_type, region, database_engine, deployment_option)
        
        # Use AWS API
        filters = [
            {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
            {'Type': 'TERM_MATCH', 'Field': 'databaseEngine', 'Value': database_engine},
            {'Type': 'TERM_MATCH', 'Field': 'deploymentOption', 'Value': deployment_option}
        ]
        
        return self.get_products('AmazonRDS', filters, max_results=10)
    
    def format_pricing_data(self, products: List[Dict]) -> List[Dict]:
        """
        Format raw pricing data into a more readable structure.
        
        Args:
            products: List of raw product data from AWS API
            
        Returns:
            List of formatted pricing information
        """
        formatted_results = []
        
        for product in products:
            try:
                # Extract product attributes
                product_attrs = product.get('product', {}).get('attributes', {})
                
                # Extract pricing terms (On-Demand)
                terms = product.get('terms', {})
                on_demand = terms.get('OnDemand', {})
                
                pricing_info = {
                    'description': product_attrs.get('instanceType', 'N/A'),
                    'location': product_attrs.get('location', 'N/A'),
                    'instanceType': product_attrs.get('instanceType', 'N/A'),
                    'vcpu': product_attrs.get('vcpu', 'N/A'),
                    'memory': product_attrs.get('memory', 'N/A'),
                    'storage': product_attrs.get('storage', 'N/A'),
                    'networkPerformance': product_attrs.get('networkPerformance', 'N/A'),
                    'prices': []
                }
                
                # Extract price per hour
                for offer_term in on_demand.values():
                    for price_dimension in offer_term.get('priceDimensions', {}).values():
                        price_per_unit = price_dimension.get('pricePerUnit', {}).get('USD', 'N/A')
                        unit = price_dimension.get('unit', 'N/A')
                        description = price_dimension.get('description', 'N/A')
                        
                        pricing_info['prices'].append({
                            'amount': price_per_unit,
                            'unit': unit,
                            'description': description
                        })
                
                formatted_results.append(pricing_info)
            except Exception as e:
                # Skip products that can't be parsed
                continue
        
        return formatted_results

    def get_s3_pricing(self, storage_class: str = 'General Purpose', region: str = 'US East (N. Virginia)') -> List[Dict]:
        """
        Get S3 storage pricing.
        
        Args:
            storage_class: Storage class (General Purpose, Infrequent Access, Glacier, etc.)
            region: AWS region location
            
        Returns:
            List of pricing information for S3 storage
        """
        # Use bulk pricing if in fallback mode
        if self.use_bulk_pricing:
            # Return basic structure, will be formatted with storage_gb in format_s3_pricing_data
            return self.bulk_client.find_s3_pricing(storage_class, region, 0)
        
        filters = [
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
            {'Type': 'TERM_MATCH', 'Field': 'storageClass', 'Value': storage_class},
            {'Type': 'TERM_MATCH', 'Field': 'volumeType', 'Value': 'Standard'}
        ]
        
        return self.get_products('AmazonS3', filters, max_results=10)
    
    def get_vpc_pricing(self, component: str = 'NatGateway', region: str = 'US East (N. Virginia)') -> List[Dict]:
        """
        Get VPC component pricing.
        
        Args:
            component: VPC component (NatGateway, VPN, etc.)
            region: AWS region location
            
        Returns:
            List of pricing information for VPC components
        """
        # Use bulk pricing if in fallback mode
        if self.use_bulk_pricing:
            return self.bulk_client.find_vpc_pricing(component, region, 1)
        
        # VPC NAT Gateway pricing
        if component == 'NatGateway':
            filters = [
                {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
                {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'NAT Gateway'}
            ]
        # VPN Connection pricing
        elif component == 'VPN':
            filters = [
                {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
                {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'VPN Connection'}
            ]
        else:
            filters = []
        
        return self.get_products('AmazonVPC', filters, max_results=10)
    
    def get_alb_pricing(self, region: str = 'US East (N. Virginia)') -> List[Dict]:
        """
        Get Application Load Balancer pricing.
        
        Args:
            region: AWS region location
            
        Returns:
            List of pricing information for ALB
        """
        # Use bulk pricing if in fallback mode
        if self.use_bulk_pricing:
            return self.bulk_client.find_alb_pricing(region, 1)
        
        filters = [
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
            {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'Load Balancer-Application'}
        ]
        
        return self.get_products('AWSELB', filters, max_results=10)
    
    def get_route53_pricing(self, component: str = 'HostedZone') -> List[Dict]:
        """
        Get Route53 pricing.
        
        Args:
            component: Route53 component (HostedZone, Queries, etc.)
            
        Returns:
            List of pricing information for Route53
        """
        # Use bulk pricing if in fallback mode
        if self.use_bulk_pricing:
            return self.bulk_client.find_route53_pricing(component, 1)
        
        if component == 'HostedZone':
            filters = [
                {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'DNS Zone'}
            ]
        elif component == 'Queries':
            filters = [
                {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'DNS Query'}
            ]
        else:
            filters = []
        
        return self.get_products('AmazonRoute53', filters, max_results=10)
    
    def format_s3_pricing_data(self, products: List[Dict], storage_gb: float = 0) -> List[Dict]:
        """
        Format S3 pricing data.
        
        Args:
            products: List of raw S3 product data (AWS API or bulk pricing format)
            storage_gb: Storage size in GB for cost calculation
            
        Returns:
            List of formatted S3 pricing information
        """
        if not products:
            return []
        
        formatted_results = []
        
        for product in products:
            try:
                # Check if this is bulk pricing format (has 'service' field)
                if product.get('service') == 'S3':
                    # Bulk pricing format - just update the storage GB and monthly cost
                    if product.get('prices') and len(product['prices']) > 0:
                        price_per_gb = float(product['prices'][0]['amount'])
                        product['storageGB'] = storage_gb
                        product['prices'][0]['monthly_cost'] = price_per_gb * storage_gb
                    formatted_results.append(product)
                    continue
                
                # AWS API format
                product_attrs = product.get('product', {}).get('attributes', {})
                terms = product.get('terms', {})
                on_demand = terms.get('OnDemand', {})
                
                pricing_info = {
                    'service': 'S3',
                    'storageClass': product_attrs.get('storageClass', 'N/A'),
                    'location': product_attrs.get('location', 'N/A'),
                    'volumeType': product_attrs.get('volumeType', 'N/A'),
                    'storageGB': storage_gb,
                    'prices': []
                }
                
                for offer_term in on_demand.values():
                    for price_dimension in offer_term.get('priceDimensions', {}).values():
                        price_per_unit = float(price_dimension.get('pricePerUnit', {}).get('USD', 0))
                        unit = price_dimension.get('unit', 'N/A')
                        
                        # Calculate monthly cost based on storage size
                        monthly_cost = price_per_unit * storage_gb if storage_gb > 0 else 0
                        
                        pricing_info['prices'].append({
                            'amount': price_per_unit,
                            'monthly_cost': monthly_cost,
                            'unit': unit
                        })
                
                formatted_results.append(pricing_info)
            except Exception:
                continue
        
        return formatted_results
    
    def format_single_price(self, products: List[Dict], service_name: str, quantity: int = 1) -> List[Dict]:
        """
        Format pricing data for services with simple hourly/monthly costs.
        
        Args:
            products: List of raw product data (AWS API or bulk pricing format)
            service_name: Name of the service
            quantity: Number of units (e.g., NAT Gateways, Hosted Zones)
            
        Returns:
            List of formatted pricing information
        """
        if not products:
            return []
        
        formatted_results = []
        
        for product in products:
            try:
                # Check if this is already bulk pricing format
                if product.get('service') in ['VPC', 'ALB', 'Route53']:
                    # Already formatted by bulk pricing, just update quantity if needed
                    if product.get('prices') and len(product['prices']) > 0:
                        # Recalculate monthly_cost with actual quantity
                        amount = float(product['prices'][0].get('amount', 0))
                        unit = product['prices'][0].get('unit', 'Hrs')
                        if 'Hrs' in unit:
                            product['prices'][0]['monthly_cost'] = amount * 730 * quantity
                        else:
                            product['prices'][0]['monthly_cost'] = amount * quantity
                        product['quantity'] = quantity
                    formatted_results.append(product)
                    continue
                
                # AWS API format
                product_attrs = product.get('product', {}).get('attributes', {})
                terms = product.get('terms', {})
                on_demand = terms.get('OnDemand', {})
                
                pricing_info = {
                    'service': service_name,
                    'description': product_attrs.get('usagetype', 'N/A'),
                    'location': product_attrs.get('location', 'N/A'),
                    'productFamily': product_attrs.get('productFamily', 'N/A'),
                    'quantity': quantity,
                    'prices': []
                }
                
                for offer_term in on_demand.values():
                    for price_dimension in offer_term.get('priceDimensions', {}).values():
                        price_per_unit = float(price_dimension.get('pricePerUnit', {}).get('USD', 0))
                        unit = price_dimension.get('unit', 'N/A')
                        description = price_dimension.get('description', 'N/A')
                        
                        # Calculate total cost based on quantity
                        # If unit is 'Hrs', calculate monthly (730 hours)
                        if 'Hrs' in unit:
                            monthly_cost = price_per_unit * 730 * quantity
                        else:
                            monthly_cost = price_per_unit * quantity
                        
                        pricing_info['prices'].append({
                            'amount': price_per_unit,
                            'monthly_cost': monthly_cost,
                            'unit': unit,
                            'description': description
                        })
                
                formatted_results.append(pricing_info)
            except Exception:
                continue
        
        return formatted_results


def test_connection():
    """Test AWS Pricing API connection"""
    try:
        client = AWSPricingClient()
        services = client.get_services()
        return True, f"Successfully connected. Found {len(services)} services."
    except Exception as e:
        return False, str(e)


if __name__ == "__main__":
    # Test the connection
    success, message = test_connection()
    print(f"Connection test: {message}")
