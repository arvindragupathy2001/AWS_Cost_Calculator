// AWS Pricing Calculator - Main JavaScript with Cart Functionality

// Global state
let currentService = 'EC2';
let currentRegion = 'US East (N. Virginia)';
let cart = [];

// Service form templates
const SERVICE_FORMS = {
    EC2: `
        <div class="form-group">
            <label>Instance Type</label>
            <select id="ec2InstanceType">
                <option value="">Loading instances...</option>
            </select>
        </div>
        <div class="form-group">
            <label>Operating System</label>
            <select id="ec2OS">
                <option value="Linux">Linux</option>
                <option value="Windows">Windows</option>
                <option value="RHEL">Red Hat Enterprise Linux</option>
            </select>
        </div>
        <div class="form-group">
            <label>Quantity</label>
            <input type="number" id="ec2Quantity" value="1" min="1" max="100">
        </div>
    `,
    RDS: `
        <div class="form-group">
            <label>Instance Type</label>
            <select id="rdsInstanceType">
                <option value="db.t3.micro">db.t3.micro</option>
                <option value="db.t3.small">db.t3.small</option>
                <option value="db.t3.medium">db.t3.medium</option>
                <option value="db.m5.large">db.m5.large</option>
                <option value="db.r5.large">db.r5.large</option>
            </select>
        </div>
        <div class="form-group">
            <label>Database Engine</label>
            <select id="rdsEngine">
                <option value="MySQL">MySQL</option>
                <option value="PostgreSQL">PostgreSQL</option>
                <option value="MariaDB">MariaDB</option>
            </select>
        </div>
        <div class="form-group">
            <label>Deployment</label>
            <select id="rdsDeployment">
                <option value="Single-AZ">Single-AZ</option>
                <option value="Multi-AZ">Multi-AZ</option>
            </select>
        </div>
        <div class="form-group">
            <label>Quantity</label>
            <input type="number" id="rdsQuantity" value="1" min="1" max="100">
        </div>
    `,
    S3: `
        <div class="form-group">
            <label>Storage Class</label>
            <select id="s3StorageClass">
                <option value="General Purpose">S3 Standard</option>
                <option value="Infrequent Access">S3 Infrequent Access</option>
                <option value="Archive">S3 Glacier</option>
            </select>
        </div>
        <div class="form-group">
            <label>Storage Size (GB)</label>
            <input type="number" id="s3StorageGB" value="100" min="1" max="1000000" step="10">
        </div>
    `,
    VPC: `
        <div class="form-group">
            <label>Component Type</label>
            <select id="vpcComponent">
                <option value="NatGateway">NAT Gateway</option>
                <option value="VPN">VPN Connection</option>
            </select>
        </div>
        <div class="form-group">
            <label>Quantity</label>
            <input type="number" id="vpcQuantity" value="1" min="1" max="10">
        </div>
    `,
    ALB: `
        <div class="form-group">
            <label>Number of Load Balancers</label>
            <input type="number" id="albQuantity" value="1" min="1" max="20">
        </div>
        <div class="form-info">
            <small>💡 Additional LCU charges may apply based on traffic</small>
        </div>
    `,
    Route53: `
        <div class="form-group">
            <label>Component Type</label>
            <select id="route53Component">
                <option value="HostedZone">Hosted Zones</option>
                <option value="Queries">DNS Queries</option>
            </select>
        </div>
        <div class="form-group">
            <label>Quantity</label>
            <input type="number" id="route53Quantity" value="1" min="1" max="100">
        </div>
    `
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    checkConnection();
    setupEventListeners();
    updateFormFields();
    loadCart();
});

// Setup event listeners
function setupEventListeners() {
    document.getElementById('serviceType').addEventListener('change', (e) => {
        currentService = e.target.value;
        updateFormFields();
    });

    document.getElementById('globalRegion').addEventListener('change', (e) => {
        currentRegion = e.target.value;
        // Reload instances if EC2 is selected
        if (currentService === 'EC2') {
            loadAvailableInstances();
        }
    });

    document.getElementById('addToCartBtn').addEventListener('click', addToCart);
    document.getElementById('clearCartBtn').addEventListener('click', clearCart);
    document.getElementById('downloadBtn').addEventListener('click', downloadReport);
}

// Check AWS connection
async function checkConnection() {
    const statusDot = document.getElementById('statusDot');
    const statusText = document.getElementById('statusText');

    try {
        const response = await fetch('/api/test-connection');
        const data = await response.json();

        if (data.success) {
            statusDot.className = 'status-dot connected';
            statusText.textContent = 'Connected to AWS';
        } else {
            statusDot.className = 'status-dot disconnected';
            statusText.textContent = 'Not Connected';
        }
    } catch (error) {
        statusDot.className = 'status-dot disconnected';
        statusText.textContent = 'Connection Error';
    }
}

