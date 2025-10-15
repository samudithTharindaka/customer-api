# Customer API - Usage Guide

## Overview

This custom Frappe app adds API endpoints to check if a customer is registered in your ERPNext system and to create new customers.

## Installation

The app has already been installed. If you need to install it on another site:

```bash
cd /home/samudith/frappe-bench
bench --site your-site-name install-app customer_api
```

## Available Endpoints

### 1. Check Customer by Name

**Endpoint:** `/api/method/customer_api.api.check_customer_registered`

**Method:** GET or POST

**Authentication:** Required (API Key/Token or Session)

**Parameters:**
- `customer_name` (required): The customer name to check

**Example Request (cURL):**
```bash
# With session cookie
curl -X GET "http://erpsite.com:8000/api/method/customer_api.api.check_customer_registered?customer_name=John%20Doe" \
  -H "Cookie: sid=YOUR_SESSION_ID"

# With API key (Generate from User → API Access)
curl -X GET "http://erpsite.com:8000/api/method/customer_api.api.check_customer_registered?customer_name=John%20Doe" \
  -H "Authorization: token API_KEY:API_SECRET"
```

**Example Response (Customer Found):**
```json
{
  "message": {
    "customer_name": "John Doe",
    "is_registered": true,
    "customer_id": "CUST-00001",
    "customer_group": "Individual",
    "territory": "All Territories",
    "customer_type": "Individual",
    "disabled": 0
  }
}
```

**Example Response (Customer Not Found):**
```json
{
  "message": {
    "customer_name": "Non Existing Customer",
    "is_registered": false,
    "customer_id": null,
    "customer_group": null,
    "territory": null,
    "customer_type": null,
    "disabled": null
  }
}
```

### 2. Check Customer by ID

**Endpoint:** `/api/method/customer_api.api.check_customer_by_id`

**Method:** GET or POST

**Authentication:** Required (API Key/Token or Session)

**Parameters:**
- `customer_id` (required): The customer ID to check

**Example Request (cURL):**
```bash
curl -X GET "http://erpsite.com:8000/api/method/customer_api.api.check_customer_by_id?customer_id=CUST-00001" \
  -H "Authorization: token API_KEY:API_SECRET"
```

**Example Response:**
```json
{
  "message": {
    "customer_id": "CUST-00001",
    "is_registered": true,
    "customer_name": "John Doe",
    "customer_group": "Individual",
    "territory": "All Territories",
    "customer_type": "Individual",
    "disabled": 0
  }
}
```

### 3. Create Customer

**Endpoint:** `/api/method/customer_api.api.create_customer`

**Method:** POST

**Authentication:** Required (API Key/Token or Session)

**Parameters:**
- `customer_name` (required): The customer name
- `customer_type` (optional): "Individual" or "Company" (default: "Individual")
- `customer_group` (optional): Customer group (defaults to system setting)
- `territory` (optional): Territory (defaults to system setting)
- `email` (optional): Customer email address
- `mobile` (optional): Customer mobile number
- `phone` (optional): Customer phone number
- `address_line1` (optional): Address line 1
- `address_line2` (optional): Address line 2
- `city` (optional): City
- `state` (optional): State/Province
- `country` (optional): Country
- `pincode` (optional): Postal/ZIP code

**Example Request (cURL - Minimal):**
```bash
curl -X POST "http://erpsite.com:8000/api/method/customer_api.api.create_customer" \
  -H "Authorization: token API_KEY:API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Jane Smith"
  }'
```

**Example Request (cURL - Complete):**
```bash
curl -X POST "http://erpsite.com:8000/api/method/customer_api.api.create_customer" \
  -H "Authorization: token API_KEY:API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Jane Smith",
    "customer_type": "Individual",
    "customer_group": "Commercial",
    "territory": "United States",
    "email": "jane.smith@example.com",
    "mobile": "+1234567890",
    "phone": "+1987654321",
    "address_line1": "123 Main Street",
    "address_line2": "Apt 4B",
    "city": "New York",
    "state": "NY",
    "country": "United States",
    "pincode": "10001"
  }'
```

**Example Response (Success):**
```json
{
  "message": {
    "success": true,
    "customer_id": "CUST-00002",
    "customer_name": "Jane Smith",
    "customer_type": "Individual",
    "customer_group": "Commercial",
    "territory": "United States",
    "address_id": "ADDR-00001",
    "message": "Customer created successfully"
  }
}
```

**Example Response (Already Exists):**
```json
{
  "message": {
    "success": false,
    "customer_id": "CUST-00001",
    "customer_name": "Jane Smith",
    "message": "Customer already exists with this name"
  }
}
```

**Example Response (Error):**
```json
{
  "message": {
    "success": false,
    "customer_id": null,
    "customer_name": "Jane Smith",
    "message": "Error creating customer: <error details>"
  }
}
```

## Authentication Methods

### Method 1: Session-based Authentication (for web apps)

1. Login to get session:
```bash
curl -X POST "http://erpsite.com:8000/api/method/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "usr=your_username&pwd=your_password" \
  -c cookies.txt
```

2. Use the session cookie for subsequent requests:
```bash
curl -X GET "http://erpsite.com:8000/api/method/customer_api.api.check_customer_registered?customer_name=Test" \
  -b cookies.txt
```

### Method 2: API Key/Secret (recommended for integrations)

