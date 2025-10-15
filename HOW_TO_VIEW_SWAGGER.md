# 🔍 How to View the New Sales Invoice API in Swagger

## ✅ The API is There! (Verified)

The Sales Invoice endpoint IS in your Swagger documentation. You just need to refresh properly.

---

## 🚀 **Method 1: Hard Refresh Browser (Easiest)**

### **Step-by-Step:**

1. **Open (or go to):**
   ```
   http://erpsite.com:8000/api-docs
   ```

2. **Do a HARD REFRESH:**
   - **Windows/Linux:** Press `Ctrl + Shift + R` or `Ctrl + F5`
   - **Mac:** Press `Cmd + Shift + R`
   - **Or:** Hold `Shift` and click the refresh button

3. **Wait for page to fully reload** (should see "Customer API Documentation" at top)

4. **Scroll down** - You should now see **3 sections/tags:**
   - 📋 **Customer Availability** (green)
   - 👥 **Customer Creation** (green)
   - 💰 **Sales Invoice** (green) ← **THIS IS NEW!**

5. **Click on "Sales Invoice"** to expand it

6. **You'll see:** 
   ```
   POST /api/method/customer_api.api.create_sales_invoice
   Create a new sales invoice
   ```

---

## 🔄 **Method 2: Clear Browser Cache**

If hard refresh doesn't work:

### **Chrome/Edge:**
1. Press `Ctrl + Shift + Delete` (Windows) or `Cmd + Shift + Delete` (Mac)
2. Select "Cached images and files"
3. Click "Clear data"
4. Go back to: http://erpsite.com:8000/api-docs

### **Firefox:**
1. Press `Ctrl + Shift + Delete`
2. Select "Cache"
3. Click "Clear Now"
4. Go back to: http://erpsite.com:8000/api-docs

---

## 🆕 **Method 3: Incognito/Private Window**

1. **Open incognito/private window:**
   - Chrome: `Ctrl + Shift + N`
   - Firefox: `Ctrl + Shift + P`
   - Edge: `Ctrl + Shift + N`

2. **Go to:**
   ```
   http://erpsite.com:8000/api-docs
   ```

3. **Scroll down** to see all 3 endpoints

---

## 📋 **What You Should See**

### **At the Top:**
```
Customer API for ERPNext
v1.0.0

API for Customer Management and Sales in ERPNext

This API provides three main endpoints:
1. Check Customer Availability
2. Create Customer
3. Create Sales Invoice  ← NEW!
```

### **In the Endpoints List:**

```
┌─────────────────────────────────────────────┐
│ Customer Availability                       │
│ ▼ GET /api/method/customer_api.api...      │
│   Check if customer exists by name          │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Customer Creation                           │
│ ▼ POST /api/method/customer_api.api...     │
│   Create a new customer                     │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Sales Invoice  ← NEW!                       │
│ ▼ POST /api/method/customer_api.api...     │
│   Create a new sales invoice                │
└─────────────────────────────────────────────┘
```

---

## 🎯 **To Test the Sales Invoice API:**

Once you can see it:

1. **Click on** "Sales Invoice" section to expand

2. **Click on** the POST endpoint to open it

3. **Click** "Try it out" button (top right of the request section)

4. **You'll see a dropdown** with 4 example options:
   - Simple Invoice
   - Multiple Items
   - With Taxes and Auto-Submit
   - Service Invoice (No Stock)

5. **Select an example** (e.g., "Simple Invoice")

6. **Modify the JSON** if needed (change customer name, item code, etc.)

7. **Click "Execute"** button

8. **See the response** below!

---

## 🔍 **Verify API is Deployed**

Run this command to confirm:

```bash
curl -s "http://erpsite.com:8000/assets/customer_api/openapi.yaml" | grep "create_sales_invoice"
```

**Expected output:**
```
  /api/method/customer_api.api.create_sales_invoice:
```

If you see this, the API IS deployed! Just need to refresh browser.

---

## 🐛 **Troubleshooting**

### **Issue: Still don't see it after hard refresh**

**Solution 1:** Clear all site data
1. Open Developer Tools (F12)
2. Go to "Application" tab (Chrome) or "Storage" tab (Firefox)
3. Right-click on "http://erpsite.com:8000"
4. Click "Clear" or "Delete"
5. Refresh page

**Solution 2:** Check the OpenAPI file directly
```
http://erpsite.com:8000/assets/customer_api/openapi.yaml
```

Search for "create_sales_invoice" - you should find it!

**Solution 3:** Use a different browser
- Try Firefox if you were using Chrome
- Or vice versa

---

## 📱 **Direct URLs**

### **Swagger UI:**
```
http://erpsite.com:8000/api-docs
```

### **OpenAPI Spec (Raw):**
```
http://erpsite.com:8000/assets/customer_api/openapi.yaml
```

### **Search in spec:**
```bash
# In browser, press Ctrl+F and search for:
create_sales_invoice
```

---

## ✅ **Confirmation Checklist**

After hard refresh, you should see:

- [ ] Page title: "Customer API for ERPNext"
- [ ] Description mentions "three main endpoints"
- [ ] Three collapsible sections (tags)
- [ ] "Sales Invoice" section (new!)
- [ ] POST endpoint for create_sales_invoice
- [ ] 4 examples in dropdown
- [ ] "Try it out" button works

---

## 💡 **Why This Happens**

Browsers cache static files (like JavaScript, CSS, and YAML specs) to load pages faster. When we update the OpenAPI spec, your browser might show the old cached version until you do a hard refresh.

**Hard refresh forces the browser to:**
- Skip the cache
- Download fresh files from server
- Load the latest version

---

## 🎬 **Quick Video Guide**

If still having trouble, follow these exact steps:

1. Open: http://erpsite.com:8000/api-docs
2. Press: `Ctrl + Shift + R` (or `Cmd + Shift + R` on Mac)
3. Wait: 2-3 seconds for page to reload
4. Scroll: Down the page
5. Look for: "Sales Invoice" section (green tag)
6. Click: To expand it
7. Success: You see the create_sales_invoice endpoint!

---

## 🆘 **Still Can't See It?**

If you've tried all the above and still can't see it, let me know and I'll help troubleshoot further. But in 99% of cases, a hard refresh (Ctrl+Shift+R) solves it!

---

**The API is deployed and working - just needs a fresh browser cache!** 🎉

