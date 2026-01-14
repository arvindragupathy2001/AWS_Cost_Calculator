"""
Flask AWS Pricing Calculator Web Application

A web application for querying AWS pricing information using the AWS Pricing API.
"""

from flask import Flask, render_template, request, jsonify, session, Response
from aws_pricing import AWSPricingClient
from report_generator import generate_csv_report
import os
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SESSION_TYPE'] = 'filesystem'

# Initialize AWS Pricing client
try:
    pricing_client = AWSPricingClient()
except Exception as e:
    print(f"Warning: Could not initialize AWS Pricing client: {e}")
    pricing_client = None


@app.route('/')
def index():
    """Render the main page"""
    # Initialize cart in session if it doesn't exist
    if 'cart' not in session:
        session['cart'] = []
    return render_template('index.html')


# ==================== Pricing Endpoints ====================

@app.route('/api/pricing/ec2', methods=['POST'])
def get_ec2_pricing():
    """Get EC2 pricing based on parameters"""
    try:
        if not pricing_client:
            return jsonify({'success': False, 'error': 'AWS Pricing client not initialized'}), 500
        
        data = request.get_json()
        products = pricing_client.get_ec2_pricing(
            instance_type=data.get('instanceType', 't2.micro'),
            region=data.get('region', 'US East (N. Virginia)'),
            operating_system=data.get('operatingSystem', 'Linux'),
            tenancy=data.get('tenancy', 'Shared')
        )
        
        # Bulk pricing client already returns formatted data
        if pricing_client.use_bulk_pricing:
            formatted_data = products
        else:
            formatted_data = pricing_client.format_pricing_data(products)
        
        return jsonify({'success': True, 'data': formatted_data, 'count': len(formatted_data)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/pricing/rds', methods=['POST'])
def get_rds_pricing():
    """Get RDS pricing based on parameters"""
    try:
        if not pricing_client:
            return jsonify({'success': False, 'error': 'AWS Pricing client not initialized'}), 500
        
        data = request.get_json()
        products = pricing_client.get_rds_pricing(
            instance_type=data.get('instanceType', 'db.t3.micro'),
            region=data.get('region', 'US East (N. Virginia)'),
            database_engine=data.get('databaseEngine', 'MySQL'),
            deployment_option=data.get('deploymentOption', 'Single-AZ')
        )
        
        # Bulk pricing client already returns formatted data
        if pricing_client.use_bulk_pricing:
            formatted_data = products
        else:
            formatted_data = pricing_client.format_pricing_data(products)
        
        return jsonify({'success': True, 'data': formatted_data, 'count': len(formatted_data)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/pricing/s3', methods=['POST'])
def get_s3_pricing():
    """Get S3 pricing based on parameters"""
    try:
        if not pricing_client:
            return jsonify({'success': False, 'error': 'AWS Pricing client not initialized'}), 500
        
        data = request.get_json()
        storage_gb = float(data.get('storageGB', 0))
        
        products = pricing_client.get_s3_pricing(
            storage_class=data.get('storageClass', 'General Purpose'),
            region=data.get('region', 'US East (N. Virginia)')
        )
        
        formatted_data = pricing_client.format_s3_pricing_data(products, storage_gb)
        return jsonify({'success': True, 'data': formatted_data, 'count': len(formatted_data)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/pricing/vpc', methods=['POST'])
def get_vpc_pricing():
    """Get VPC pricing based on parameters"""
    try:
        if not pricing_client:
            return jsonify({'success': False, 'error': 'AWS Pricing client not initialized'}), 500
        
        data = request.get_json()
        quantity = int(data.get('quantity', 1))
        
        products = pricing_client.get_vpc_pricing(
            component=data.get('component', 'NatGateway'),
            region=data.get('region', 'US East (N. Virginia)')
        )
        
        formatted_data = pricing_client.format_single_price(products, 'VPC', quantity)
        return jsonify({'success': True, 'data': formatted_data, 'count': len(formatted_data)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/pricing/alb', methods=['POST'])
def get_alb_pricing():
    """Get ALB pricing based on parameters"""
    try:
        if not pricing_client:
            return jsonify({'success': False, 'error': 'AWS Pricing client not initialized'}), 500
        
        data = request.get_json()
        quantity = int(data.get('quantity', 1))
        
        products = pricing_client.get_alb_pricing(
            region=data.get('region', 'US East (N. Virginia)')
        )
        
        formatted_data = pricing_client.format_single_price(products, 'ALB', quantity)
        return jsonify({'success': True, 'data': formatted_data, 'count': len(formatted_data)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/pricing/route53', methods=['POST'])
def get_route53_pricing():
    """Get Route53 pricing based on parameters"""
    try:
        if not pricing_client:
            return jsonify({'success': False, 'error': 'AWS Pricing client not initialized'}), 500
        
        data = request.get_json()
        quantity = int(data.get('quantity', 1))
        
        products = pricing_client.get_route53_pricing(
            component=data.get('component', 'HostedZone')
        )
        
        formatted_data = pricing_client.format_single_price(products, 'Route53', quantity)
        return jsonify({'success': True, 'data': formatted_data, 'count': len(formatted_data)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Cart Endpoints ====================

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    try:
        data = request.get_json()
        
        if 'cart' not in session:
            session['cart'] = []
        
        # Create cart item with unique ID
        cart_item = {
            'id': str(uuid.uuid4()),
            'service': data.get('service'),
            'resourceType': data.get('resourceType'),
            'specifications': data.get('specifications'),
            'region': data.get('region'),
            'quantity': data.get('quantity', 1),
            'hourlyCost': float(data.get('hourlyCost', 0)),
            'monthlyCost': float(data.get('monthlyCost', 0))
        }
        
        session['cart'].append(cart_item)
        session.modified = True
        
        return jsonify({
            'success': True,
            'message': 'Item added to cart',
            'cartCount': len(session['cart'])
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/cart/items', methods=['GET'])
def get_cart_items():
    """Get all cart items"""
    try:
        if 'cart' not in session:
            session['cart'] = []
        
        return jsonify({
            'success': True,
            'items': session['cart'],
            'count': len(session['cart'])
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/cart/remove/<item_id>', methods=['DELETE'])
def remove_from_cart(item_id):
    """Remove item from cart"""
    try:
        if 'cart' not in session:
            session['cart'] = []
        
        session['cart'] = [item for item in session['cart'] if item['id'] != item_id]
        session.modified = True
        
        return jsonify({
            'success': True,
            'message': 'Item removed from cart',
            'cartCount': len(session['cart'])
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/cart/clear', methods=['DELETE'])
def clear_cart():
    """Clear all items from cart"""
    try:
        session['cart'] = []
        session.modified = True
        
        return jsonify({
            'success': True,
            'message': 'Cart cleared'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/cart/total', methods=['GET'])
def get_cart_total():
    """Get total cost of cart items"""
    try:
        if 'cart' not in session:
            session['cart'] = []
        
        total = sum(item.get('monthlyCost', 0) for item in session['cart'])
        
        return jsonify({
            'success': True,
            'total': round(total, 2),
            'count': len(session['cart'])
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Export Endpoints ====================

@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    """Export cart items as CSV"""
    try:
        if 'cart' not in session:
            session['cart'] = []
        
        total = sum(item.get('monthlyCost', 0) for item in session['cart'])
        csv_content = generate_csv_report(session['cart'], total)
        
        return Response(
            csv_content,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=aws_cost_estimate.csv'}
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Utility Endpoints ====================

@app.route('/api/test-connection', methods=['GET'])
def test_connection():
    """Test AWS Pricing API connection"""
    try:
        if not pricing_client:
            return jsonify({'success': False, 'error': 'Pricing client not initialized'})
        
        # If using bulk pricing, it's always "connected"
        if pricing_client.use_bulk_pricing:
            return jsonify({'success': True, 'message': 'Using credential-free pricing'})
        
        # Test actual AWS connection
        pricing_client.get_services()
        return jsonify({'success': True, 'message': 'Connected to AWS Pricing API'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/available-instances', methods=['GET'])
def get_available_instances():
    """Get all available EC2 instance types for the current region"""
    try:
        region = request.args.get('region', 'US East (N. Virginia)')
        
        if pricing_client and pricing_client.use_bulk_pricing:
            # Get instance types from bulk pricing data
            ec2_data = pricing_client.bulk_client.pricing_data.get('EC2', {})
            region_data = ec2_data.get(region, {})
            instances = sorted(list(region_data.keys()))
            
            return jsonify({
                'success': True,
                'instances': instances,
                'count': len(instances),
                'region': region
            })
        else:
            # Return a basic list if using AWS API
            return jsonify({
                'success': True,
                'instances': ['t2.micro', 't3.micro', 'm5.large'],  # Basic fallback
                'count': 3
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'success': False, 'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    print(f"\n{'='*60}")
    print("🚀 AWS Pricing Calculator")
    print(f"{'='*60}")
    print(f"Server running on http://localhost:{port}")
    print(f"Debug mode: {debug}")
    print(f"{'='*60}\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
