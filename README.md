# AWS Pricing Calculator

A modern Flask web application for querying real-time AWS pricing information using the AWS Pricing API.

![AWS Pricing Calculator](https://img.shields.io/badge/Flask-3.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![AWS](https://img.shields.io/badge/AWS-boto3-orange)

## Features

- 🚀 **Real-time AWS Pricing**: Query live pricing data directly from AWS
- 💻 **Multiple Services**: Support for EC2, RDS, S3, VPC, ALB, Route53
- 🛒 **Shopping Cart**: Add multiple resources and calculate total costs
- 📊 **Cost Reports**: Download detailed CSV reports
- 🎨 **Modern UI**: Beautiful glassmorphism design with dark theme
- ⚡ **Fast & Responsive**: Smooth animations and dynamic content loading
- 🔓 **Credential-Free Mode**: Works without AWS credentials using public pricing data

## Supported AWS Services

- **Amazon EC2**: Elastic Compute Cloud instances
- **Amazon RDS**: Relational Database Service instances
- **Amazon S3**: Simple Storage Service
- **Amazon VPC**: NAT Gateway, VPN connections
- **Application Load Balancer**: ALB pricing
- **Amazon Route53**: DNS hosting and queries

## Prerequisites

- Python 3.8 or higher
- **Optional**: AWS credentials (app works without them using public pricing data)

## Installation

1. **Clone or navigate to the project directory**:
   ```powershell
   cd "c:\Users\ArvindRagupathy\Desktop\Cost calculator"
   ```

2. **Install required dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Configure AWS credentials** (Optional):
   
   > [!NOTE]
   > **AWS credentials are optional!** The app automatically uses public AWS pricing data if credentials are not configured. However, using credentials may provide faster responses for some queries.
   
   If you want to use AWS API with credentials:
   
   Copy the example environment file:
   ```powershell
   copy .env.example .env
   ```
   
   Edit `.env` and add your AWS credentials:
   ```
   AWS_ACCESS_KEY_ID=your_access_key_here
   AWS_SECRET_ACCESS_KEY=your_secret_key_here
   AWS_DEFAULT_REGION=us-east-1
   ```

   **Alternative**: You can also configure AWS credentials using AWS CLI:
   ```powershell
   aws configure
   ```

## Credential-Free Mode

The app automatically detects if AWS credentials are available. If not, it falls back to using **AWS's public bulk pricing files**.

**How it works:**
- On first run without credentials, the app downloads pricing data from AWS's public endpoints
- Pricing data is cached locally in `pricing_cache/` directory
- Cache is refreshed automatically after 7 days
- **Note**: Initial download may take a few minutes for each service (files are 100MB+)

**Advantages:**
- ✅ No AWS account required
- ✅ No credential management
- ✅ Pricing data cached locally for fast access

**Trade-offs:**
- ⏱️ First-time download for each service takes time
- 💾 Requires ~500MB disk space for cache
- 📅 Pricing refreshes weekly (vs. real-time with API)

## Running the Application

Start the Flask development server:

```powershell
python app.py
```

The application will be available at: **http://localhost:5000**

You should see output similar to:
```
============================================================
🚀 AWS Pricing Calculator
============================================================
Server running on http://localhost:5000
Debug mode: True
============================================================
```

## Usage

1. **Open your browser** and navigate to `http://localhost:5000`

2. **Check Connection Status**: The header will show whether the app is connected to AWS (green dot = connected)

3. **Select AWS Service**: Choose between EC2 or RDS from the dropdown

4. **Configure Parameters**:
   - For **EC2**: Select instance type, region, operating system, and tenancy
   - For **RDS**: Select instance type, region, database engine, and deployment option

5. **Query Pricing**: Click the "Get Pricing" button to retrieve pricing information

6. **View Results**: Pricing details will be displayed in cards showing:
   - Instance specifications (vCPU, memory, storage, network)
   - Hourly pricing in USD
   - Additional pricing details

## Project Structure

```
Cost calculator/
├── app.py                  # Main Flask application
├── aws_pricing.py          # AWS Pricing API wrapper
├── requirements.txt        # Python dependencies
├── .env.example           # Environment configuration template
├── .env                   # Your environment configuration (not in git)
├── static/
│   ├── css/
│   │   └── style.css     # Modern CSS styling
│   └── js/
│       └── main.js       # Client-side JavaScript
└── templates/
    └── index.html        # Main HTML template
```

## API Endpoints

- `GET /` - Main application page
- `GET /api/services` - List available AWS services
- `POST /api/pricing/ec2` - Get EC2 pricing
- `POST /api/pricing/rds` - Get RDS pricing
- `GET /api/test-connection` - Test AWS connection

## Troubleshooting

### Connection Issues

If you see "Not Connected" status:

1. **Verify AWS credentials** are correctly configured in `.env` or via AWS CLI
2. **Check IAM permissions**: Ensure your AWS user has `pricing:GetProducts` and `pricing:DescribeServices` permissions
3. **Network connectivity**: Ensure you can reach AWS APIs from your network

### No Pricing Data Returned

- Try different instance types or regions
- Some combinations may not have pricing data available
- Check the AWS Pricing API documentation for valid parameter combinations

### Module Import Errors

If you get import errors:
```powershell
pip install --upgrade -r requirements.txt
```

## AWS IAM Permissions

Your AWS credentials need the following permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "pricing:GetProducts",
                "pricing:DescribeServices"
            ],
            "Resource": "*"
        }
    ]
}
```

## Development

To run in development mode with auto-reload:

```powershell
$env:FLASK_ENV="development"
$env:FLASK_DEBUG="True"
python app.py
```

## Technologies Used

- **Backend**: Flask 3.0.0 (Python web framework)
- **AWS SDK**: boto3 (AWS API integration)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Design**: Custom glassmorphism UI with dark theme

## License

This project is open source and available for educational purposes.

## Support

For issues or questions:
- Check the AWS Pricing API documentation
- Review boto3 documentation
- Ensure AWS credentials are properly configured

---

**Built with ❤️ using Flask and AWS**
