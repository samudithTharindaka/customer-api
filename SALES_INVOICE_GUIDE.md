# Sales Invoice API Guide

## Overview

The Sales Invoice endpoint allows you to create sales invoices programmatically with automatic inventory management.

---

## 🎯 **Inventory Management - Automatic!**

### **When `update_stock=1` (Default):**

ERPNext automatically handles:

✅ **Stock Deduction** - Decreases inventory quantities  
✅ **Stock Ledger Entries** - Creates complete audit trail  
✅ **Item Valuation** - Updates FIFO/Moving Average costs  
✅ **Accounting Entries** - Creates GL entries automatically:
   - Debit: Accounts Receivable
   - Credit: Sales
   - Debit: Cost of Goods Sold (COGS)
   - Credit: Stock Asset

✅ **Real-time Updates** - Inventory updated immediately  
✅ **Serial/Batch Numbers** - Handled if items use them  

### **When `update_stock=0`:**

- Invoice created without affecting inventory
- Stock updated separately via Delivery Note
- Useful for services or manual delivery tracking

---

## 📡 **API Endpoint**

**Endpoint:** `POST /api/method/customer_api.api.create_sales_invoice`

**Authentication:** Required (API Key or Session)

---

## 📋 **Parameters**

### **Required Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `customer` | string | Customer ID or name |
| `items` | array | List of items to invoice (see format below) |

### **Optional Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `posting_date` | string | Today | Invoice date (YYYY-MM-DD) |
| `due_date` | string | posting_date | Payment due date (YYYY-MM-DD) |
| `update_stock` | integer | 1 | Update inventory (1=Yes, 0=No) |
| `submit` | integer | 0 | Submit invoice (1=Yes, 0=No draft) |
| `company` | string | Default | Company name |
| `currency` | string | Customer's | Currency code |
| `taxes_and_charges` | string | None | Sales Taxes Template name |
| `payment_terms_template` | string | None | Payment Terms Template |
| `cost_center` | string | None | Default Cost Center |
| `project` | string | None | Project name |

---

## 🛒 **Items Format**

### **Required Item Fields:**

```json
{
  "item_code": "ITEM-001",  // Required
  "qty": 10                 // Required
}
```

### **Optional Item Fields:**

```json
{
  "item_code": "ITEM-001",
  "qty": 10,
  "rate": 100,                    // Price per unit
  "warehouse": "Stores - C",      // Warehouse to deduct from
  "description": "Custom desc",   // Override default
  "uom": "Box",                  // Unit of measure
  "discount_percentage": 10,      // Discount %
  "cost_center": "Main - C"      // Item-level cost center
}
```

---

## 📝 **Complete Examples**

### **Example 1: Simple Invoice (Auto Stock Update)**

```bash
curl -X POST "http://erpsite.com:8000/api/method/customer_api.api.create_sales_invoice" \
  -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "customer": "John Doe",
    "items": [
      {
        "item_code": "ITEM-001",
        "qty": 5,
        "rate": 100
      }
    ]
  }'
```

**What Happens:**
- ✅ Invoice created for $500 (5 × $100)
- ✅ Stock deducted: 5 units of ITEM-001
- ✅ Invoice saved as Draft
- ✅ Ready for payment

---

### **Example 2: Invoice with Multiple Items**

```bash
curl -X POST "http://erpsite.com:8000/api/method/customer_api.api.create_sales_invoice" \
  -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "customer": "Jane Smith",
    "items": [
      {
        "item_code": "LAPTOP-HP",
        "qty": 2,
        "rate": 800,
        "warehouse": "Main Store - C"
      },
      {
        "item_code": "MOUSE-WIRELESS",
        "qty": 2,
        "rate": 25,
        "warehouse": "Main Store - C"
      }
    ],
    "posting_date": "2025-10-15",
    "due_date": "2025-11-15"
  }'
```

**Result:**
- 2 Laptops @ $800 = $1,600
- 2 Mice @ $25 = $50
- **Total: $1,650**
- Stock deducted from "Main Store - C"

