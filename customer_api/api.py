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
def check_customer_by_id(customer_id):
	"""
	Check if a customer exists by customer ID.
	
	Args:
		customer_id (str): The customer ID to check
		
	Returns:
		dict: Dictionary containing customer registration status
	"""
	
	if not customer_id:
		frappe.throw(_("Customer ID is required"))
	
	# Check if customer exists
	if frappe.db.exists("Customer", customer_id):
		customer_doc = frappe.get_doc("Customer", customer_id)
		
		return {
			"customer_id": customer_id,
			"is_registered": True,
			"customer_name": customer_doc.customer_name,
			"customer_group": customer_doc.customer_group,
			"territory": customer_doc.territory,
			"customer_type": customer_doc.customer_type,
			"disabled": customer_doc.disabled
		}
	else:
		return {
			"customer_id": customer_id,
			"is_registered": False,
			"customer_name": None,
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

