# Postman Collection - Import & Usage Guide

## 📦 Import the Collection

### **File Location:**
```
/home/samudith/frappe-bench/apps/customer_api/Customer_API.postman_collection.json
```

### **Method 1: Import by File**

1. Open Postman
2. Click **"Import"** button (top left)
3. Click **"Upload Files"**
4. Select: `Customer_API.postman_collection.json`
5. Click **"Import"**

### **Method 2: Drag & Drop**

1. Open Postman
2. Drag the `Customer_API.postman_collection.json` file
3. Drop it onto the Postman window
4. Collection imported!

---

## ⚙️ **Setup After Import**

### **Step 1: Configure Variables**

1. **Click on the collection** name ("Customer API for ERPNext")
2. **Go to "Variables" tab**
3. **Update these variables:**

| Variable | Current Value | Update To |
|----------|--------------|-----------|
| `base_url` | http://erpsite.com:8000 | Your ERPNext URL |
| `api_key` | your_api_key_here | Your actual API key |
| `api_secret` | your_api_secret_here | Your actual API secret |
| `customer_name` | Test Customer API | Any existing customer |
| `item_code_1` | ITEM-001 | Your actual item code |
| `item_code_2` | ITEM-002 | Another item code |
| `warehouse` | Stores - C | Your warehouse name |

**How to get API Key:**
1. Login to ERPNext: http://erpsite.com:8000
2. Go to: User → Administrator (or your user)
3. Scroll to "API Access"
4. Click "Generate Keys"
5. Copy API Key and API Secret
6. Paste into Postman variables

---

## 📋 **Collection Structure**

The collection includes **3 folders** with **10 requests**:

### **Folder 1: Customer Availability (1 request)**
- ✅ Check Customer - Exists

### **Folder 2: Customer Creation (5 requests)**
- ✅ Create Customer - Minimal
- ✅ Create Customer - With Email
- ✅ Create Customer - With Contact Info
- ✅ Create Customer - Complete
- ✅ Create Customer - Company Type

### **Folder 3: Sales Invoice (5 requests)**
- ✅ Create Invoice - Simple
- ✅ Create Invoice - Multiple Items
- ✅ Create Invoice - With Taxes & Auto-Submit
- ✅ Create Invoice - Service (No Stock)
- ✅ Create Invoice - Complete Example

### **Folder 4: Authentication (1 request)**
- ✅ Login (for session-based auth)

---

## 🚀 **Using the Collection**

### **Option A: Using API Key (Recommended)**

1. **Set variables:**
   - `api_key` = your key
   - `api_secret` = your secret

2. **Select any request** and click "Send"

3. **Authentication is automatic!** (Uses collection-level auth)

### **Option B: Using Session Cookie**

1. **First, run the "Login" request:**
   - Go to: Authentication → Login
   - Update password in the body
   - Click "Send"
   - Cookie is automatically saved

