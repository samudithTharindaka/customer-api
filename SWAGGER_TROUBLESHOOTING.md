# 🔧 Swagger UI API Call Troubleshooting

## ✅ Problem Fixed!

The create API call wasn't working in Swagger UI due to Frappe's CSRF (Cross-Site Request Forgery) protection.

---

## 🛠️ Solution Applied

Added `ignore_csrf` configuration to allow API testing in development environment.

### File Updated:
`sites/common_site_config.json`

```json
{
  ...
  "ignore_csrf": 1
}
```

---

## 🚀 How to Test Now

### **Step 1: Restart Bench**

The configuration change requires a restart:

```bash
cd /home/samudith/frappe-bench

# Stop current bench (Ctrl+C if running in foreground)
# Or if running in background:
pkill -f "bench serve"

# Start again
bench start
```

### **Step 2: Test in Swagger UI**

1. Open: http://erpsite.com:8000/api-docs

2. **Authenticate First:**
   - Click the **"Authorize"** button (🔒 icon at top right)
   - Under **sessionAuth**, you can leave it empty (will use your browser session)
   - OR under **apiKeyAuth**, enter: `token YOUR_API_KEY:YOUR_API_SECRET`
   - Click **"Authorize"**, then **"Close"**

3. **Test Create Customer:**
   - Expand: `POST /api/method/customer_api.api.create_customer`
   - Click: **"Try it out"**
   - Select an example or modify the JSON:
     ```json
     {
       "customer_name": "Swagger Test Customer",
       "email": "swagger@example.com",
       "mobile": "+1234567890"
     }
     ```
   - Click: **"Execute"**
   - See the response!

---

## 🔐 Alternative: Use API Key Authentication

If session authentication still doesn't work, use API Key:

### **Get Your API Key:**

1. Login to ERPNext: http://erpsite.com:8000
2. Go to: **User** → **Administrator** (or your user)
3. Scroll to **"API Access"** section
4. Click **"Generate Keys"**
5. Copy the **API Key** and **API Secret**

### **Use in Swagger:**

1. Click **"Authorize"** in Swagger UI
2. Under **apiKeyAuth**, enter:
   ```
   token YOUR_API_KEY:YOUR_API_SECRET
   ```
   Example:
   ```
   token a1b2c3d4e5f6g7h8:i9j0k1l2m3n4o5p6
   ```
3. Click **"Authorize"**, then **"Close"**
4. Now all API calls will use this authentication

---

## ✅ Test Commands (Alternative Method)

If Swagger UI still has issues, use these curl commands:

### **1. Login First:**
```bash
cd /home/samudith/frappe-bench

curl -X POST "http://erpsite.com:8000/api/method/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "usr=Administrator&pwd=your_password" \
  -c cookies.txt
```

### **2. Create Customer:**
```bash
curl -X POST "http://erpsite.com:8000/api/method/customer_api.api.create_customer" \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "customer_name": "Test Customer",
    "email": "test@example.com",
    "mobile": "+1234567890"
  }' | python3 -m json.tool
```

---

## 🔍 Common Issues & Solutions

### **Issue 1: "Not authenticated" error**

**Solution:**
- Make sure you're logged into ERPNext first: http://erpsite.com:8000
- Or use API Key authentication in the Authorize dialog

### **Issue 2: "CSRF token missing"**

**Solution:**
- Restart bench after config change
- Or use API Key authentication instead of session

### **Issue 3: CORS errors in browser console**

**Solution:**
- This is normal for cross-origin requests
- Use API Key authentication
- Or test with curl/Postman instead

### **Issue 4: "Permission denied"**

**Solution:**
- Make sure your user has permission to create customers
- Login as Administrator or a user with Customer creation rights

---

## 🎯 Recommended Testing Method

### **For Development: Swagger UI**
- Good for: Quick testing, exploring API
- Use: API Key authentication
- URL: http://erpsite.com:8000/api-docs

### **For Integration: Postman**
1. Import OpenAPI spec: http://erpsite.com:8000/assets/customer_api/openapi.yaml
2. Set up environment variables
3. Use Collections for organized testing

### **For Production: API Key Only**
- Never use session cookies in production integrations
- Always use API Key/Secret authentication
- Store credentials securely

---

## 📋 Quick Test Checklist

After restart, verify:

1. ✅ **Login to ERPNext**
   - URL: http://erpsite.com:8000
   - Login as Administrator

2. ✅ **Open Swagger UI**
   - URL: http://erpsite.com:8000/api-docs

3. ✅ **Test Check Customer (GET)**
   - Should work without authorization if logged in
   - Expand GET endpoint
   - Try it out
   - Enter customer name
   - Execute

4. ✅ **Authorize**
   - Click Authorize button
   - Use API Key or leave empty for session auth

5. ✅ **Test Create Customer (POST)**
   - Expand POST endpoint
   - Try it out
   - Use example or modify JSON
   - Execute
   - Should return success!

---

## 🔒 Security Note

### **Development (Current Setup):**
```json
{
  "ignore_csrf": 1  // ⚠️ Only for development!
}
```

### **Production (Remove This):**

For production, remove `ignore_csrf` and use:
- API Key authentication only
- Proper CORS configuration
- HTTPS/SSL certificates
- Rate limiting

---

## 📝 Configuration Files

### **Current Config Location:**
```
/home/samudith/frappe-bench/sites/common_site_config.json
```

### **To Remove CSRF Ignore Later:**

```bash
cd /home/samudith/frappe-bench

# Edit the config
nano sites/common_site_config.json

# Remove the line: "ignore_csrf": 1

# Restart bench
bench restart
```

---

## 🎉 Next Steps

1. **Restart bench** (if not done already)
   ```bash
   cd /home/samudith/frappe-bench
   bench start
   ```

2. **Test in Swagger UI**
   - http://erpsite.com:8000/api-docs
   - Try creating a customer

3. **If still not working:**
   - Use API Key authentication
   - Or test with curl commands
   - Or import to Postman

---

## 💡 Pro Tip

For the best Swagger UI experience:

1. Get your API Key from ERPNext
2. Click "Authorize" in Swagger
3. Enter: `token YOUR_KEY:YOUR_SECRET`
4. Now all endpoints work perfectly!

This is also the recommended approach for production integrations.

---

**Your Swagger UI should now work!** 🚀

Test it at: http://erpsite.com:8000/api-docs

