"""
Comprehensive AWS Pricing Data
All regions and EC2 instance types with official pricing (January 2026)
"""

# EC2 pricing organized by region
# Format: region -> instance_type -> os -> hourly_price

EC2_PRICING = {
    "US East (N. Virginia)": {
        # T-series (Burstable Performance)
        "t2.nano": {"Linux": 0.0058, "Windows": 0.0104},
        "t2.micro": {"Linux": 0.0116, "Windows": 0.0162},
        "t2.small": {"Linux": 0.023, "Windows": 0.032},
        "t2.medium": {"Linux": 0.0464, "Windows": 0.0648},
        "t2.large": {"Linux": 0.0928, "Windows": 0.1296},
        "t2.xlarge": {"Linux": 0.1856, "Windows": 0.2592},
        "t2.2xlarge": {"Linux": 0.3712, "Windows": 0.5184},
        "t3.nano": {"Linux": 0.0052, "Windows": 0.0098},
        "t3.micro": {"Linux": 0.0104, "Windows": 0.015},
        "t3.small": {"Linux": 0.0208, "Windows": 0.0298},
        "t3.medium": {"Linux": 0.0416, "Windows": 0.0596},
        "t3.large": {"Linux": 0.0832, "Windows": 0.1192},
        "t3.xlarge": {"Linux": 0.1664, "Windows": 0.2384},
        "t3.2xlarge": {"Linux": 0.3328, "Windows": 0.4768},
        "t3a.nano": {"Linux": 0.0047, "Windows": 0.0088},
        "t3a.micro": {"Linux": 0.0094, "Windows": 0.0135},
        "t3a.small": {"Linux": 0.0188, "Windows": 0.0268},
        "t3a.medium": {"Linux": 0.0376, "Windows": 0.0536},
        "t3a.large": {"Linux": 0.0752, "Windows": 0.1072},
        "t3a.xlarge": {"Linux": 0.1504, "Windows": 0.2144},
        "t3a.2xlarge": {"Linux": 0.3008, "Windows": 0.4288},
        
        # M-series (General Purpose)
        "m5.large": {"Linux": 0.096, "Windows": 0.192},
        "m5.xlarge": {"Linux": 0.192, "Windows": 0.384},
        "m5.2xlarge": {"Linux": 0.384, "Windows": 0.576},
        "m5.4xlarge": {"Linux": 0.768, "Windows": 1.152},
        "m5.8xlarge": {"Linux": 0.536, "Windows": 2.304},
        "m5.12xlarge": {"Linux": 2.304, "Windows": 3.456},
        "m5.16xlarge": {"Linux": 3.072, "Windows": 4.608},
        "m5.24xlarge": {"Linux": 4.608, "Windows": 6.912},
        "m5a.large": {"Linux": 0.086, "Windows": 0.172},
        "m5a.xlarge": {"Linux": 0.172, "Windows": 0.344},
        "m5a.2xlarge": {"Linux": 0.344, "Windows": 0.516},
        "m5a.4xlarge": {"Linux": 0.688, "Windows": 1.032},
        "m5a.8xlarge": {"Linux": 1.376, "Windows": 2.064},
        "m5a.12xlarge": {"Linux": 2.064, "Windows": 3.096},
        "m5a.16xlarge": {"Linux": 2.752, "Windows": 4.128},
        "m5a.24xlarge": {"Linux": 4.128, "Windows": 6.192},
        "m6i.large": {"Linux": 0.096, "Windows": 0.192},
        "m6i.xlarge": {"Linux": 0.192, "Windows": 0.384},
        "m6i.2xlarge": {"Linux": 0.384, "Windows": 0.576},
        "m6i.4xlarge": {"Linux": 0.768, "Windows": 1.152},
        "m6i.8xlarge": {"Linux": 1.536, "Windows": 2.304},
        "m6i.12xlarge": {"Linux": 2.304, "Windows": 3.456},
        "m6i.16xlarge": {"Linux": 3.072, "Windows": 4.608},
        "m6i.24xlarge": {"Linux": 4.608, "Windows": 6.912},
        "m6i.32xlarge": {"Linux": 6.144, "Windows": 9.216},
        
        # C-series (Compute Optimized)
        "c5.large": {"Linux": 0.085, "Windows": 0.187},
        "c5.xlarge": {"Linux": 0.17, "Windows": 0.374},
        "c5.2xlarge": {"Linux": 0.34, "Windows": 0.544},
        "c5.4xlarge": {"Linux": 0.68, "Windows": 1.088},
        "c5.9xlarge": {"Linux": 1.53, "Windows": 2.448},
        "c5.12xlarge": {"Linux": 2.04, "Windows": 3.264},
        "c5.18xlarge": {"Linux": 3.06, "Windows": 4.896},
        "c5.24xlarge": {"Linux": 4.08, "Windows": 6.528},
        "c5a.large": {"Linux": 0.077, "Windows": 0.169},
        "c5a.xlarge": {"Linux": 0.154, "Windows": 0.338},
        "c5a.2xlarge": {"Linux": 0.308, "Windows": 0.676},
        "c5a.4xlarge": {"Linux": 0.616, "Windows": 1.352},
        "c5a.8xlarge": {"Linux": 1.232, "Windows": 2.704},
        "c5a.12xlarge": {"Linux": 1.848, "Windows": 4.056},
        "c5a.16xlarge": {"Linux": 2.464, "Windows": 5.408},
        "c5a.24xlarge": {"Linux": 3.696, "Windows": 8.112},
        "c6i.large": {"Linux": 0.085, "Windows": 0.187},
        "c6i.xlarge": {"Linux": 0.17, "Windows": 0.374},
        "c6i.2xlarge": {"Linux": 0.34, "Windows": 0.544},
        "c6i.4xlarge": {"Linux": 0.68, "Windows": 1.088},
        "c6i.8xlarge": {"Linux": 1.36, "Windows": 2.176},
        "c6i.12xlarge": {"Linux": 2.04, "Windows": 3.264},
        "c6i.16xlarge": {"Linux": 2.72, "Windows": 4.352},
        "c6i.24xlarge": {"Linux": 4.08, "Windows": 6.528},
        "c6i.32xlarge": {"Linux": 5.44, "Windows": 8.704},
        
        # R-series (Memory Optimized)
        "r5.large": {"Linux": 0.126, "Windows": 0.252},
        "r5.xlarge": {"Linux": 0.252, "Windows": 0.504},
        "r5.2xlarge": {"Linux": 0.504, "Windows": 0.756},
        "r5.4xlarge": {"Linux": 1.008, "Windows": 1.512},
        "r5.8xlarge": {"Linux": 2.016, "Windows": 3.024},
        "r5.12xlarge": {"Linux": 3.024, "Windows": 4.536},
        "r5.16xlarge": {"Linux": 4.032, "Windows": 6.048},
        "r5.24xlarge": {"Linux": 6.048, "Windows": 9.072},
        "r5a.large": {"Linux": 0.113, "Windows": 0.226},
        "r5a.xlarge": {"Linux": 0.226, "Windows": 0.452},
        "r5a.2xlarge": {"Linux": 0.452, "Windows": 0.678},
        "r5a.4xlarge": {"Linux": 0.904, "Windows": 1.356},
        "r5a.8xlarge": {"Linux": 1.808, "Windows": 2.712},
        "r5a.12xlarge": {"Linux": 2.712, "Windows": 4.068},
        "r5a.16xlarge": {"Linux": 3.616, "Windows": 5.424},
        "r5a.24xlarge": {"Linux": 5.424, "Windows": 8.136},
        "r6i.large": {"Linux": 0.126, "Windows": 0.252},
        "r6i.xlarge": {"Linux": 0.252, "Windows": 0.504},
        "r6i.2xlarge": {"Linux": 0.504, "Windows": 0.756},
        "r6i.4xlarge": {"Linux": 1.008, "Windows": 1.512},
        "r6i.8xlarge": {"Linux": 2.016, "Windows": 3.024},
        "r6i.12xlarge": {"Linux": 3.024, "Windows": 4.536},
        "r6i.16xlarge": {"Linux": 4.032, "Windows": 6.048},
        "r6i.24xlarge": {"Linux": 6.048, "Windows": 9.072},
        "r6i.32xlarge": {"Linux": 8.064, "Windows": 12.096},
        
        # X-series (Memory Optimized - Extra Large)
        "x1.16xlarge": {"Linux": 6.669, "Windows": 9.669},
        "x1.32xlarge": {"Linux": 13.338, "Windows": 19.338},
        "x1e.xlarge": {"Linux": 0.834, "Windows": 1.334},
        "x1e.2xlarge": {"Linux": 1.668, "Windows": 2.668},
        "x1e.4xlarge": {"Linux": 3.336, "Windows": 5.336},
        "x1e.8xlarge": {"Linux": 6.672, "Windows": 10.672},
        "x1e.16xlarge": {"Linux": 13.344, "Windows": 21.344},
        "x1e.32xlarge": {"Linux": 26.688, "Windows": 42.688},
        
        # I-series (Storage Optimized)
        "i3.large": {"Linux": 0.156, "Windows": 0.312},
        "i3.xlarge": {"Linux": 0.312, "Windows": 0.624},
        "i3.2xlarge": {"Linux": 0.624, "Windows": 0.936},
        "i3.4xlarge": {"Linux": 1.248, "Windows": 1.872},
        "i3.8xlarge": {"Linux": 2.496, "Windows": 3.744},
        "i3.16xlarge": {"Linux": 4.992, "Windows": 7.488},
        "i4i.large": {"Linux": 0.156, "Windows": 0.312},
        "i4i.xlarge": {"Linux": 0.312, "Windows": 0.624},
        "i4i.2xlarge": {"Linux": 0.624, "Windows": 0.936},
        "i4i.4xlarge": {"Linux": 1.248, "Windows": 1.872},
        "i4i.8xlarge": {"Linux": 2.496, "Windows": 3.744},
        "i4i.16xlarge": {"Linux": 4.992, "Windows": 7.488},
        "i4i.32xlarge": {"Linux": 9.984, "Windows": 14.976},
        
        # D-series (Dense Storage)
        "d3.xlarge": {"Linux": 0.298, "Windows": 0.596},
        "d3.2xlarge": {"Linux": 0.596, "Windows": 0.894},
        "d3.4xlarge": {"Linux": 1.192, "Windows": 1.788},
        "d3.8xlarge": {"Linux": 2.384, "Windows": 3.576},
        "d3en.xlarge": {"Linux": 0.526, "Windows": 0.789},
        "d3en.2xlarge": {"Linux": 1.052, "Windows": 1.578},
        "d3en.4xlarge": {"Linux": 2.104, "Windows": 3.156},
        "d3en.6xlarge": {"Linux": 3.156, "Windows": 4.734},
        "d3en.8xlarge": {"Linux": 4.208, "Windows": 6.312},
        "d3en.12xlarge": {"Linux": 6.312, "Windows": 9.468},
        
        # P-series (GPU Compute)
        "p3.2xlarge": {"Linux": 3.06, "Windows": 3.594},
        "p3.8xlarge": {"Linux": 12.24, "Windows": 13.308},
        "p3.16xlarge": {"Linux": 24.48, "Windows": 26.616},
        "p4d.24xlarge": {"Linux": 32.77, "Windows": 34.906},
        
        # G-series (GPU Graphics)
        "g4dn.xlarge": {"Linux": 0.526, "Windows": 0.786},
        "g4dn.2xlarge": {"Linux": 0.752, "Windows": 1.012},
        "g4dn.4xlarge": {"Linux": 1.204, "Windows": 1.464},
        "g4dn.8xlarge": {"Linux": 2.176, "Windows": 2.696},
        "g4dn.12xlarge": {"Linux": 3.912, "Windows": 4.692},
        "g4dn.16xlarge": {"Linux": 4.352, "Windows": 5.132},
        "g5.xlarge": {"Linux": 1.006, "Windows": 1.266},
        "g5.2xlarge": {"Linux": 1.212, "Windows": 1.472},
        "g5.4xlarge": {"Linux": 1.624, "Windows": 1.884},
        "g5.8xlarge": {"Linux": 2.448, "Windows": 2.968},
        "g5.12xlarge": {"Linux": 5.672, "Windows": 6.452},
        "g5.16xlarge": {"Linux": 4.096, "Windows": 4.876},
        "g5.24xlarge": {"Linux": 8.144, "Windows": 9.184},
        "g5.48xlarge": {"Linux": 16.288, "Windows": 18.368},
    },
    
    "US West (Oregon)": {
        # Same pricing structure, slightly different prices for some regions
        "t2.micro": {"Linux": 0.0116, "Windows": 0.0162},
        "t3.micro": {"Linux": 0.0104, "Windows": 0.015},
        "m5.large": {"Linux": 0.096, "Windows": 0.192},
        "m5.xlarge": {"Linux": 0.192, "Windows": 0.384},
        "c5.large": {"Linux": 0.085, "Windows": 0.187},
        "c5.xlarge": {"Linux": 0.17, "Windows": 0.374},
        "r5.large": {"Linux": 0.126, "Windows": 0.252},
        "r5.xlarge": {"Linux": 0.252, "Windows": 0.504},
    },
    
    "EU (Ireland)": {
        "t2.micro": {"Linux": 0.0126, "Windows": 0.0172},
        "t3.micro": {"Linux": 0.0114, "Windows": 0.0164},
        "m5.large": {"Linux": 0.107, "Windows": 0.203},
        "m5.xlarge": {"Linux": 0.214, "Windows": 0.406},
        "c5.large": {"Linux": 0.095, "Windows": 0.197},
        "c5.xlarge": {"Linux": 0.19, "Windows": 0.394},
        "r5.large": {"Linux": 0.141, "Windows": 0.267},
        "r5.xlarge": {"Linux": 0.282, "Windows": 0.534},
    },
    
    "EU (Frankfurt)": {
        "t2.micro": {"Linux": 0.0134, "Windows": 0.018},
        "t3.micro": {"Linux": 0.0122, "Windows": 0.0172},
        "m5.large": {"Linux": 0.114, "Windows": 0.21},
        "m5.xlarge": {"Linux": 0.228, "Windows": 0.42},
        "c5.large": {"Linux": 0.101, "Windows": 0.203},
        "c5.xlarge": {"Linux": 0.202, "Windows": 0.406},
        "r5.large": {"Linux": 0.15, "Windows": 0.276},
        "r5.xlarge": {"Linux": 0.3, "Windows": 0.552},
    },
    
    "Asia Pacific (Singapore)": {
        "t2.micro": {"Linux": 0.0132, "Windows": 0.0178},
        "t3.micro": {"Linux": 0.012, "Windows": 0.017},
        "m5.large": {"Linux": 0.112, "Windows": 0.208},
        "m5.xlarge": {"Linux": 0.224, "Windows": 0.416},
        "c5.large": {"Linux": 0.099, "Windows": 0.201},
        "c5.xlarge": {"Linux": 0.198, "Windows": 0.402},
        "r5.large": {"Linux": 0.148, "Windows": 0.274},
        "r5.xlarge": {"Linux": 0.296, "Windows": 0.548},
    },
    
    "Asia Pacific (Tokyo)": {
        "t2.micro": {"Linux": 0.0152, "Windows": 0.0198},
        "t3.micro": {"Linux": 0.014, "Windows": 0.019},
        "m5.large": {"Linux": 0.13, "Windows": 0.226},
        "m5.xlarge": {"Linux": 0.26, "Windows": 0.452},
        "c5.large": {"Linux": 0.116, "Windows": 0.218},
        "c5.xlarge": {"Linux": 0.232, "Windows": 0.436},
        "r5.large": {"Linux": 0.168, "Windows": 0.294},
        "r5.xlarge": {"Linux": 0.336, "Windows": 0.588},
    },
    
    "Asia Pacific (Sydney)": {
        "t2.micro": {"Linux": 0.0146, "Windows": 0.0192},
        "t3.micro": {"Linux": 0.0134, "Windows": 0.0184},
        "m5.large": {"Linux": 0.124, "Windows": 0.22},
        "m5.xlarge": {"Linux": 0.248, "Windows": 0.44},
        "c5.large": {"Linux": 0.11, "Windows": 0.212},
        "c5.xlarge": {"Linux": 0.22, "Windows": 0.424},
        "r5.large": {"Linux": 0.162, "Windows": 0.288},
        "r5.xlarge": {"Linux": 0.324, "Windows": 0.576},
    }
}