// Update form fields based on selected service
function updateFormFields() {
    const container = document.getElementById('serviceFormsContainer');
    container.innerHTML = SERVICE_FORMS[currentService] || '';

    // Load available instances if EC2 is selected
    if (currentService === 'EC2') {
        loadAvailableInstances();
    }
}

// Load available EC2 instance types from backend
async function loadAvailableInstances() {
    const select = document.getElementById('ec2InstanceType');
    if (!select) return;

    try {
        const response = await fetch(`/api/available-instances?region=${encodeURIComponent(currentRegion)}`);
        const data = await response.json();

        if (data.success && data.instances) {
            select.innerHTML = data.instances.map(instance =>
                `<option value="${instance}">${instance}</option>`
            ).join('');
        } else {
            select.innerHTML = '<option value="">No instances available</option>';
        }
    } catch (error) {
        console.error('Failed to load instances:', error);
        select.innerHTML = '<option value="">Error loading instances</option>';
    }
}

// Add resource to cart
async function addToCart() {
    const btn = document.getElementById('addToCartBtn');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> Adding...';

    clearMessages();

    try {
        // Get pricing first
        const pricingData = await fetchPricingData();

        if (!pricingData || pricingData.length === 0) {
            showMessage('No pricing data available for this configuration', 'error');
            return;
        }

        // Create cart item from pricing data
        const cartItem = createCartItemFromPricing(pricingData[0]);

        // Add to cart via API
        const response = await fetch('/api/cart/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(cartItem)
        });

        const result = await response.json();

        if (result.success) {
            showMessage('Resource added to cart!', 'success');
            loadCart();
        } else {
            showMessage(result.error || 'Failed to add to cart', 'error');
        }
    } catch (error) {
        showMessage('Error: ' + error.message, 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = '🛒 Add to Cart';
    }
}

// Fetch pricing data based on current service
async function fetchPricingData() {
    let endpoint, data;

    switch (currentService) {
        case 'EC2':
            endpoint = '/api/pricing/ec2';
            data = {
                instanceType: document.getElementById('ec2InstanceType').value,
                region: currentRegion,
                operatingSystem: document.getElementById('ec2OS').value,
                tenancy: 'Shared'
            };
            break;

        case 'RDS':
            endpoint = '/api/pricing/rds';
            data = {
                instanceType: document.getElementById('rdsInstanceType').value,
                region: currentRegion,
                databaseEngine: document.getElementById('rdsEngine').value,
                deploymentOption: document.getElementById('rdsDeployment').value
            };
            break;

        case 'S3':
            endpoint = '/api/pricing/s3';
            data = {
                storageClass: document.getElementById('s3StorageClass').value,
                region: currentRegion,
                storageGB: document.getElementById('s3StorageGB').value
            };
            break;

        case 'VPC':
            endpoint = '/api/pricing/vpc';
            data = {
                component: document.getElementById('vpcComponent').value,
                region: currentRegion,
                quantity: document.getElementById('vpcQuantity').value
            };
            break;

        case 'ALB':
            endpoint = '/api/pricing/alb';
            data = {
                region: currentRegion,
                quantity: document.getElementById('albQuantity').value
            };
            break;

        case 'Route53':
            endpoint = '/api/pricing/route53';
            data = {
                component: document.getElementById('route53Component').value,
                quantity: document.getElementById('route53Quantity').value
            };
            break;
    }

    const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    return result.success ? result.data : [];
}

// Create cart item from pricing data
function createCartItemFromPricing(pricingData) {
    let specs = '';
    let hourlyCost = 0;
    let monthlyCost = 0;
    let resourceType = '';
    let quantity = 1;

    switch (currentService) {
        case 'EC2':
            quantity = parseInt(document.getElementById('ec2Quantity').value);
            resourceType = pricingData.instanceType || 'Unknown';
            specs = `${pricingData.vcpu || 'N/A'} vCPU, ${pricingData.memory || 'N/A'} RAM, ${document.getElementById('ec2OS').value}`;
            if (pricingData.prices && pricingData.prices[0]) {
                hourlyCost = parseFloat(pricingData.prices[0].amount) * quantity;
                monthlyCost = hourlyCost * 730;
            }
            break;

        case 'RDS':
            quantity = parseInt(document.getElementById('rdsQuantity').value);
            resourceType = pricingData.instanceType || 'Unknown';
            specs = `${document.getElementById('rdsEngine').value}, ${document.getElementById('rdsDeployment').value}`;
            if (pricingData.prices && pricingData.prices[0]) {
                hourlyCost = parseFloat(pricingData.prices[0].amount) * quantity;
                monthlyCost = hourlyCost * 730;
            }
            break;

        case 'S3':
            const storageGB = document.getElementById('s3StorageGB').value;
            resourceType = pricingData.storageClass || 'Storage';
            specs = `${storageGB} GB, ${pricingData.storageClass || 'Standard'}`;
            if (pricingData.prices && pricingData.prices[0]) {
                monthlyCost = pricingData.prices[0].monthly_cost;
                hourlyCost = monthlyCost / 730;
            }
            break;

        case 'VPC':
        case 'ALB':
        case 'Route53':
            quantity = currentService === 'VPC' ? parseInt(document.getElementById('vpcQuantity').value) :
                currentService === 'ALB' ? parseInt(document.getElementById('albQuantity').value) :
                    parseInt(document.getElementById('route53Quantity').value);
            resourceType = pricingData.productFamily || pricingData.description || 'Unknown';
            specs = `Quantity: ${quantity}`;
            if (pricingData.prices && pricingData.prices[0]) {
                monthlyCost = pricingData.prices[0].monthly_cost;
                hourlyCost = monthlyCost / 730;
            }
            break;
    }

    return {
        service: currentService,
        resourceType: resourceType,
        specifications: specs,
        region: currentRegion,
        quantity: quantity,
        hourlyCost: hourlyCost,
        monthlyCost: monthlyCost
    };
}

