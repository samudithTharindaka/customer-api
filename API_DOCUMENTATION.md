# Customer API Documentation

## Overview

This API provides endpoints for customer management in Frappe/ERPNext. All endpoints require authentication.

---

## Authentication

All API endpoints require authentication. Include your API key and secret in the request headers:

```bash
Authorization: token <api_key>:<api_secret>
```

Or use session-based authentication by logging in first.

---

## Endpoints

### 1. Check Customer Registration by Name

**Endpoint:** `/api/method/customer_api.api.check_customer_registered`

**Method:** `GET` or `POST`

**Description:** Check if a customer exists in the system by their name.

**Parameters:**
- `customer_name` (required): The name of the customer to check

**Example Request:**
```bash
curl -X POST https://your-site.com/api/method/customer_api.api.check_customer_registered \
  -H "Authorization: token your_api_key:your_api_secret" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe"
  }'
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
    "customer_name": "Jane Smith",
    "is_registered": false,
    "customer_id": null,
    "customer_group": null,
    "territory": null,
    "customer_type": null,
    "disabled": null
  }
}
```

---

### 2. Create Customer

**Endpoint:** `/api/method/customer_api.api.create_customer`

**Method:** `POST`

**Description:** Create a new customer in the system with optional contact and address information.

**Parameters:**

**Required:**
- `customer_name` (string): The name of the customer

**Optional:**
- `customer_type` (string): "Individual" or "Company" (default: "Individual")
- `customer_group` (string): Customer group (defaults to system setting)
- `territory` (string): Territory (defaults to system setting)
- `email` (string): Customer email address
- `mobile` (string): Customer mobile number
- `phone` (string): Customer phone number
- `address_line1` (string): Address line 1
- `address_line2` (string): Address line 2
- `city` (string): City
- `state` (string): State/Province
- `country` (string): Country
- `pincode` (string): Postal/ZIP code

**Example Request (Minimal):**
```bash
curl -X POST https://your-site.com/api/method/customer_api.api.create_customer \
  -H "Authorization: token your_api_key:your_api_secret" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Jane Smith"
  }'
```

**Example Request (Complete):**
```bash
curl -X POST https://your-site.com/api/method/customer_api.api.create_customer \
  -H "Authorization: token your_api_key:your_api_secret" \
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

**Example Response (Customer Already Exists):**
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

---

## Python/Requests Examples

### Check Customer Registration

```python
import requests

url = "https://your-site.com/api/method/customer_api.api.check_customer_registered"
headers = {
    "Authorization": "token your_api_key:your_api_secret",
    "Content-Type": "application/json"
}
data = {
    "customer_name": "John Doe"
}

response = requests.post(url, json=data, headers=headers)
result = response.json()

if result["message"]["is_registered"]:
    print(f"Customer found: {result['message']['customer_id']}")
else:
    print("Customer not found")
```

### Create Customer

```python
import requests

url = "https://your-site.com/api/method/customer_api.api.create_customer"
headers = {
    "Authorization": "token your_api_key:your_api_secret",
    "Content-Type": "application/json"
}
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

response = requests.post(url, json=data, headers=headers)
result = response.json()

if result["message"]["success"]:
    print(f"Customer created: {result['message']['customer_id']}")
else:
    print(f"Error: {result['message']['message']}")
```

---

## PHP Examples

### Check Customer Registration

```php
<?php
$url = "https://your-site.com/api/method/customer_api.api.check_customer_registered";
$headers = [
    "Authorization: token your_api_key:your_api_secret",
    "Content-Type: application/json"
];
$data = json_encode([
    "customer_name" => "John Doe"
]);

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
curl_close($ch);

$result = json_decode($response, true);

if ($result["message"]["is_registered"]) {
    echo "Customer found: " . $result["message"]["customer_id"];
} else {
    echo "Customer not found";
}
?>
```

### Create Customer

```php
<?php
$url = "https://your-site.com/api/method/customer_api.api.create_customer";
$headers = [
    "Authorization: token your_api_key:your_api_secret",
    "Content-Type: application/json"
];
$data = json_encode([
    "customer_name" => "Jane Smith",
    "customer_type" => "Individual",
    "email" => "jane.smith@example.com",
    "mobile" => "+1234567890",
    "address_line1" => "123 Main Street",
    "city" => "New York",
    "state" => "NY",
    "country" => "United States",
    "pincode" => "10001"
]);

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
curl_close($ch);

$result = json_decode($response, true);

