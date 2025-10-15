# Manual Testing Guide - Customer API

## 🚀 Step-by-Step Testing Instructions

### Step 1: Start Your Bench

```bash
cd /home/samudith/frappe-bench
bench start
```

Your site should be accessible at: **http://localhost:8000**

---

## 🔐 Step 2: Get API Credentials

### Option A: Use Session-Based Authentication (Easier for Testing)

1. **Login to get session cookie:**
```bash
curl -X POST "http://localhost:8000/api/method/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "usr=Administrator&pwd=admin" \
  -c cookies.txt
```

2. **Use the cookie for subsequent requests:**
```bash
curl -X GET "http://localhost:8000/api/method/customer_api.api.check_customer_registered?customer_name=Test" \
  -b cookies.txt
```

### Option B: Use API Key/Secret (For Production)

1. **Generate API Key in ERPNext:**
   - Go to: http://localhost:8000/app/user
   - Click on "Administrator" (or your user)
   - Scroll to "API Access" section
   - Click "Generate Keys"
   - Copy the API Key and API Secret

2. **Use in requests:**
```bash
curl -X GET "http://localhost:8000/api/method/customer_api.api.check_customer_registered?customer_name=Test" \
  -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET"
```

---

## 🧪 Step 3: Test the Endpoints

### Test 1: Check Customer Registration (by name)

**URL:** `http://localhost:8000/api/method/customer_api.api.check_customer_registered`

**Method:** GET or POST

**cURL Command (with cookie):**
```bash
curl -X GET "http://localhost:8000/api/method/customer_api.api.check_customer_registered?customer_name=Test%20Customer%20API" \
  -b cookies.txt
```

**cURL Command (with API key):**
```bash
curl -X GET "http://localhost:8000/api/method/customer_api.api.check_customer_registered?customer_name=Test%20Customer%20API" \
  -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET"
```

**Expected Response:**
```json
{
  "message": {
    "customer_name": "Test Customer API",
    "is_registered": true,
    "customer_id": "Test Customer API",
    "customer_group": "All Customer Groups",
    "territory": "All Territories",
    "customer_type": "Individual",
    "disabled": 0
  }
}
```

---

### Test 2: Check Customer by ID

**URL:** `http://localhost:8000/api/method/customer_api.api.check_customer_by_id`

**Method:** GET or POST

**cURL Command:**
```bash
curl -X GET "http://localhost:8000/api/method/customer_api.api.check_customer_by_id?customer_id=Test%20Customer%20API" \
  -b cookies.txt
```

**Expected Response:**
```json
{
  "message": {
    "customer_id": "Test Customer API",
    "is_registered": true,
    "customer_name": "Test Customer API",
    "customer_group": "All Customer Groups",
    "territory": "All Territories",
    "customer_type": "Individual",
    "disabled": 0
  }
}
```

---

### Test 3: Create Customer (Minimal)

**URL:** `http://localhost:8000/api/method/customer_api.api.create_customer`

**Method:** POST

**cURL Command:**
```bash
curl -X POST "http://localhost:8000/api/method/customer_api.api.create_customer" \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "customer_name": "Manual Test Customer"
  }'
```

**Expected Response:**
```json
{
  "message": {
    "success": true,
    "customer_id": "Manual Test Customer",
    "customer_name": "Manual Test Customer",
    "customer_type": "Individual",
    "customer_group": "All Customer Groups",
    "territory": "All Territories",
    "contact_id": null,
    "address_id": null,
    "message": "Customer created successfully"
  }
}
```

---

### Test 4: Create Customer (Full Details)

**URL:** `http://localhost:8000/api/method/customer_api.api.create_customer`

**Method:** POST

**cURL Command:**
```bash
curl -X POST "http://localhost:8000/api/method/customer_api.api.create_customer" \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "customer_name": "Sarah Connor",
    "customer_type": "Individual",
    "customer_group": "Commercial",
    "territory": "Rest Of The World",
    "email": "sarah.connor@example.com",
    "mobile": "+1-555-0123",
    "phone": "+1-555-9876",
    "address_line1": "1234 Tech Road",
    "address_line2": "Building A",
    "city": "Los Angeles",
    "state": "California",
    "country": "United States",
    "pincode": "90001"
  }'
```

**Expected Response:**
```json
{
  "message": {
    "success": true,
    "customer_id": "Sarah Connor",
    "customer_name": "Sarah Connor",
    "customer_type": "Individual",
    "customer_group": "Commercial",
    "territory": "Rest Of The World",
    "contact_id": "Sarah Connor-Sarah Connor",
    "address_id": "Sarah Connor-Billing",
    "message": "Customer created successfully"
  }
}
```

