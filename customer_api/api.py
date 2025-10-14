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

