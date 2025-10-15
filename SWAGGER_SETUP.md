# 📚 Swagger/OpenAPI Documentation Setup

Your Customer API now has **complete Swagger/OpenAPI documentation**! 🎉

---

## 🌐 Access Swagger UI

### Method 1: Web Page (Recommended)

**URL:** http://erpsite.com:8000/api-docs

Just open this URL in your browser to see the interactive API documentation!

---

### Method 2: Direct OpenAPI Spec File

**Download/View the OpenAPI specification:**

```bash
# View in terminal
cat /home/samudith/frappe-bench/apps/customer_api/customer_api/openapi.yaml

# Or download from web
curl http://erpsite.com:8000/assets/customer_api/openapi.yaml
```

**Web URL:** http://erpsite.com:8000/assets/customer_api/openapi.yaml

---

### Method 3: Online Swagger Editor

1. Go to: https://editor.swagger.io/
2. Click **File** → **Import URL**
3. Enter: `http://erpsite.com:8000/assets/customer_api/openapi.yaml`
4. Or copy the content from the file and paste it

---

## 📖 What's Included in the Documentation

### ✅ Complete API Specification (OpenAPI 3.0.3)

1. **API Information**
   - Title, description, version
   - Contact and license info
   - Server URLs (dev and production)

2. **All 3 Endpoints Documented:**
   - ✅ `check_customer_registered` - Check by name
   - ✅ `check_customer_by_id` - Check by ID
   - ✅ `create_customer` - Create new customer

3. **For Each Endpoint:**
   - Description and purpose
   - Request parameters/body
   - Response schemas
   - Example requests and responses
   - Authentication requirements
   - Error responses

4. **Authentication Methods:**
   - Session cookie authentication
   - API Key/Secret authentication

5. **Interactive Features:**
   - "Try it out" button to test APIs directly
   - Request/response examples
   - Schema validation
   - Code generation

---

## 🚀 Using Swagger UI

### 1. Open the Documentation
```
http://erpsite.com:8000/api-docs
```

### 2. Authenticate

**Option A: Using API Key**
1. Click the **"Authorize"** button (🔒 icon)
2. Under **apiKeyAuth**, enter:
   ```
   token YOUR_API_KEY:YOUR_API_SECRET
   ```
3. Click **Authorize**, then **Close**

**Option B: Using Session**
1. Login to ERPNext first: http://erpsite.com:8000
2. The session cookie will be used automatically

### 3. Test Endpoints

1. **Expand an endpoint** (e.g., "Check customer registration by name")
2. Click **"Try it out"**
3. Fill in the parameters (e.g., `customer_name: "Test Customer API"`)
4. Click **"Execute"**
5. See the response below!

---

## 📝 Example Usage in Swagger UI

### Test 1: Check Customer
1. Expand: **GET /api/method/customer_api.api.check_customer_registered**
2. Click **"Try it out"**
3. Enter `customer_name`: `Test Customer API`
4. Click **"Execute"**
5. See response with customer details!

### Test 2: Create Customer
1. Expand: **POST /api/method/customer_api.api.create_customer**
2. Click **"Try it out"**
3. Use the example JSON or modify it:
   ```json
   {
     "customer_name": "Swagger Test Customer",
     "email": "swagger@example.com",
     "mobile": "+1234567890",
     "address_line1": "123 API Street",
     "city": "San Francisco",
     "country": "United States"
   }
   ```
4. Click **"Execute"**
5. See the created customer details!

---

## 🔧 Files Created

```
apps/customer_api/
├── customer_api/
│   ├── openapi.yaml              # OpenAPI specification
│   ├── public/
│   │   └── openapi.yaml          # Public copy (web accessible)
│   └── www/
│       └── api-docs.html         # Swagger UI page
```

---

## 🎨 Customize the Documentation

### Edit the OpenAPI Spec

```bash
nano /home/samudith/frappe-bench/apps/customer_api/customer_api/openapi.yaml
```

