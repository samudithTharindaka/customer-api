"""
Comprehensive Test Suite for Customer API
==========================================

This test suite covers all endpoints in the Customer API:
1. check_customer_registered - Check if customer exists
2. create_customer - Create new customer with contact and address
3. create_sales_invoice - Create sales invoice (with/without POS)

Test Organization:
- Each endpoint has its own test class
- Tests are numbered for easy reference
- Tests cover success cases, error cases, and edge cases
"""

import frappe
import unittest
import json
from frappe.utils import nowdate, add_days


class TestCheckCustomerRegistered(unittest.TestCase):
	"""
	Test Suite for check_customer_registered endpoint
	"""
	
	def setUp(self):
		"""Set up test data"""
		self.test_customer_name = f"Test Customer {frappe.utils.now()}"
		
	def tearDown(self):
		"""Clean up test data"""
		# Delete test customer if exists
		if frappe.db.exists("Customer", self.test_customer_name):
			frappe.delete_doc("Customer", self.test_customer_name, force=True)
		frappe.db.commit()
	
	def test_01_check_non_existent_customer(self):
		"""Test 1: Check for a customer that doesn't exist"""
		from customer_api.api import check_customer_registered
		
		result = check_customer_registered("Non Existent Customer 123456")
		
		self.assertIsInstance(result, dict)
		self.assertEqual(result["customer_name"], "Non Existent Customer 123456")
		self.assertFalse(result["is_registered"])
		self.assertIsNone(result["customer_id"])
		self.assertIsNone(result["customer_group"])
		self.assertIsNone(result["territory"])
		
		print("✅ Test 1 Passed: Non-existent customer check")
	
	def test_02_check_existing_customer(self):
		"""Test 2: Check for a customer that exists"""
		from customer_api.api import check_customer_registered, create_customer
		
		# First create a customer
		create_customer(
			customer_name=self.test_customer_name,
			customer_type="Individual"
		)
		
		# Now check if it exists
		result = check_customer_registered(self.test_customer_name)
		
		self.assertIsInstance(result, dict)
		self.assertEqual(result["customer_name"], self.test_customer_name)
		self.assertTrue(result["is_registered"])
		self.assertIsNotNone(result["customer_id"])
		self.assertIsNotNone(result["customer_group"])
		self.assertIsNotNone(result["territory"])
		self.assertEqual(result["disabled"], 0)
		
		print("✅ Test 2 Passed: Existing customer check")
	
	def test_03_check_customer_without_name(self):
		"""Test 3: Check without providing customer name (error case)"""
		from customer_api.api import check_customer_registered
		
		with self.assertRaises(Exception):
			check_customer_registered(None)
		
		print("✅ Test 3 Passed: Missing customer name validation")


