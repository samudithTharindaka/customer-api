# Customer API for ERPNext

Professional REST API for customer management in ERPNext/Frappe Framework.

## Overview

Customer API is a Frappe app that provides RESTful API endpoints for managing customers in ERPNext. Perfect for integrating e-commerce platforms, CRM systems, or any external application with your ERPNext instance.

## Features

- ✅ **Check Customer Availability** - Verify if a customer exists by name
- ✅ **Create Customers** - Create customers with complete contact and address information
- ✅ **Automatic Linking** - Contacts and addresses are automatically linked to customers
- ✅ **Duplicate Detection** - Prevents duplicate customer creation
- ✅ **RESTful Design** - Standard HTTP methods and JSON responses
- ✅ **Secure** - Built-in authentication and permission checks
- ✅ **Well Documented** - Complete API documentation with Swagger UI

## Installation

### Install via Frappe Bench

```bash
# Get the app
bench get-app https://github.com/YOUR_USERNAME/customer_api.git

# Install on your site
bench --site your-site.com install-app customer_api

# Restart bench
bench restart
```

### Manual Installation

```bash
cd ~/frappe-bench/apps
git clone https://github.com/YOUR_USERNAME/customer_api.git
cd ~/frappe-bench
bench --site your-site.com install-app customer_api
bench restart
```

## API Endpoints

### 1. Check Customer Availability

**Endpoint:** `GET /api/method/customer_api.api.check_customer_registered`

Check if a customer exists in the system.

**Parameters:**
- `customer_name` (required): Customer name to check

**Example:**
```bash
curl -X GET "https://your-site.com/api/method/customer_api.api.check_customer_registered?customer_name=John%20Doe" \
  -H "Authorization: token API_KEY:API_SECRET"
```

**Response:**
```json
{
  "message": {
    "customer_name": "John Doe",
    "is_registered": true,
    "customer_id": "John Doe",
    "customer_group": "Individual",
    "territory": "All Territories",
    "customer_type": "Individual",
    "disabled": 0
  }
}
```

### 2. Create Customer

**Endpoint:** `POST /api/method/customer_api.api.create_customer`

Create a new customer with optional contact and address information.

**Parameters:**
- `customer_name` (required): Customer name
- `customer_type` (optional): "Individual" or "Company" (default: "Individual")
- `customer_group` (optional): Customer group
- `territory` (optional): Territory
- `email` (optional): Email address
- `mobile` (optional): Mobile number
- `phone` (optional): Phone number
- `address_line1`, `address_line2`, `city`, `state`, `country`, `pincode` (optional): Address details

**Example:**
```bash
curl -X POST "https://your-site.com/api/method/customer_api.api.create_customer" \
  -H "Authorization: token API_KEY:API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Jane Smith",
    "email": "jane@example.com",
    "mobile": "+1234567890",
    "address_line1": "123 Main St",
    "city": "New York",
    "country": "United States"
  }'
```

**Response:**
```json
{
  "message": {
    "success": true,
    "customer_id": "Jane Smith",
    "customer_name": "Jane Smith",
    "customer_type": "Individual",
    "customer_group": "All Customer Groups",
    "territory": "All Territories",
    "contact_id": "Jane Smith-Jane Smith",
    "address_id": "Jane Smith-Billing",
    "message": "Customer created successfully"
  }
}
```

## Authentication

All API endpoints require authentication. You can use either:

### API Key/Secret (Recommended)

1. Go to User → Your User in ERPNext
2. Scroll to "API Access" section
3. Click "Generate Keys"
4. Use in Authorization header: `token {api_key}:{api_secret}`

### Session Cookie

Login via `/api/method/login` and use the session cookie for subsequent requests.

## Documentation

### Interactive API Documentation (Swagger UI)

Access the complete interactive API documentation at:

```
https://your-site.com/api-docs
```

Features:
- Try out API calls directly from your browser
- Complete request/response schemas
- Example requests for all endpoints
- Authentication testing

### API Reference

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API reference with examples in multiple languages:
- cURL
- Python
- JavaScript/Node.js
- PHP
- WooCommerce integration examples

## What Gets Created

When you create a customer with full details, the following records are created in ERPNext:

1. **Customer Document** - Always created with provided details
2. **Contact Document** - Created if email, mobile, or phone is provided
3. **Address Document** - Created if address information is provided

All records are automatically linked together.

## Use Cases

- **E-commerce Integration** - Sync WooCommerce/Shopify customers to ERPNext
- **CRM Integration** - Import customers from external CRM systems
- **Mobile Apps** - Create customers from mobile applications
- **Wholesale Portals** - Allow B2B customers to self-register
- **Lead Conversion** - Convert website leads to customers
- **Third-party Systems** - Any system that needs to create customers in ERPNext

## Requirements

- Frappe Framework v13 or higher
- ERPNext v13 or higher
- Python 3.7+

## Configuration

### CSRF Protection (Development)

For development/testing environments, you may need to disable CSRF:

```json
// sites/common_site_config.json
{
  "ignore_csrf": 1
}
```

**Note:** Remove this in production and use API Key authentication.

## Permissions

Users making API calls need the following permissions:
- **Read** access to Customer doctype
- **Create/Write** access to Customer doctype (for create endpoint)
- **Create/Write** access to Contact and Address doctypes (if creating with contact/address info)

## Error Handling

The API returns appropriate HTTP status codes and structured error messages:

- `200 OK` - Request successful
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `500 Internal Server Error` - Server error

Error responses include detailed messages to help diagnose issues.

## Support

For issues, questions, or feature requests:
- Create an issue on GitHub
- Check the [API Documentation](API_DOCUMENTATION.md)
- Review the Swagger UI documentation

## License

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## About

Built with ❤️ for the Frappe/ERPNext community.

Professional REST API solution for customer management in ERPNext.