After editing:
```bash
# Copy to public folder
cp /home/samudith/frappe-bench/apps/customer_api/customer_api/openapi.yaml \
   /home/samudith/frappe-bench/apps/customer_api/customer_api/public/

# Rebuild
cd /home/samudith/frappe-bench
bench build --app customer_api
```

### Change Server URLs

In `openapi.yaml`, update the `servers` section:
```yaml
servers:
  - url: https://your-production-domain.com
    description: Production server
  - url: http://erpsite.com:8000
    description: Development server
```

---

## 📤 Share the Documentation

### Share the Live URL
```
http://erpsite.com:8000/api-docs
```

### Export the Spec File
```bash
# Download the spec
curl http://erpsite.com:8000/assets/customer_api/openapi.yaml > customer-api-spec.yaml

# Or copy locally
cp /home/samudith/frappe-bench/apps/customer_api/customer_api/openapi.yaml ./
```

### Import to Other Tools

**Postman:**
1. Open Postman
2. Click **Import**
3. Select the `openapi.yaml` file
4. All endpoints will be imported as a collection!

**Insomnia:**
1. Open Insomnia
2. Click **Create** → **Import**
3. Select the YAML file

**API Clients:**
- Use the spec with any OpenAPI-compatible client generator
- Generate SDKs in various languages

---

## 🔗 Integration with Third-Party Tools

### Swagger Hub
1. Go to: https://app.swaggerhub.com/
2. Create account
3. Upload your `openapi.yaml`
4. Share with team, generate documentation

### ReadMe.io
1. Import OpenAPI spec
2. Create beautiful hosted docs
3. Add guides and tutorials

### Stoplight
1. Import spec
2. Create mock servers
3. Add design guidelines

---

## 📚 OpenAPI Features

### Request Examples
- Multiple examples for each endpoint
- Customer found vs not found
- Success vs error responses
- Minimal vs complete requests

### Schema Validation
- Type validation
- Required fields
- Enum values
- Format validation

### Security Schemes
- Session cookie auth
- API key/secret auth
- Clear documentation on how to authenticate

### Response Types
- Success responses (200)
- Unauthorized (401)
- Server errors (500)
- Detailed error schemas

---

## 🎯 Quick Links

| Resource | URL |
|----------|-----|
| **Swagger UI** | http://erpsite.com:8000/api-docs |
| **OpenAPI Spec** | http://erpsite.com:8000/assets/customer_api/openapi.yaml |
| **Online Editor** | https://editor.swagger.io/ |
| **Postman** | https://www.postman.com/ |

---

## 💡 Pro Tips

1. **Use "Try it out"** - Test all endpoints directly in Swagger UI
2. **Export to Postman** - Import the OpenAPI spec into Postman for easier testing
3. **Share with developers** - Send them the Swagger UI link for instant API understanding
4. **Generate client code** - Use Swagger Codegen to generate API clients
5. **Keep it updated** - Update openapi.yaml when you add new endpoints

---

## 🔄 Update After Changes

Whenever you modify the API:

```bash
# 1. Edit the OpenAPI spec
nano /home/samudith/frappe-bench/apps/customer_api/customer_api/openapi.yaml

# 2. Copy to public
cp /home/samudith/frappe-bench/apps/customer_api/customer_api/openapi.yaml \
   /home/samudith/frappe-bench/apps/customer_api/customer_api/public/

# 3. Rebuild (if needed)
cd /home/samudith/frappe-bench
bench build --app customer_api

# 4. Refresh browser
# Visit: http://erpsite.com:8000/api-docs
```

---

## 🎉 Your API is Now Professionally Documented!

✅ Interactive documentation  
✅ Try it out functionality  
✅ Complete request/response examples  
✅ Authentication documentation  
✅ Schema validation  
✅ Export to Postman/Insomnia  
✅ Code generation ready  

**Access it now:** http://erpsite.com:8000/api-docs

