## Customer API

Custom API endpoints for ERPNext Customer doctype.

### Features

- Check if a customer is registered by customer name

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

### License

MIT

