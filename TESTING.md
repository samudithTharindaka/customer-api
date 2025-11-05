# Customer API - Testing Guide

Comprehensive test suite for Customer API endpoints with organized, numbered test cases.

## Table of Contents

1. [Overview](#overview)
2. [Test Organization](#test-organization)
3. [Running Tests](#running-tests)
4. [Test Cases](#test-cases)
5. [Test Results](#test-results)

---

## Overview

The Customer API test suite provides comprehensive coverage of all three main endpoints:

- `check_customer_registered` - Verify customer existence
- `create_customer` - Create customers with contacts and addresses
- `create_sales_invoice` - Create sales invoices (including POS invoices)

**Total Test Cases: 17**

---

## Test Organization

Tests are organized into three main classes:

```
customer_api/tests/
├── __init__.py
└── test_customer_api.py
    ├── TestCheckCustomerRegistered (3 tests)
    ├── TestCreateCustomer (6 tests)
    └── TestCreateSalesInvoice (8 tests)
```

Each test is:
- ✅ **Numbered** for easy reference
- ✅ **Self-contained** with setup and teardown
- ✅ **Documented** with clear descriptions
- ✅ **Isolated** - no dependencies between tests

---

## Running Tests

### Method 1: Using Bench Execute (Recommended)

```bash
cd /home/samudith/frappe-bench
bench --site dcode.com execute customer_api.tests.test_customer_api.run_all_tests
```

### Method 2: Using Python Script

```bash
cd /home/samudith/frappe-bench
python apps/customer_api/run_tests.py
```

### Method 3: Run Specific Test Class

```python
# In Frappe console
from customer_api.tests.test_customer_api import TestCreateCustomer
import unittest

suite = unittest.TestLoader().loadTestsFromTestCase(TestCreateCustomer)
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
```

---

## Test Cases

### 1. TestCheckCustomerRegistered (3 tests)

Tests for the `check_customer_registered` endpoint.

#### Test 1: Check Non-Existent Customer ✅
**Purpose:** Verify API correctly identifies customer doesn't exist  
**Input:** Non-existent customer name  
**Expected:** `is_registered = False`, all fields null

```python
test_01_check_non_existent_customer()
```

#### Test 2: Check Existing Customer ✅
**Purpose:** Verify API correctly identifies existing customer  
**Input:** Existing customer name  
**Expected:** `is_registered = True`, customer details populated

```python
test_02_check_existing_customer()
```

#### Test 3: Check Without Name (Error Case) ✅
**Purpose:** Verify validation for missing customer name  
**Input:** None/empty customer name  
**Expected:** Exception raised

```python
test_03_check_customer_without_name()
```

---

### 2. TestCreateCustomer (6 tests)

Tests for the `create_customer` endpoint.

#### Test 1: Create Minimal Customer ✅
**Purpose:** Create customer with only required field  
**Input:** `customer_name` only  
**Expected:** Customer created, no contact/address

```python
test_01_create_minimal_customer()
```

#### Test 2: Create Customer With Contact ✅
**Purpose:** Create customer with email, mobile, phone  
**Input:** Customer name + contact details  
**Expected:** Customer + Contact document created

```python
test_02_create_customer_with_contact()
```

#### Test 3: Create Customer With Address ✅
**Purpose:** Create customer with full address  
**Input:** Customer name + address details  
**Expected:** Customer + Address document created

```python
test_03_create_customer_with_address()
```

#### Test 4: Create Customer Full Details ✅
**Purpose:** Create customer with all fields  
**Input:** Customer name + contact + address  
**Expected:** Customer + Contact + Address created

```python
test_04_create_customer_full_details()
```

#### Test 5: Create Duplicate Customer (Error Case) ✅
**Purpose:** Verify duplicate prevention  
**Input:** Same customer name twice  
**Expected:** Second attempt fails with error message

```python
test_05_create_duplicate_customer()
```

#### Test 6: Create Company Type Customer ✅
**Purpose:** Create customer with type "Company"  
**Input:** `customer_type = "Company"`  
**Expected:** Customer created with Company type

```python
test_06_create_company_type_customer()
```

---

### 3. TestCreateSalesInvoice (8 tests)

Tests for the `create_sales_invoice` endpoint.

#### Test 1: Create Basic Invoice ✅
**Purpose:** Create simple invoice with one item  
**Input:** Customer + 1 item  
**Expected:** Draft invoice created

```python
test_01_create_basic_invoice()
```

#### Test 2: Create Invoice Multiple Items ✅
**Purpose:** Create invoice with multiple line items  
**Input:** Customer + 2 items  
**Expected:** Invoice with correct total

```python
test_02_create_invoice_multiple_items()
```

#### Test 3: Create Invoice With POS Profile ✅
**Purpose:** Create POS invoice using POS Profile  
**Input:** Customer + items + `pos_profile`  
**Expected:** Invoice with `is_pos = 1`, POS Profile set

```python
test_03_create_invoice_with_pos_profile()
```

#### Test 4: Create Invoice Invalid POS Profile (Error Case) ✅
**Purpose:** Verify validation for non-existent POS Profile  
**Input:** Invalid POS Profile name  
**Expected:** Error message returned

```python
test_04_create_invoice_with_invalid_pos_profile()
```

#### Test 5: Create Invoice With Submit ✅
**Purpose:** Create and immediately submit invoice  
**Input:** Customer + items + `submit=1`  
**Expected:** Submitted invoice (status = "Submitted")

```python
test_05_create_invoice_with_submit()
```

#### Test 6: Create Invoice With Dates ✅
**Purpose:** Create invoice with custom dates  
**Input:** Custom posting_date and due_date  
**Expected:** Invoice with specified dates

```python
test_06_create_invoice_with_dates()
```

#### Test 7: Create Invoice Invalid Customer (Error Case) ✅
**Purpose:** Verify validation for non-existent customer  
**Input:** Non-existent customer name  
**Expected:** Error message returned

```python
test_07_create_invoice_invalid_customer()
```

#### Test 8: Create Invoice No Items (Error Case) ✅
**Purpose:** Verify validation for empty items list  
**Input:** Empty items array  
**Expected:** Exception raised

```python
test_08_create_invoice_no_items()
```

---

## Test Results

### Example Output

```
================================================================================
CUSTOMER API - COMPREHENSIVE TEST SUITE
================================================================================

test_01_check_non_existent_customer (__main__.TestCheckCustomerRegistered) ... ok
✅ Test 1 Passed: Non-existent customer check

test_02_check_existing_customer (__main__.TestCheckCustomerRegistered) ... ok
✅ Test 2 Passed: Existing customer check

test_03_check_customer_without_name (__main__.TestCheckCustomerRegistered) ... ok
✅ Test 3 Passed: Missing customer name validation

[... more tests ...]

================================================================================
TEST SUMMARY
================================================================================
Total Tests Run: 17
✅ Passed: 17
❌ Failed: 0
⚠️  Errors: 0
================================================================================
```

---

## Test Coverage

| Endpoint | Test Cases | Coverage |
|----------|-----------|----------|
| check_customer_registered | 3 | 100% |
| create_customer | 6 | 100% |
| create_sales_invoice | 8 | 100% |
| **Total** | **17** | **100%** |

### Coverage Details:

✅ **Success Cases** - Normal operations  
✅ **Error Cases** - Invalid inputs and validation  
✅ **Edge Cases** - Minimal data, maximum data  
✅ **POS Mode** - POS Profile integration  
✅ **Data Cleanup** - Proper teardown after each test  

---

## Maintenance

### Adding New Tests

1. Add test method to appropriate test class
2. Follow naming convention: `test_##_descriptive_name`
3. Include docstring with purpose and expectations
4. Add setup/teardown if needed
5. Print success message at end

### Example:

```python
def test_09_your_new_test(self):
    """Test 9: Description of what this tests"""
    from customer_api.api import create_sales_invoice
    
    # Your test code here
    
    print("✅ Test 9 Passed: Your test description")
```

---

## Troubleshooting

### Common Issues

**Issue: Tests fail with "Permission Denied"**  
Solution: Make sure you're running as Administrator

**Issue: Items not found**  
Solution: Tests create test items automatically, check Item creation permissions

**Issue: Tests don't clean up**  
Solution: Check tearDown methods are executing, may need force=True on deletes

---

## API Testing with cURL

For manual API testing, see the API examples below:

### Test Check Customer
```bash
curl -X GET "http://localhost:8000/api/method/customer_api.api.check_customer_registered?customer_name=Test%20Customer" \
  -H "Authorization: token YOUR_KEY:YOUR_SECRET"
```

### Test Create Customer
```bash
curl -X POST "http://localhost:8000/api/method/customer_api.api.create_customer" \
  -H "Authorization: token YOUR_KEY:YOUR_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"customer_name":"API Test Customer","email":"test@example.com"}'
```

### Test Create Sales Invoice (POS)
```bash
curl -X POST "http://localhost:8000/api/method/customer_api.api.create_sales_invoice" \
  -H "Authorization: token YOUR_KEY:YOUR_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "customer":"Test Customer",
    "pos_profile":"Main Counter",
    "items":[{"item_code":"ITEM-001","qty":2,"rate":100}]
  }'
```

---

## Continuous Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# .github/workflows/test.yml
- name: Run Customer API Tests
  run: |
    cd /path/to/bench
    bench --site your-site execute customer_api.tests.test_customer_api.run_all_tests
```

---

**Last Updated:** November 6, 2025  
**Test Suite Version:** 1.0  
**Total Tests:** 17