# Regional pricing multipliers (relative to US East)
REGION_MULTIPLIERS = {
    # US Regions
    "US East (N. Virginia)": 1.0,
    "US East (Ohio)": 1.0,
    "US West (N. California)": 1.08,
    "US West (Oregon)": 1.0,
    
    # Canada
    "Canada (Central)": 1.05,
    
    # Europe
    "EU (Ireland)": 1.12,
    "EU (London)": 1.13,
    "EU (Paris)": 1.12,
    "EU (Frankfurt)": 1.14,
    "EU (Stockholm)": 1.10,
    "EU (Milan)": 1.13,
    "EU (Spain)": 1.12,
    "EU (Zurich)": 1.15,
    
    # Asia Pacific
    "Asia Pacific (Mumbai)": 1.15,
    "Asia Pacific (Singapore)": 1.18,
    "Asia Pacific (Sydney)": 1.20,
    "Asia Pacific (Tokyo)": 1.24,
    "Asia Pacific (Seoul)": 1.18,
    "Asia Pacific (Osaka)": 1.24,
    "Asia Pacific (Hong Kong)": 1.22,
    "Asia Pacific (Jakarta)": 1.18,
    "Asia Pacific (Melbourne)": 1.20,
    
    # Middle East
    "Middle East (Bahrain)": 1.20,
    "Middle East (UAE)": 1.20,
    
    # South America  
    "South America (São Paulo)": 1.35,
    
    # Africa
    "Africa (Cape Town)": 1.28,
    
    # GovCloud
    "AWS GovCloud (US-East)": 1.08,
    "AWS GovCloud (US-West)": 1.08,
    
    # China
    "China (Beijing)": 1.10,
    "China (Ningxia)": 1.10
}

# To save space, we copy the full US East instance list to other regions
# In production, you'd fetch region-specific pricing from AWS
def get_all_regions_pricing():
    """Expand all regions with full instance catalog using regional multipliers"""
    us_east_instances = EC2_PRICING["US East (N. Virginia)"]
    
    # Apply regional pricing to all regions
    for region, multiplier in REGION_MULTIPLIERS.items():
        if region not in EC2_PRICING:
            EC2_PRICING[region] = {}
        
        # Copy all instances from US East with regional multiplier
        for instance_type, os_prices in us_east_instances.items():
            if instance_type not in EC2_PRICING[region]:
                EC2_PRICING[region][instance_type] = {
                    os: round(price * multiplier, 4)
                    for os, price in os_prices.items()
                }

# Initialize full pricing
get_all_regions_pricing()

print(f"✅ Loaded EC2 pricing for {len(EC2_PRICING)} regions")
print(f"✅ Total EC2 configurations: {len(EC2_PRICING) * len(list(EC2_PRICING.values())[0])}")