if ($result["message"]["success"]) {
    echo "Customer created: " . $result["message"]["customer_id"];
} else {
    echo "Error: " . $result["message"]["message"];
}
?>
```

---

## JavaScript/Node.js Examples

### Check Customer Registration

```javascript
const axios = require('axios');

const url = 'https://your-site.com/api/method/customer_api.api.check_customer_registered';
const headers = {
    'Authorization': 'token your_api_key:your_api_secret',
    'Content-Type': 'application/json'
};
const data = {
    customer_name: 'John Doe'
};

axios.post(url, data, { headers })
    .then(response => {
        if (response.data.message.is_registered) {
            console.log('Customer found:', response.data.message.customer_id);
        } else {
            console.log('Customer not found');
        }
    })
    .catch(error => {
        console.error('Error:', error.message);
    });
```

### Create Customer

```javascript
const axios = require('axios');

const url = 'https://your-site.com/api/method/customer_api.api.create_customer';
const headers = {
    'Authorization': 'token your_api_key:your_api_secret',
    'Content-Type': 'application/json'
};
const data = {
    customer_name: 'Jane Smith',
    customer_type: 'Individual',
    email: 'jane.smith@example.com',
    mobile: '+1234567890',
    address_line1: '123 Main Street',
    city: 'New York',
    state: 'NY',
    country: 'United States',
    pincode: '10001'
};

axios.post(url, data, { headers })
    .then(response => {
        if (response.data.message.success) {
            console.log('Customer created:', response.data.message.customer_id);
        } else {
            console.log('Error:', response.data.message.message);
        }
    })
    .catch(error => {
        console.error('Error:', error.message);
    });
```

---

## WooCommerce Integration Example

Here's an example of how to integrate this with WooCommerce using a custom plugin:

```php
<?php
/**
 * Sync WooCommerce customer to ERPNext
 */
add_action('woocommerce_created_customer', 'sync_customer_to_erpnext', 10, 1);

function sync_customer_to_erpnext($customer_id) {
    $customer = new WC_Customer($customer_id);
    
    $url = "https://your-erpnext-site.com/api/method/customer_api.api.create_customer";
    $headers = [
        "Authorization: token your_api_key:your_api_secret",
        "Content-Type: application/json"
    ];
    
    $data = json_encode([
        "customer_name" => $customer->get_first_name() . ' ' . $customer->get_last_name(),
        "customer_type" => "Individual",
        "email" => $customer->get_email(),
        "mobile" => $customer->get_billing_phone(),
        "address_line1" => $customer->get_billing_address_1(),
        "address_line2" => $customer->get_billing_address_2(),
        "city" => $customer->get_billing_city(),
        "state" => $customer->get_billing_state(),
        "country" => $customer->get_billing_country(),
        "pincode" => $customer->get_billing_postcode()
    ]);
    
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    
    $response = curl_exec($ch);
    curl_close($ch);
    
    $result = json_decode($response, true);
    
    if ($result["message"]["success"]) {
        // Store ERPNext customer ID in WooCommerce user meta
        update_user_meta($customer_id, 'erpnext_customer_id', $result["message"]["customer_id"]);
    }
}
?>
```

---

## Error Handling

All endpoints return structured error messages. Always check the `success` field in create operations:

```python
response = requests.post(url, json=data, headers=headers)
result = response.json()

if "message" in result:
    if "success" in result["message"]:
        # This is a create_customer response
        if result["message"]["success"]:
            # Success
            customer_id = result["message"]["customer_id"]
        else:
            # Error
            error_message = result["message"]["message"]
    else:
        # This is a check_customer response
        if result["message"]["is_registered"]:
            # Customer exists
            customer_id = result["message"]["customer_id"]
        else:
            # Customer doesn't exist
            pass
```

---

## Testing the API

You can test these endpoints using:

1. **Postman**: Import the examples above
2. **curl**: Use the command-line examples
3. **Frappe Console**: Test directly in your ERPNext site:
   ```python
   import frappe
   from customer_api.api import create_customer
   
   result = create_customer(
       customer_name="Test Customer",
       email="test@example.com",
       mobile="+1234567890"
   )
   print(result)
   ```

---

## Security Notes

1. **Never expose API keys** in client-side code
2. Use **HTTPS** for all API requests
3. Implement **rate limiting** on your server
4. Regularly **rotate API keys**
5. Use **IP whitelisting** if possible
6. Monitor API logs for suspicious activity

---

## Support

For issues or questions:
- Check Frappe documentation: https://frappeframework.com/docs
- ERPNext API docs: https://frappeframework.com/docs/user/en/api
- GitHub Issues: https://github.com/samudithTharindaka/wooIntergtare-Frappe-app/issues

