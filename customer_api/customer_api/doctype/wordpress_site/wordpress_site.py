# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WordPressSite(Document):
	def validate(self):
		"""Set the webhook URL automatically"""
		if not self.webhook_url:
			site_url = frappe.utils.get_url()
			self.webhook_url = f"{site_url}/api/method/customer_api.api.woocommerce_webhook_listener"
	
	def on_update(self):
		"""Clear password cache when updated"""
		pass