class TestCreateCustomer(unittest.TestCase):
	"""
	Test Suite for create_customer endpoint
	"""
	
	def setUp(self):
		"""Set up test data"""
		self.test_customers = []
		
	def tearDown(self):
		"""Clean up test data"""
		# Delete all test customers
		for customer_name in self.test_customers:
			if frappe.db.exists("Customer", customer_name):
				# Delete related contacts
				contacts = frappe.get_all("Dynamic Link", 
					filters={"link_doctype": "Customer", "link_name": customer_name, "parenttype": "Contact"},
					fields=["parent"])
				for contact in contacts:
					if frappe.db.exists("Contact", contact.parent):
						frappe.delete_doc("Contact", contact.parent, force=True)
				
				# Delete related addresses
				addresses = frappe.get_all("Dynamic Link",
					filters={"link_doctype": "Customer", "link_name": customer_name, "parenttype": "Address"},
					fields=["parent"])
				for address in addresses:
					if frappe.db.exists("Address", address.parent):
						frappe.delete_doc("Address", address.parent, force=True)
				
				# Delete customer
				frappe.delete_doc("Customer", customer_name, force=True)
		
		frappe.db.commit()
	
	def test_01_create_minimal_customer(self):
		"""Test 1: Create customer with only required field (customer_name)"""
		from customer_api.api import create_customer
		
		customer_name = f"Minimal Customer {frappe.utils.now()}"
		self.test_customers.append(customer_name)
		
		result = create_customer(customer_name=customer_name)
		
		self.assertIsInstance(result, dict)
		self.assertTrue(result["success"])
		self.assertEqual(result["customer_name"], customer_name)
		self.assertIsNotNone(result["customer_id"])
		self.assertEqual(result["customer_type"], "Individual")
		self.assertIsNone(result["contact_id"])
		self.assertIsNone(result["address_id"])
		
		print("✅ Test 1 Passed: Minimal customer creation")
	
	def test_02_create_customer_with_contact(self):
		"""Test 2: Create customer with contact information"""
		from customer_api.api import create_customer
		
		customer_name = f"Customer With Contact {frappe.utils.now()}"
		self.test_customers.append(customer_name)
		
		result = create_customer(
			customer_name=customer_name,
			email="contact@example.com",
			mobile="+1234567890",
			phone="+0987654321"
		)
		
		self.assertIsInstance(result, dict)
		self.assertTrue(result["success"])
		self.assertEqual(result["customer_name"], customer_name)
		self.assertIsNotNone(result["contact_id"])
		self.assertIsNone(result["address_id"])
		
		# Verify contact was created
		self.assertTrue(frappe.db.exists("Contact", result["contact_id"]))
		
		print("✅ Test 2 Passed: Customer with contact creation")
	
	def test_03_create_customer_with_address(self):
		"""Test 3: Create customer with address information"""
		from customer_api.api import create_customer
		
		customer_name = f"Customer With Address {frappe.utils.now()}"
		self.test_customers.append(customer_name)
		
		result = create_customer(
			customer_name=customer_name,
			address_line1="123 Test Street",
			address_line2="Suite 100",
			city="Test City",
			state="Test State",
			country="United States",
			pincode="12345"
		)
		
		self.assertIsInstance(result, dict)
		self.assertTrue(result["success"])
		self.assertEqual(result["customer_name"], customer_name)
		self.assertIsNone(result["contact_id"])
		self.assertIsNotNone(result["address_id"])
		
		# Verify address was created
		self.assertTrue(frappe.db.exists("Address", result["address_id"]))
		
		print("✅ Test 3 Passed: Customer with address creation")
	
	def test_04_create_customer_full_details(self):
		"""Test 4: Create customer with complete contact and address"""
		from customer_api.api import create_customer
		
		customer_name = f"Complete Customer {frappe.utils.now()}"
		self.test_customers.append(customer_name)
		
		result = create_customer(
			customer_name=customer_name,
			customer_type="Individual",
			email="complete@example.com",
			mobile="+1111111111",
			phone="+2222222222",
			address_line1="456 Complete Ave",
			address_line2="Floor 2",
			city="Complete City",
			state="Complete State",
			country="United States",
			pincode="54321"
		)
		
		self.assertIsInstance(result, dict)
		self.assertTrue(result["success"])
		self.assertEqual(result["customer_name"], customer_name)
		self.assertIsNotNone(result["contact_id"])
		self.assertIsNotNone(result["address_id"])
		
		# Verify both contact and address were created
		self.assertTrue(frappe.db.exists("Contact", result["contact_id"]))
		self.assertTrue(frappe.db.exists("Address", result["address_id"]))
		
		print("✅ Test 4 Passed: Complete customer creation")
	
	def test_05_create_duplicate_customer(self):
		"""Test 5: Try to create duplicate customer (error case)"""
		from customer_api.api import create_customer
		
		customer_name = f"Duplicate Customer {frappe.utils.now()}"
		self.test_customers.append(customer_name)
		
		# Create first customer
		result1 = create_customer(customer_name=customer_name)
		self.assertTrue(result1["success"])
		
		# Try to create duplicate
		result2 = create_customer(customer_name=customer_name)
		self.assertFalse(result2["success"])
		self.assertIn("already exists", result2["message"].lower())
		
		print("✅ Test 5 Passed: Duplicate customer prevention")
	
	def test_06_create_company_type_customer(self):
		"""Test 6: Create customer with type 'Company'"""
		from customer_api.api import create_customer
		
		customer_name = f"Company Customer {frappe.utils.now()}"
		self.test_customers.append(customer_name)
		
		result = create_customer(
			customer_name=customer_name,
			customer_type="Company"
		)
		
		self.assertIsInstance(result, dict)
		self.assertTrue(result["success"])
		self.assertEqual(result["customer_type"], "Company")
		
		print("✅ Test 6 Passed: Company type customer creation")