1. Generate API credentials in ERPNext:
   - Go to User List
   - Open your user
   - Scroll to "API Access" section
   - Click "Generate Keys"
   - Copy the API Key and API Secret

2. Use in requests:
```bash
curl -X GET "http://erpsite.com:8000/api/method/customer_api.api.check_customer_registered?customer_name=Test" \
  -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET"
```

## Python Examples

### Check Customer Registration

```python
import requests

# Configuration
base_url = "http://erpsite.com:8000"
api_key = "your_api_key"
api_secret = "your_api_secret"

# Headers
headers = {
    "Authorization": f"token {api_key}:{api_secret}"
}

# Check customer by name
response = requests.get(
    f"{base_url}/api/method/customer_api.api.check_customer_registered",
    params={"customer_name": "John Doe"},
    headers=headers
)

result = response.json()
if result["message"]["is_registered"]:
    print(f"Customer found: {result['message']['customer_id']}")
else:
    print("Customer not registered")
```

### Create Customer

```python
import requests

# Configuration
base_url = "http://erpsite.com:8000"
api_key = "your_api_key"
api_secret = "your_api_secret"

# Headers
headers = {
    "Authorization": f"token {api_key}:{api_secret}",
    "Content-Type": "application/json"
}

# Create customer
data = {
    "customer_name": "Jane Smith",
    "customer_type": "Individual",
    "email": "jane.smith@example.com",
    "mobile": "+1234567890",
    "address_line1": "123 Main Street",
    "city": "New York",
    "state": "NY",
    "country": "United States",
    "pincode": "10001"
}

response = requests.post(
    f"{base_url}/api/method/customer_api.api.create_customer",
    json=data,
    headers=headers
)

result = response.json()
if result["message"]["success"]:
    print(f"Customer created: {result['message']['customer_id']}")
else:
    print(f"Error: {result['message']['message']}")
```

## JavaScript Examples

### Check Customer Registration

```javascript
// Using Fetch API
const baseUrl = "http://erpsite.com:8000";
const apiKey = "your_api_key";
const apiSecret = "your_api_secret";

async function checkCustomer(customerName) {
    const url = `${baseUrl}/api/method/customer_api.api.check_customer_registered?customer_name=${encodeURIComponent(customerName)}`;
    
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': `token ${apiKey}:${apiSecret}`
        }
    });
    
    const data = await response.json();
    return data.message;
}

// Usage
checkCustomer("John Doe").then(result => {
    if (result.is_registered) {
        console.log(`Customer found: ${result.customer_id}`);
    } else {
        console.log("Customer not registered");
    }
});
```

### Create Customer

```javascript
// Using Fetch API
const baseUrl = "http://erpsite.com:8000";
const apiKey = "your_api_key";
const apiSecret = "your_api_secret";

async function createCustomer(customerData) {
    const url = `${baseUrl}/api/method/customer_api.api.create_customer`;
    
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Authorization': `token ${apiKey}:${apiSecret}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(customerData)
    });
    
    const data = await response.json();
    return data.message;
}

// Usage
const newCustomer = {
    customer_name: "Jane Smith",
    customer_type: "Individual",
    email: "jane.smith@example.com",
    mobile: "+1234567890",
    address_line1: "123 Main Street",
    city: "New York",
    state: "NY",
    country: "United States",
    pincode: "10001"
};

createCustomer(newCustomer).then(result => {
    if (result.success) {
        console.log(`Customer created: ${result.customer_id}`);
    } else {
        console.log(`Error: ${result.message}`);
    }
});
```

## Testing

A test script is provided at `/home/samudith/frappe-bench/test_customer_api.py`

To use it:

1. Make sure your bench is running:
```bash
cd /home/samudith/frappe-bench
bench start
```

2. In another terminal, run the test script:
```bash
cd /home/samudith/frappe-bench
python3 test_customer_api.py
```

3. Modify the script with actual customer names from your system for testing.

## Error Handling

The API will return appropriate HTTP status codes:

- **200 OK**: Request successful
- **401 Unauthorized**: Authentication failed
- **403 Forbidden**: User doesn't have permission
- **500 Internal Server Error**: Server error

Error response format:
```json
{
  "exc_type": "Exception",
  "exception": "Error message here"
}
```

## Permissions

By default, the endpoints require authentication (`allow_guest=False`). Make sure the user making the API call has the following permissions:

- **For check endpoints:** Read access to the Customer doctype
- **For create endpoint:** Create and Write access to the Customer doctype (and Address doctype if creating addresses)

You can modify the permissions in the `customer_api/api.py` file if needed.

## Troubleshooting

### Issue: "No module named 'customer_api'"
**Solution:** Reinstall the app:
```bash
cd /home/samudith/frappe-bench
./env/bin/pip install -e apps/customer_api
bench --site erpsite.com install-app customer_api
```

### Issue: "Authentication required"
**Solution:** Make sure you're providing valid credentials either via session cookie or API key/secret.

### Issue: API returns 404
**Solution:** Check that:
1. The bench is running
2. The URL is correct
3. The app is installed: `bench --site erpsite.com list-apps`

## Additional Resources

- [Frappe API Documentation](https://frappeframework.com/docs/user/en/api)
- [ERPNext API Documentation](https://frappeframework.com/docs/user/en/api/rest)

## Support

For issues or questions, check the code in:
- `/home/samudith/frappe-bench/apps/customer_api/customer_api/api.py`

You can modify the API endpoints by editing this file and restarting your bench.


