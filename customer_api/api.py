import frappe
from frappe import _


@frappe.whitelist(allow_guest=False)
def check_customer_registered(customer_name):
	"""
	Check if a customer is registered in the system.
	
	Args:
		customer_name (str): The name of the customer to check
		
	Returns:
		dict: Dictionary containing customer registration status
			- customer_name: The customer name searched for
			- is_registered: Boolean indicating if customer exists
			- customer_id: The customer ID if registered, else None
			- customer_group: The customer group if registered, else None
			- territory: The territory if registered, else None
	"""
	
	if not customer_name:
		frappe.throw(_("Customer name is required"))
	
	# Check if customer exists
	customer = frappe.db.exists("Customer", {"customer_name": customer_name})
	
	if customer:
		# Get customer details
		customer_doc = frappe.get_doc("Customer", customer)
		
		return {
			"customer_name": customer_name,
			"is_registered": True,
			"customer_id": customer_doc.name,
			"customer_group": customer_doc.customer_group,
			"territory": customer_doc.territory,
			"customer_type": customer_doc.customer_type,
			"disabled": customer_doc.disabled
		}
	else:
		return {
			"customer_name": customer_name,
			"is_registered": False,
			"customer_id": None,
			"customer_group": None,
			"territory": None,
			"customer_type": None,
			"disabled": None
		}


@frappe.whitelist(allow_guest=False)
def create_customer(customer_name, customer_type="Individual", customer_group=None, territory=None, email=None, mobile=None, phone=None, address_line1=None, address_line2=None, city=None, state=None, country=None, pincode=None):
	"""
	Create a new customer in the system.
	
	Args:
		customer_name (str): The name of the customer (required)
		customer_type (str): Type of customer - "Individual" or "Company" (default: "Individual")
		customer_group (str): Customer group (default: from system defaults)
		territory (str): Territory (default: from system defaults)
		email (str): Customer email address (optional)
		mobile (str): Customer mobile number (optional)
		phone (str): Customer phone number (optional)
		address_line1 (str): Address line 1 (optional)
		address_line2 (str): Address line 2 (optional)
		city (str): City (optional)
		state (str): State (optional)
		country (str): Country (optional)
		pincode (str): Postal/ZIP code (optional)
		
	Returns:
		dict: Dictionary containing created customer details
			- success: Boolean indicating success
			- customer_id: The created customer ID
			- customer_name: The customer name
			- message: Success or error message
	"""
	
	try:
		# Validate required fields
		if not customer_name:
			frappe.throw(_("Customer name is required"))
		
		# Check if customer already exists
		existing_customer = frappe.db.exists("Customer", {"customer_name": customer_name})
		if existing_customer:
			return {
				"success": False,
				"customer_id": existing_customer,
				"customer_name": customer_name,
				"message": _("Customer already exists with this name")
			}
		
		# Validate customer type
		if customer_type not in ["Individual", "Company"]:
			frappe.throw(_("Customer type must be 'Individual' or 'Company'"))
		
		# Get default customer group if not provided
		if not customer_group:
			customer_group = frappe.db.get_single_value("Selling Settings", "customer_group")
			if not customer_group:
				customer_group = _("All Customer Groups")
		
		# Get default territory if not provided
		if not territory:
			territory = frappe.db.get_single_value("Selling Settings", "territory")
			if not territory:
				territory = _("All Territories")
		
		# Create customer document
		customer_doc = frappe.get_doc({
			"doctype": "Customer",
			"customer_name": customer_name,
			"customer_type": customer_type,
			"customer_group": customer_group,
			"territory": territory
		})
		
		# Insert the customer
		customer_doc.insert(ignore_permissions=False)
		frappe.db.commit()
		
		# Create contact if email, mobile, or phone is provided
		contact_id = None
		if email or mobile or phone:
			try:
				contact_doc = frappe.get_doc({
					"doctype": "Contact",
					"first_name": customer_name,
					"is_primary_contact": 1
				})
				
				# Add email if provided
				if email:
					contact_doc.append("email_ids", {
						"email_id": email,
						"is_primary": 1
					})
				
				# Add mobile if provided
				if mobile:
					contact_doc.append("phone_nos", {
						"phone": mobile,
						"is_primary_mobile_no": 1
					})
				
				# Add phone if provided
				if phone:
					contact_doc.append("phone_nos", {
						"phone": phone,
						"is_primary_phone": 1 if not mobile else 0
					})
				
				# Link contact to customer
				contact_doc.append("links", {
					"link_doctype": "Customer",
					"link_name": customer_doc.name
				})
				
				contact_doc.insert(ignore_permissions=False)
				frappe.db.commit()
				contact_id = contact_doc.name
				
				# Update customer with primary contact
				customer_doc.customer_primary_contact = contact_id
				customer_doc.save(ignore_permissions=False)
				frappe.db.commit()
				
			except Exception as e:
				# If contact creation fails, log it but don't fail the customer creation
				frappe.log_error(f"Failed to create contact for customer {customer_doc.name}: {str(e)}")
		
		# Create address if address details provided
		address_id = None
		if address_line1 or city or country:
			try:
				# Get default country if not provided
				if not country:
					country = frappe.db.get_single_value("System Settings", "country") or "India"
				
				# Validate that country exists in the system
				if not frappe.db.exists("Country", country):
					# Try to find a default country
					default_country = frappe.db.get_value("Country", filters={}, fieldname="name")
					if default_country:
						country = default_country
				
				address_doc = frappe.get_doc({
					"doctype": "Address",
					"address_title": customer_name,
					"address_type": "Billing",
					"address_line1": address_line1 or "",
					"address_line2": address_line2 or "",
					"city": city or "",
					"state": state or "",
					"country": country,
					"pincode": pincode or ""
				})
				
				# Link address to customer
				address_doc.append("links", {
					"link_doctype": "Customer",
					"link_name": customer_doc.name
				})
				
				address_doc.insert(ignore_permissions=False)
				frappe.db.commit()
				address_id = address_doc.name
			except Exception as e:
				# If address creation fails, log it but don't fail the customer creation
				frappe.log_error(f"Failed to create address for customer {customer_doc.name}: {str(e)}")
		
		return {
			"success": True,
			"customer_id": customer_doc.name,
			"customer_name": customer_doc.customer_name,
			"customer_type": customer_doc.customer_type,
			"customer_group": customer_doc.customer_group,
			"territory": customer_doc.territory,
			"contact_id": contact_id,
			"address_id": address_id,
			"message": _("Customer created successfully")
		}
		
	except frappe.DuplicateEntryError:
		frappe.db.rollback()
		return {
			"success": False,
			"customer_id": None,
			"customer_name": customer_name,
			"message": _("Customer with this name already exists")
		}
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(frappe.get_traceback(), _("Customer Creation Error"))
		return {
			"success": False,
			"customer_id": None,
			"customer_name": customer_name,
			"message": _("Error creating customer: {0}").format(str(e))
		}


