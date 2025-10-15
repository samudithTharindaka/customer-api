## Customer API

Custom API endpoints for ERPNext Customer doctype.

### Features

- Check if a customer is registered by customer name
- Check if a customer is registered by customer ID
- Create new customers with contact and address information

### Installation

```bash
bench get-app customer_api
bench --site your-site-name install-app customer_api
```

### API Endpoints

#### Check Customer Registration

**Endpoint:** `/api/method/customer_api.api.check_customer_registered`

**Method:** GET/POST

**Parameters:**
- `customer_name` (required): The name of the customer to check

**Response:**
```json
{
  "message": {
    "customer_name": "Customer Name",
    "is_registered": true,
    "customer_id": "CUST-00001"
  }
}
```

**Example Usage:**
```bash
curl -X GET "http://your-site/api/method/customer_api.api.check_customer_registered?customer_name=John%20Doe"
```

#### Check Customer by ID

**Endpoint:** `/api/method/customer_api.api.check_customer_by_id`

**Method:** GET/POST

**Parameters:**
- `customer_id` (required): The customer ID to check

**Example Usage:**
```bash
curl -X GET "http://your-site/api/method/customer_api.api.check_customer_by_id?customer_id=CUST-00001"
```

#### Create Customer

**Endpoint:** `/api/method/customer_api.api.create_customer`

**Method:** POST

**Parameters:**
- `customer_name` (required): The name of the customer
- `customer_type` (optional): "Individual" or "Company" (default: "Individual")
- `customer_group` (optional): Customer group
- `territory` (optional): Territory
- `email` (optional): Customer email
- `mobile` (optional): Customer mobile number
- `phone` (optional): Customer phone number
- `address_line1`, `address_line2`, `city`, `state`, `country`, `pincode` (optional): Address details

**Response:**
```json
{
  "message": {
    "success": true,
    "customer_id": "CUST-00002",
    "customer_name": "Jane Smith",
    "message": "Customer created successfully"
  }
}
```

**Example Usage:**
```bash
curl -X POST "http://your-site/api/method/customer_api.api.create_customer" \
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

### Documentation

For detailed documentation and more examples, see:
- `USAGE_GUIDE.md` - Complete usage guide with examples in multiple languages
- `API_DOCUMENTATION.md` - Comprehensive API reference with WooCommerce integration examples

### License

MIT

