"""
Report Generator for AWS Pricing Calculator

Generates professional, readable cost reports in CSV format.
"""

import csv
import io
from datetime import datetime
from typing import List, Dict


def generate_csv_report(cart_items: List[Dict], total_cost: float) -> str:
    """
    Generate a professional CSV report from cart items.
    
    Args:
        cart_items: List of cart items with pricing data
        total_cost: Total monthly cost
        
    Returns:
        CSV content as string with proper formatting
    """
    output = io.StringIO()
    writer = csv.writer(output)
    
    # ==================== HEADER SECTION ====================
    writer.writerow(['AWS COST ESTIMATE REPORT'])
    writer.writerow(['Generated', datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    writer.writerow(['Total Resources', len(cart_items)])
    writer.writerow([])
    
    # ==================== RESOURCE DETAILS ====================
    writer.writerow(['RESOURCE BREAKDOWN'])
    writer.writerow([])
    
    # Column headers with clear separation
    writer.writerow([
        'Service',
        'Resource',
        'Specifications',
        'Region',
        'Qty',
        'Hourly Rate',
        'Monthly Cost',
        'Annual Cost'
    ])
    
    # Separator row
    writer.writerow(['-' * 15, '-' * 20, '-' * 40, '-' * 25, '-' * 5, '-' * 12, '-' * 15, '-' * 15])
    
    # Cart items with clear formatting
    annual_total = 0
    for item in cart_items:
        service = item.get('service', 'N/A')
        resource_type = item.get('resourceType', 'N/A')
        specs = item.get('specifications', 'N/A')
        region = item.get('region', 'N/A')
        quantity = item.get('quantity', 1)
        hourly_cost = item.get('hourlyCost', 0)
        monthly_cost = item.get('monthlyCost', 0)
        annual_cost = monthly_cost * 12
        annual_total += annual_cost
        
        writer.writerow([
            service,
            resource_type,
            specs,
            region,
            quantity,
            f'${hourly_cost:.4f}/hr',
            f'${monthly_cost:,.2f}',
            f'${annual_cost:,.2f}'
        ])
    
    writer.writerow([])
    
    # ==================== COST SUMMARY ====================
    writer.writerow(['COST SUMMARY'])
    writer.writerow([])
    writer.writerow(['Period', 'Total Cost'])
    writer.writerow(['-' * 20, '-' * 20])
    writer.writerow(['Monthly', f'${total_cost:,.2f}'])
    writer.writerow(['Annual', f'${total_cost * 12:,.2f}'])
    writer.writerow([])
    
    # ==================== BREAKDOWN BY SERVICE ====================
    writer.writerow(['COST BY SERVICE'])
    writer.writerow([])
    writer.writerow(['Service', 'Resources', 'Monthly Cost', 'Annual Cost'])
    writer.writerow(['-' * 15, '-' * 12, '-' * 15, '-' * 15])
    
    # Group by service
    service_costs = {}
    service_counts = {}
    for item in cart_items:
        service = item.get('service', 'N/A')
        monthly = item.get('monthlyCost', 0)
        
        if service not in service_costs:
            service_costs[service] = 0
            service_counts[service] = 0
        
        service_costs[service] += monthly
        service_counts[service] += 1
    
    # Write service breakdown
    for service in sorted(service_costs.keys()):
        monthly = service_costs[service]
        annual = monthly * 12
        count = service_counts[service]
        
        writer.writerow([
            service,
            count,
            f'${monthly:,.2f}',
            f'${annual:,.2f}'
        ])
    
    writer.writerow([])
    
    # ==================== BREAKDOWN BY REGION ====================
    writer.writerow(['COST BY REGION'])
    writer.writerow([])
    writer.writerow(['Region', 'Resources', 'Monthly Cost', 'Annual Cost'])
    writer.writerow(['-' * 30, '-' * 12, '-' * 15, '-' * 15])
    
    # Group by region
    region_costs = {}
    region_counts = {}
    for item in cart_items:
        region = item.get('region', 'N/A')
        monthly = item.get('monthlyCost', 0)
        
        if region not in region_costs:
            region_costs[region] = 0
            region_counts[region] = 0
        
        region_costs[region] += monthly
        region_counts[region] += 1
    
    # Write region breakdown
    for region in sorted(region_costs.keys()):
        monthly = region_costs[region]
        annual = monthly * 12
        count = region_counts[region]
        
        writer.writerow([
            region,
            count,
            f'${monthly:,.2f}',
            f'${annual:,.2f}'
        ])
    
    writer.writerow([])
    
    # ==================== IMPORTANT NOTES ====================
    writer.writerow(['IMPORTANT NOTES'])
    writer.writerow([])
    writer.writerow(['1. Pricing Basis', 'On-Demand pricing (no reservations or savings plans)'])
    writer.writerow(['2. Monthly Hours', '730 hours (365 days ÷ 12 months × 24 hours)'])
    writer.writerow(['3. Currency', 'USD (United States Dollars)'])
    writer.writerow(['4. Exclusions', 'Data transfer, requests, and additional service-specific charges'])
    writer.writerow(['5. Accuracy', 'Estimates based on official AWS pricing as of January 2026'])
    writer.writerow(['6. Actual Costs', 'May vary based on usage patterns, reserved instances, and volume discounts'])
    writer.writerow([])
    
    # ==================== FOOTER ====================
    writer.writerow(['Report generated by AWS Cost Calculator'])
    writer.writerow(['For the most accurate pricing, please consult the official AWS Pricing Calculator'])
    writer.writerow(['https://calculator.aws/'])
    
    return output.getvalue()


def format_cart_item_for_export(item: Dict) -> Dict:
    """
    Format a cart item for export with standardized fields.
    
    Args:
        item: Cart item dictionary
        
    Returns:
        Formatted item dictionary
    """
    return {
        'service': item.get('service', 'N/A'),
        'resourceType': item.get('resourceType', 'N/A'),
        'specifications': item.get('specifications', 'N/A'),
        'region': item.get('region', 'N/A'),
        'quantity': item.get('quantity', 1),
        'hourlyCost': item.get('hourlyCost', 0),
        'monthlyCost': item.get('monthlyCost', 0)
    }