@frappe.whitelist(allow_guest=False)
def create_sales_invoice(customer, items, due_date=None, posting_date=None, update_stock=1, 
						set_posting_time=0, company=None, currency=None, taxes_and_charges=None,
						payment_terms_template=None, submit=0, cost_center=None, project=None,
						pos_profile=None):
	"""
	Create a new sales invoice in the system.
	
	Args:
		customer (str): Customer ID or name (required)
		items (list): List of items with item_code, qty, rate, etc. (required)
		due_date (str): Payment due date (optional, defaults to posting_date)
		posting_date (str): Invoice date (optional, defaults to today)
		update_stock (int): Update stock on save (1=Yes, 0=No, default=1)
		set_posting_time (int): Set custom posting time (0 or 1, default=0)
		company (str): Company name (optional, uses default)
		currency (str): Currency (optional, uses customer's default)
		taxes_and_charges (str): Sales Taxes and Charges Template name (optional)
		payment_terms_template (str): Payment Terms Template (optional)
		submit (int): Submit invoice after creation (1=Yes, 0=No, default=0)
		cost_center (str): Default Cost Center (optional)
		project (str): Project name (optional)
		pos_profile (str): POS Profile name (optional, enables POS mode)
		
	Returns:
		dict: Dictionary containing created sales invoice details
			- success: Boolean indicating success
			- invoice_id: The created invoice ID
			- invoice_name: The invoice name/number
			- grand_total: Total invoice amount
			- message: Success or error message
			
	Example items format:
		[
			{
				"item_code": "ITEM-001",
				"qty": 10,
				"rate": 100,
				"warehouse": "Stores - C" (optional)
			},
			{
				"item_code": "ITEM-002",
				"qty": 5,
				"rate": 200
			}
		]
	"""
	
	try:
		# Validate required fields
		if not customer:
			frappe.throw(_("Customer is required"))
		
		if not items or not isinstance(items, list) or len(items) == 0:
			frappe.throw(_("At least one item is required"))
		
		# Parse items if it's a JSON string
		if isinstance(items, str):
			import json
			items = json.loads(items)
		
		# Verify customer exists
		if not frappe.db.exists("Customer", customer):
			return {
				"success": False,
				"invoice_id": None,
				"invoice_name": None,
				"grand_total": 0,
				"message": _("Customer '{0}' does not exist").format(customer)
			}
		
		# Get default company if not provided
		if not company:
			company = frappe.db.get_single_value("Global Defaults", "default_company")
			if not company:
				company = frappe.get_all("Company", limit=1, pluck="name")[0]
		
		# Set posting date to today if not provided
		if not posting_date:
			posting_date = frappe.utils.nowdate()
		
		# Set due date to posting date if not provided
		if not due_date:
			due_date = posting_date
		
		# Create sales invoice document
		invoice_doc = frappe.get_doc({
			"doctype": "Sales Invoice",
			"customer": customer,
			"posting_date": posting_date,
			"due_date": due_date,
			"company": company,
			"update_stock": int(update_stock),
			"set_posting_time": int(set_posting_time)
		})
		
		# Set POS Profile if provided (enables POS mode)
		if pos_profile:
			# Verify POS Profile exists
			if not frappe.db.exists("POS Profile", pos_profile):
				return {
					"success": False,
					"invoice_id": None,
					"invoice_name": None,
					"grand_total": 0,
					"message": _("POS Profile '{0}' does not exist").format(pos_profile)
				}
			invoice_doc.is_pos = 1
			invoice_doc.pos_profile = pos_profile
		
		# Set optional fields
		if currency:
			invoice_doc.currency = currency
		
		if cost_center:
			invoice_doc.cost_center = cost_center
		
		if project:
			invoice_doc.project = project
		
		if payment_terms_template:
			invoice_doc.payment_terms_template = payment_terms_template
		
		if taxes_and_charges:
			invoice_doc.taxes_and_charges = taxes_and_charges
		
		# Add items
		for item in items:
			if not item.get("item_code"):
				frappe.throw(_("Item code is required for all items"))
			
			if not item.get("qty"):
				frappe.throw(_("Quantity is required for item {0}").format(item.get("item_code")))
			
			# Verify item exists
			if not frappe.db.exists("Item", item.get("item_code")):
				frappe.throw(_("Item '{0}' does not exist").format(item.get("item_code")))
			
			item_row = {
				"item_code": item.get("item_code"),
				"qty": float(item.get("qty")),
			}
			
			# Add optional item fields
			if item.get("rate"):
				item_row["rate"] = float(item.get("rate"))
			
			if item.get("warehouse"):
				item_row["warehouse"] = item.get("warehouse")
			
			if item.get("description"):
				item_row["description"] = item.get("description")
			
			if item.get("uom"):
				item_row["uom"] = item.get("uom")
			
			if item.get("conversion_factor"):
				item_row["conversion_factor"] = float(item.get("conversion_factor"))
			
			if item.get("discount_percentage"):
				item_row["discount_percentage"] = float(item.get("discount_percentage"))
			
			if item.get("cost_center"):
				item_row["cost_center"] = item.get("cost_center")
			
			invoice_doc.append("items", item_row)
		
		# Insert the invoice
		invoice_doc.insert(ignore_permissions=False)
		
		# Get taxes if template is provided
		if taxes_and_charges:
			invoice_doc.set_missing_values()
		
		# Calculate totals
		invoice_doc.calculate_taxes_and_totals()
		invoice_doc.save()
		frappe.db.commit()
		
		result = {
			"success": True,
			"invoice_id": invoice_doc.name,
			"invoice_name": invoice_doc.name,
			"customer": invoice_doc.customer,
			"posting_date": str(invoice_doc.posting_date),
			"due_date": str(invoice_doc.due_date),
			"total_qty": invoice_doc.total_qty,
			"total": invoice_doc.total,
			"grand_total": invoice_doc.grand_total,
			"outstanding_amount": invoice_doc.outstanding_amount,
			"status": invoice_doc.status,
			"update_stock": invoice_doc.update_stock,
			"is_pos": invoice_doc.is_pos,
			"pos_profile": invoice_doc.pos_profile if pos_profile else None,
			"message": _("Sales invoice created successfully")
		}
		
		# Submit if requested
		if int(submit) == 1:
			try:
				invoice_doc.submit()
				frappe.db.commit()
				result["status"] = "Submitted"
				result["message"] = _("Sales invoice created and submitted successfully")
			except Exception as e:
				# If submit fails, return draft invoice info with error
				result["message"] = _("Invoice created as draft. Submit failed: {0}").format(str(e))
				result["submit_error"] = str(e)
		
		return result
		
	except frappe.exceptions.ValidationError as e:
		frappe.db.rollback()
		return {
			"success": False,
			"invoice_id": None,
			"invoice_name": None,
			"grand_total": 0,
			"message": _("Validation error: {0}").format(str(e))
		}
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(frappe.get_traceback(), _("Sales Invoice Creation Error"))
		return {
			"success": False,
			"invoice_id": None,
			"invoice_name": None,
			"grand_total": 0,
			"message": _("Error creating sales invoice: {0}").format(str(e))
		}