2. **Then use other requests** (they'll use the session cookie)

---

## 🧪 **Testing Each Endpoint**

### **Test 1: Check Customer**

1. **Open:** Customer Availability → Check Customer - Exists
2. **Update:** customer_name parameter (in Params tab)
3. **Click:** Send
4. **See:** Customer details or not found message

### **Test 2: Create Customer**

1. **Open:** Customer Creation → Create Customer - Complete
2. **Modify:** JSON body (change customer name)
3. **Click:** Send
4. **See:** Customer created with contact_id and address_id

### **Test 3: Create Sales Invoice**

1. **Open:** Sales Invoice → Create Invoice - Simple
2. **Update:** customer and item_code in body
3. **Click:** Send
4. **See:** Invoice created with invoice_id

---

## 💡 **Smart Features**

### **Auto-Generated Variables:**

The collection automatically:
- ✅ Sets today's date for `posting_date`
- ✅ Sets due date to 30 days from now
- ✅ Saves last created customer_id
- ✅ Saves last created invoice_id

### **Pre-configured Auth:**

- Collection-level auth set up
- All requests inherit authentication
- Just update `api_key` and `api_secret` once

### **Example Requests:**

- Multiple scenarios for each endpoint
- Real-world use cases
- Copy and modify as needed

---

## 📝 **Example Usage Flow**

### **Complete Workflow:**

1. **Check if customer exists:**
   ```
   Customer Availability → Check Customer
   ```

2. **If not, create customer:**
   ```
   Customer Creation → Create Customer - Complete
   ```

3. **Create invoice for that customer:**
   ```
   Sales Invoice → Create Invoice - Multiple Items
   ```

4. **Verify in ERPNext UI**

---

## 🎯 **Tips for Using Postman**

### **Tip 1: Use Environments**

Create an environment for dev/production:

1. Click **"Environments"** (top right)
2. Click **"+"** to create new environment
3. Add variables:
   - `base_url`: http://erpsite.com:8000 (dev)
   - `base_url`: https://your-production.com (prod)
4. Switch between environments easily!

### **Tip 2: Save Responses as Examples**

After successful request:
1. Click **"Save Response"**
2. Click **"Save as Example"**
3. Build your own example library!

### **Tip 3: Use Variables**

Replace hardcoded values with variables:
```json
{
  "customer": "{{customer_name}}",
  "items": [...]
}
```

Then update variables instead of editing JSON each time.

### **Tip 4: Use Collection Runner**

Test all requests at once:
1. Click **"..."** on collection
2. Click **"Run collection"**
3. Select requests to run
4. Click **"Run Customer API for ERPNext"**
5. See all results!

---

## 📊 **Collection Variables Reference**

| Variable | Purpose | Example |
|----------|---------|---------|
| `base_url` | Your ERPNext site URL | http://erpsite.com:8000 |
| `api_key` | Your API key | a1b2c3d4e5f6g7h8 |
| `api_secret` | Your API secret | x9y8z7w6v5u4t3s2 |
| `customer_name` | Default customer for tests | Test Customer API |
| `item_code_1` | First item code | ITEM-001 |
| `item_code_2` | Second item code | ITEM-002 |
| `warehouse` | Default warehouse | Stores - C |
| `tax_template` | Tax template name | Sales Taxes - C |
| `payment_terms` | Payment terms | Net 30 |
| `posting_date` | Auto-generated (today) | 2025-10-15 |
| `due_date` | Auto-generated (+30 days) | 2025-11-15 |
| `last_customer_id` | Auto-saved from create | (automatic) |
| `last_invoice_id` | Auto-saved from create | (automatic) |

---

## 🔍 **Verify Import**

After importing, you should see:

```
📁 Customer API for ERPNext
   📂 Customer Availability (1)
   📂 Customer Creation (5)
   📂 Sales Invoice (5)
   📂 Authentication (1)
```

**Total: 12 requests ready to use!**

---

## ✅ **Quick Start Checklist**

- [ ] Import collection to Postman
- [ ] Open collection settings
- [ ] Update `api_key` variable
- [ ] Update `api_secret` variable
- [ ] Update `base_url` if needed
- [ ] Update `item_code_1` with real item
- [ ] Update `warehouse` with real warehouse
- [ ] Test "Check Customer" request
- [ ] Test "Create Customer" request
- [ ] Test "Create Invoice" request

---

## 🎉 **Features Included**

✅ **All 3 endpoints** with multiple examples  
✅ **10 pre-configured requests** ready to use  
✅ **Collection-level authentication** (set once, use everywhere)  
✅ **Smart variables** (auto-generate dates, save IDs)  
✅ **Complete descriptions** for each request  
✅ **Sample responses** showing expected output  
✅ **Easy customization** via variables  

---

## 📚 **Additional Resources**

- **Swagger UI:** http://erpsite.com:8000/api-docs
- **API Documentation:** API_DOCUMENTATION.md
- **Sales Invoice Guide:** SALES_INVOICE_GUIDE.md

---

## 🆘 **Troubleshooting**

### **Issue: "Could not send request"**
**Solution:** Check `base_url` variable points to your running ERPNext instance

### **Issue: "401 Unauthorized"**
**Solution:** 
- Update `api_key` and `api_secret` variables
- Or use Login request first for session auth

### **Issue: "Customer does not exist"**
**Solution:** Update `customer_name` variable to an existing customer

### **Issue: "Item does not exist"**
**Solution:** Update `item_code_1` to an actual item in your ERPNext

---

## 💼 **Ready for Production**

This collection is ready to use for:
- ✅ Development testing
- ✅ Integration testing
- ✅ Client demos
- ✅ Production API calls
- ✅ Team collaboration (share collection)

---

**Import the collection now and start testing your API!** 🚀

File: `/home/samudith/frappe-bench/apps/customer_api/Customer_API.postman_collection.json`