---

### Test 5: Try Creating Duplicate (Error Handling)

**cURL Command:**
```bash
curl -X POST "http://localhost:8000/api/method/customer_api.api.create_customer" \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "customer_name": "Sarah Connor"
  }'
```

**Expected Response:**
```json
{
  "message": {
    "success": false,
    "customer_id": "Sarah Connor",
    "customer_name": "Sarah Connor",
    "message": "Customer already exists with this name"
  }
}
```

---

## 🌐 Using Postman

### Setup in Postman:

1. **Import Collection:**
   - Create a new Collection: "Customer API"

2. **Add Environment Variables:**
   - `base_url`: `http://localhost:8000`
   - `api_key`: Your API key
   - `api_secret`: Your API secret

3. **Check Customer (GET Request):**
   - URL: `{{base_url}}/api/method/customer_api.api.check_customer_registered`
   - Method: GET
   - Params: `customer_name` = `Test Customer API`
   - Headers: `Authorization` = `token {{api_key}}:{{api_secret}}`

4. **Create Customer (POST Request):**
   - URL: `{{base_url}}/api/method/customer_api.api.create_customer`
   - Method: POST
   - Headers: 
     - `Content-Type`: `application/json`
     - `Authorization`: `token {{api_key}}:{{api_secret}}`
   - Body (raw JSON):
     ```json
     {
       "customer_name": "Postman Test Customer",
       "email": "postman@example.com",
       "mobile": "+1234567890"
     }
     ```

---

## 🔍 Verify Created Customers in ERPNext UI

After creating customers via API, verify them in the UI:

1. **Go to Customer List:**
   - URL: http://localhost:8000/app/customer
   - You should see your newly created customers

2. **View Customer Details:**
   - Click on a customer (e.g., "Sarah Connor")
   - Check that contact information is linked
   - Check that address is linked
   - Email and mobile should be visible

3. **View Contact:**
   - Go to: http://localhost:8000/app/contact
   - Find the contact linked to your customer
   - Verify email and phone numbers

4. **View Address:**
   - Go to: http://localhost:8000/app/address
   - Find the address linked to your customer
   - Verify all address fields

---

## 🐛 Troubleshooting

### Issue: "Not authenticated"
**Solution:** 
- Make sure you're logged in or using valid API credentials
- Try the session-based login again
- Check that cookies.txt file was created

### Issue: "404 Not Found"
**Solution:**
- Check that bench is running: `bench start`
- Verify the app is installed: `bench --site erpsite.com list-apps`
- Check the URL is correct (no typos)

### Issue: "Method not allowed"
**Solution:**
- Make sure you're using POST for create_customer
- GET is for check endpoints only

### Issue: "Customer already exists"
**Solution:**
- This is expected behavior for duplicates
- Use a different customer name
- Or check existing customer instead

---

## 📊 Quick Reference Table

| Endpoint | Method | URL | Purpose |
|----------|--------|-----|---------|
| Check by Name | GET/POST | `/api/method/customer_api.api.check_customer_registered` | Check if customer exists by name |
| Check by ID | GET/POST | `/api/method/customer_api.api.check_customer_by_id` | Check if customer exists by ID |
| Create Customer | POST | `/api/method/customer_api.api.create_customer` | Create new customer with details |

---

## 🎯 Next Steps

1. ✅ Start bench
2. ✅ Login to get session cookie
3. ✅ Test check_customer_registered
4. ✅ Test check_customer_by_id
5. ✅ Test create_customer (minimal)
6. ✅ Test create_customer (full)
7. ✅ Verify in ERPNext UI
8. ✅ Test duplicate handling

---

## 📝 Sample Test Customers

Use these for testing (they should exist from our earlier tests):
- "Test Customer API"
- "Jane Smith Final"
- "Test Minimal Customer"

---

## 💡 Pro Tips

1. **Use -v flag in curl** to see full request/response:
   ```bash
   curl -v -X GET "http://localhost:8000/api/method/..." -b cookies.txt
   ```

2. **Pretty print JSON responses** with jq:
   ```bash
   curl -X GET "http://localhost:8000/api/method/..." -b cookies.txt | jq
   ```

3. **Save responses to file**:
   ```bash
   curl -X GET "..." -b cookies.txt > response.json
   ```

4. **Test without SSL verification** (if needed):
   ```bash
   curl -k -X GET "https://..."
   ```

---

## ✅ Ready to Test!

Start with the session login, then try each endpoint in order. Good luck! 🚀