---

### **Example 3: Invoice with Taxes (Auto-Submit)**

```bash
curl -X POST "http://erpsite.com:8000/api/method/customer_api.api.create_sales_invoice" \
  -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "customer": "ACME Corporation",
    "items": [
      {
        "item_code": "SERVICE-CONSULTING",
        "qty": 40,
        "rate": 150,
        "uom": "Hour"
      }
    ],
    "posting_date": "2025-10-15",
    "due_date": "2025-10-30",
    "taxes_and_charges": "Sales Taxes - C",
    "payment_terms_template": "30 Days",
    "update_stock": 0,
    "submit": 1
  }'
```

**Features:**
- Service item (no stock update)
- Taxes applied automatically
- Payment terms: 30 days
- **Auto-submitted** (no draft)

---

### **Example 4: Complete Invoice**

```json
{
  "customer": "Production Test Customer",
  "posting_date": "2025-10-15",
  "due_date": "2025-11-15",
  "items": [
    {
      "item_code": "WIDGET-A",
      "qty": 100,
      "rate": 50,
      "warehouse": "Finished Goods - C",
      "discount_percentage": 5
    },
    {
      "item_code": "WIDGET-B",
      "qty": 50,
      "rate": 75,
      "warehouse": "Finished Goods - C"
    }
  ],
  "taxes_and_charges": "VAT 20% - C",
  "cost_center": "Main - C",
  "project": "Project Alpha",
  "update_stock": 1,
  "submit": 1
}
```

**What Gets Created:**
- Invoice with 2 items
- Total before discount: $8,750
- Discount on Widget-A: 5%
- VAT 20% applied
- Stock deducted from "Finished Goods - C"
- Invoice auto-submitted
- Ready for payment tracking

---

## 📊 **Response Format**

### **Success Response:**

```json
{
  "message": {
    "success": true,
    "invoice_id": "SINV-2025-00123",
    "invoice_name": "SINV-2025-00123",
    "customer": "Production Test Customer",
    "posting_date": "2025-10-15",
    "due_date": "2025-11-15",
    "total_qty": 150,
    "total": 8512.5,
    "grand_total": 10215.0,
    "outstanding_amount": 10215.0,
    "status": "Submitted",
    "update_stock": 1,
    "message": "Sales invoice created and submitted successfully"
  }
}
```

### **Error Response:**

```json
{
  "message": {
    "success": false,
    "invoice_id": null,
    "invoice_name": null,
    "grand_total": 0,
    "message": "Customer 'Unknown Customer' does not exist"
  }
}
```

---

## 🔄 **Inventory Updates Explained**

### **When Invoice is Created (Draft):**
```
update_stock=1:
  ├─ Stock Reserved (soft reservation)
  ├─ Stock Ledger Entry created
  └─ Available qty shows deduction
```

### **When Invoice is Submitted:**
```
update_stock=1:
  ├─ Stock permanently deducted
  ├─ GL Entries created
  │   ├─ Dr: Accounts Receivable
  │   ├─ Cr: Sales
  │   ├─ Dr: Cost of Goods Sold
  │   └─ Cr: Stock in Hand
  ├─ Item valuation updated
  └─ Stock balance reduced
```

### **Stock Ledger Example:**

After creating invoice with 5 units of ITEM-001:

| Date | Item | Qty | Balance | Voucher |
|------|------|-----|---------|---------|
| 2025-10-15 | ITEM-001 | -5 | 45 | SINV-2025-00123 |

---

## ⚠️ **Important Notes**

### **Stock Management:**

1. **Warehouse Required:** If `update_stock=1`, each item should specify a warehouse
2. **Sufficient Stock:** Ensure items have enough stock in the warehouse
3. **Item Configuration:** Items must have "Maintain Stock" enabled
4. **Serial/Batch Items:** Automatically handled if configured

### **Permissions:**