// Load cart from server
async function loadCart() {
    try {
        const response = await fetch('/api/cart/items');
        const data = await response.json();

        if (data.success) {
            cart = data.items;
            renderCart();
            updateTotal();
        }
    } catch (error) {
        console.error('Failed to load cart:', error);
    }
}

// Render cart items
function renderCart() {
    const container = document.getElementById('cartItems');

    if (cart.length === 0) {
        container.innerHTML = '<div class="empty-cart">🛒 Cart is empty<br><small>Add resources to calculate costs</small></div>';
        document.getElementById('downloadBtn').disabled = true;
        return;
    }

    document.getElementById('downloadBtn').disabled = false;

    container.innerHTML = cart.map(item => `
        <div class="cart-item">
            <div class="cart-item-header">
                <span class="service-badge">${item.service}</span>
                <button class="btn-remove" onclick="removeFromCart('${item.id}')">×</button>
            </div>
            <div class="cart-item-body">
                <div class="resource-name">${item.resourceType}</div>
                <div class="resource-specs">${item.specifications}</div>
                <div class="resource-region">📍 ${item.region}</div>
            </div>
            <div class="cart-item-price">
                <div class="price-monthly">$${item.monthlyCost.toFixed(2)}<small>/mo</small></div>
                <div class="price-hourly">$${item.hourlyCost.toFixed(4)}/hr</div>
            </div>
        </div>
    `).join('');
}

// Remove item from cart
async function removeFromCart(itemId) {
    try {
        const response = await fetch(`/api/cart/remove/${itemId}`, { method: 'DELETE' });
        const data = await response.json();

        if (data.success) {
            loadCart();
            showMessage('Item removed from cart', 'info');
        }
    } catch (error) {
        showMessage('Failed to remove item', 'error');
    }
}

// Clear entire cart
async function clearCart() {
    if (!confirm('Are you sure you want to clear all items?')) return;

    try {
        const response = await fetch('/api/cart/clear', { method: 'DELETE' });
        const data = await response.json();

        if (data.success) {
            loadCart();
            showMessage('Cart cleared', 'info');
        }
    } catch (error) {
        showMessage('Failed to clear cart', 'error');
    }
}

// Update total cost display
async function updateTotal() {
    try {
        const response = await fetch('/api/cart/total');
        const data = await response.json();

        if (data.success) {
            document.getElementById('totalCost').textContent = `$${data.total.toFixed(2)}`;
            document.getElementById('annualCost').textContent = `$${(data.total * 12).toFixed(2)}`;
        }
    } catch (error) {
        console.error('Failed to update total:', error);
    }
}

// Download CSV report
function downloadReport() {
    window.location.href = '/api/export/csv';
    showMessage('Downloading cost report...', 'success');
}

// Show message
function showMessage(message, type = 'info') {
    const messagesDiv = document.getElementById('messages');

    const messageEl = document.createElement('div');
    messageEl.className = `message ${type}`;
    messageEl.innerHTML = `
        <span>${getMessageIcon(type)}</span>
        <span>${message}</span>
    `;

    messagesDiv.appendChild(messageEl);

    if (type === 'success' || type === 'info') {
        setTimeout(() => {
            messageEl.style.opacity = '0';
            setTimeout(() => messageEl.remove(), 300);
        }, 4000);
    }
}

// Clear messages
function clearMessages() {
    document.getElementById('messages').innerHTML = '';
}

// Get message icon
function getMessageIcon(type) {
    switch (type) {
        case 'error': return '❌';
        case 'success': return '✅';
        case 'info': return 'ℹ️';
        default: return 'ℹ️';
    }
}