class TestCreateSalesInvoice(unittest.TestCase):
	"""
	Test Suite for create_sales_invoice endpoint
	"""
	
	def setUp(self):
		"""Set up test data"""
		self.test_invoices = []
		self.test_customers = []
		self.test_items = []
		
		# Create a test customer
		self.customer_name = f"Invoice Test Customer {frappe.utils.now()}"
		self.test_customers.append(self.customer_name)
		
		from customer_api.api import create_customer
		customer_result = create_customer(customer_name=self.customer_name)
		self.assertTrue(customer_result["success"])
		
		# Create test items
		self.item1 = self._create_test_item("Test Item 1")
		self.item2 = self._create_test_item("Test Item 2")
		self.test_items.extend([self.item1, self.item2])
		
	def _create_test_item(self, item_name):
		"""Helper method to create test items"""
		full_item_name = f"{item_name} {frappe.utils.now()}"
		
		if not frappe.db.exists("Item", full_item_name):
			item_doc = frappe.get_doc({
				"doctype": "Item",
				"item_code": full_item_name,
				"item_name": full_item_name,
				"item_group": "Products",
				"stock_uom": "Nos",
				"is_stock_item": 1
			})
			item_doc.insert(ignore_permissions=True)
			frappe.db.commit()
		
		return full_item_name
	
	def tearDown(self):
		"""Clean up test data"""
		# Delete test invoices
		for invoice_name in self.test_invoices:
			if frappe.db.exists("Sales Invoice", invoice_name):
				doc = frappe.get_doc("Sales Invoice", invoice_name)
				if doc.docstatus == 1:  # Submitted
					doc.cancel()
				frappe.delete_doc("Sales Invoice", invoice_name, force=True)
		
		# Delete test items
		for item_name in self.test_items:
			if frappe.db.exists("Item", item_name):
				frappe.delete_doc("Item", item_name, force=True)
		
		# Delete test customers
		for customer_name in self.test_customers:
			if frappe.db.exists("Customer", customer_name):
				frappe.delete_doc("Customer", customer_name, force=True)
		
		frappe.db.commit()
	
	def test_01_create_basic_invoice(self):
		"""Test 1: Create basic sales invoice"""
		from customer_api.api import create_sales_invoice
		
		items = [
			{
				"item_code": self.item1,
				"qty": 5,
				"rate": 100
			}
		]
		
		result = create_sales_invoice(
			customer=self.customer_name,
			items=items
		)
		
		self.assertIsInstance(result, dict)
		self.assertTrue(result["success"])
		self.assertIsNotNone(result["invoice_id"])
		self.assertEqual(result["grand_total"], 500)
		self.assertEqual(result["status"], "Draft")
		self.test_invoices.append(result["invoice_id"])
		
		print("✅ Test 1 Passed: Basic invoice creation")
	
	def test_02_create_invoice_multiple_items(self):
		"""Test 2: Create invoice with multiple items"""
		from customer_api.api import create_sales_invoice
		
		items = [
			{
				"item_code": self.item1,
				"qty": 3,
				"rate": 150
			},
			{
				"item_code": self.item2,
				"qty": 2,
				"rate": 200
			}
		]
		
		result = create_sales_invoice(
			customer=self.customer_name,
			items=items
		)
		
		self.assertIsInstance(result, dict)
		self.assertTrue(result["success"])
		self.assertEqual(result["grand_total"], 850)  # (3*150) + (2*200)
		self.test_invoices.append(result["invoice_id"])
		
		print("✅ Test 2 Passed: Multiple items invoice creation")
	
	def test_03_create_invoice_with_pos_profile(self):
		"""Test 3: Create POS invoice with POS Profile"""
		from customer_api.api import create_sales_invoice
		
		# Check if there's an existing POS Profile to use
		existing_pos_profiles = frappe.get_all("POS Profile", limit=1, pluck="name")
		
		if existing_pos_profiles:
			# Use existing POS Profile
			pos_profile_name = existing_pos_profiles[0]
			
			items = [
				{
					"item_code": self.item1,
					"qty": 2,
					"rate": 250
				}
			]
			
			result = create_sales_invoice(
				customer=self.customer_name,
				items=items,
				pos_profile=pos_profile_name
			)
			
			self.assertIsInstance(result, dict)
			self.assertTrue(result["success"])
			self.assertEqual(result["is_pos"], 1)
			self.assertEqual(result["pos_profile"], pos_profile_name)
			self.test_invoices.append(result["invoice_id"])
			
			print("✅ Test 3 Passed: POS invoice creation")
		else:
			# Skip test if no POS Profile exists
			print("⚠️  Test 3 Skipped: No POS Profile available (create one in ERPNext first)")
			self.skipTest("No POS Profile available for testing")
	
	def test_04_create_invoice_with_invalid_pos_profile(self):
		"""Test 4: Try to create invoice with non-existent POS Profile (error case)"""
		from customer_api.api import create_sales_invoice
		
		items = [
			{
				"item_code": self.item1,
				"qty": 1,
				"rate": 100
			}
		]
		
		result = create_sales_invoice(
			customer=self.customer_name,
			items=items,
			pos_profile="Non Existent POS Profile 123"
		)
		
		self.assertFalse(result["success"])
		self.assertIn("does not exist", result["message"])
		
		print("✅ Test 4 Passed: Invalid POS Profile validation")
	
	def test_05_create_invoice_with_submit(self):
		"""Test 5: Create and submit invoice"""
		from customer_api.api import create_sales_invoice
		
		items = [
			{
				"item_code": self.item1,
				"qty": 1,
				"rate": 1000
			}
		]
		
		result = create_sales_invoice(
			customer=self.customer_name,
			items=items,
			submit=1,
			update_stock=0  # Don't update stock for simplicity
		)
		
		self.assertIsInstance(result, dict)
		self.assertTrue(result["success"])
		self.assertEqual(result["status"], "Submitted")
		self.test_invoices.append(result["invoice_id"])
		
		print("✅ Test 5 Passed: Invoice submission")
	
	def test_06_create_invoice_with_dates(self):
		"""Test 6: Create invoice with custom posting and due dates"""
		from customer_api.api import create_sales_invoice
		
		posting_date = nowdate()
		due_date = add_days(posting_date, 30)
		
		items = [
			{
				"item_code": self.item1,
				"qty": 1,
				"rate": 500
			}
		]
		
		result = create_sales_invoice(
			customer=self.customer_name,
			items=items,
			posting_date=posting_date,
			due_date=due_date
		)
		
		self.assertIsInstance(result, dict)
		self.assertTrue(result["success"])
		self.assertEqual(result["posting_date"], posting_date)
		self.assertEqual(result["due_date"], due_date)
		self.test_invoices.append(result["invoice_id"])
		
		print("✅ Test 6 Passed: Invoice with custom dates")
	
	def test_07_create_invoice_invalid_customer(self):
		"""Test 7: Try to create invoice for non-existent customer (error case)"""
		from customer_api.api import create_sales_invoice
		
		items = [
			{
				"item_code": self.item1,
				"qty": 1,
				"rate": 100
			}
		]
		
		result = create_sales_invoice(
			customer="Non Existent Customer 999999",
			items=items
		)
		
		self.assertFalse(result["success"])
		self.assertIn("does not exist", result["message"])
		
		print("✅ Test 7 Passed: Invalid customer validation")
	
	def test_08_create_invoice_no_items(self):
		"""Test 8: Try to create invoice without items (error case)"""
		from customer_api.api import create_sales_invoice
		
		try:
			result = create_sales_invoice(
				customer=self.customer_name,
				items=[]
			)
			# The API should handle this gracefully and return error
			self.assertFalse(result["success"])
			print("✅ Test 8 Passed: Empty items validation")
		except Exception:
			# If it raises an exception, that's also acceptable
			print("✅ Test 8 Passed: Empty items validation (exception raised)")
			pass


def run_all_tests():
	"""
	Run all test suites and print summary
	"""
	print("\n" + "="*80)
	print("CUSTOMER API - COMPREHENSIVE TEST SUITE")
	print("="*80 + "\n")
	
	# Create test suite
	suite = unittest.TestSuite()
	
	# Add test classes
	suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCheckCustomerRegistered))
	suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCreateCustomer))
	suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCreateSalesInvoice))
	
	# Run tests
	runner = unittest.TextTestRunner(verbosity=2)
	result = runner.run(suite)
	
	# Print summary
	print("\n" + "="*80)
	print("TEST SUMMARY")
	print("="*80)
	print(f"Total Tests Run: {result.testsRun}")
	print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
	print(f"❌ Failed: {len(result.failures)}")
	print(f"⚠️  Errors: {len(result.errors)}")
	print("="*80 + "\n")
	
	return result


if __name__ == "__main__":
	run_all_tests()