User needs:
- ✅ Create permission on Sales Invoice
- ✅ Write permission on Stock Ledger Entry (if update_stock=1)
- ✅ Submit permission (if submit=1)

### **Best Practices:**

1. **Test in Draft First:** Use `submit=0` initially
2. **Specify Warehouse:** Always include warehouse for stock items
3. **Verify Stock:** Check stock availability before creating invoice
4. **Use Transactions:** Invoice creation is atomic (all or nothing)
5. **Handle Errors:** Check `success` field in response

---

## 🧪 **Testing**

### **Test 1: Create Draft Invoice**

```bash
cd /home/samudith/frappe-bench

curl -X POST "http://erpsite.com:8000/api/method/customer_api.api.create_sales_invoice" \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "customer": "Test Customer API",
    "items": [
      {"item_code": "YOUR_ITEM_CODE", "qty": 1, "rate": 100}
    ]
  }' | python3 -m json.tool
```

### **Test 2: Check Stock Before/After**

```python
# In Frappe console
import frappe

# Check stock before
stock_before = frappe.db.get_value(
    "Bin",
    {"item_code": "YOUR_ITEM_CODE", "warehouse": "Stores - C"},
    "actual_qty"
)
print(f"Stock before: {stock_before}")

# Create invoice via API...

# Check stock after
stock_after = frappe.db.get_value(
    "Bin",
    {"item_code": "YOUR_ITEM_CODE", "warehouse": "Stores - C"},
    "actual_qty"
)
print(f"Stock after: {stock_after}")
print(f"Difference: {stock_before - stock_after}")
```

---

## 🎯 **Use Cases**

### **E-commerce Integration:**
```python
# When order is placed on website
create_sales_invoice(
    customer=customer_id,
    items=cart_items,
    update_stock=1,    # Deduct inventory
    submit=1,          # Auto-submit
    taxes_and_charges="Online Sales Tax"
)
```

### **POS/Retail:**
```python
# Walk-in customer purchase
create_sales_invoice(
    customer=customer_id,
    items=scanned_items,
    update_stock=1,
    submit=1,
    payment_terms_template="Immediate"
)
```

### **Wholesale:**
```python
# B2B order
create_sales_invoice(
    customer=wholesale_customer,
    items=bulk_items,
    update_stock=1,
    submit=0,  # Review before submission
    payment_terms_template="Net 30"
)
```

---

## 📚 **Related Endpoints**

Your API now has **3 endpoints**:

1. **Check Customer** - Verify customer exists
2. **Create Customer** - Add new customers
3. **Create Sales Invoice** - Bill customers (NEW!)

### **Complete Workflow Example:**

```python
# 1. Check if customer exists
response = check_customer("John Doe")

# 2. If not, create customer
if not response["is_registered"]:
    create_customer(
        customer_name="John Doe",
        email="john@example.com"
    )

# 3. Create invoice
create_sales_invoice(
    customer="John Doe",
    items=[
        {"item_code": "ITEM-001", "qty": 5, "rate": 100}
    ],
    update_stock=1,
    submit=1
)
```

---

## ✅ **Advantages of This Endpoint**

1. ✅ **Automatic Inventory** - No manual stock entries needed
2. ✅ **Automatic Accounting** - GL entries created automatically
3. ✅ **Atomic Transactions** - All or nothing (rollback on error)
4. ✅ **Validation** - ERPNext validates everything
5. ✅ **Flexible** - Draft or submit, with/without stock update
6. ✅ **Complete** - Handles taxes, discounts, payment terms
7. ✅ **Integrated** - Works with ERPNext reports and dashboards

---

## 🚀 **Next Steps**

1. Test the endpoint with sample data
2. Verify stock deductions in ERPNext
3. Check accounting entries
4. Update Swagger documentation
5. Add to your integration

---

**The inventory is handled automatically by ERPNext!** 🎉

Just set `update_stock=1` and ERPNext takes care of everything - stock ledger, valuation, accounting, and reporting!

