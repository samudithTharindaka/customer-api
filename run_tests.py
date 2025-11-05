#!/usr/bin/env python3
"""
Customer API Test Runner
========================

This script runs all tests for the Customer API endpoints.

Usage:
    python run_tests.py
    
Or from bench:
    bench execute customer_api.run_tests.run_all_tests
"""

import frappe
import sys


def run_all_tests():
	"""
	Execute all Customer API tests
	"""
	# Set test environment
	frappe.init(site="dcode.com")
	frappe.connect()
	frappe.set_user("Administrator")
	
	# Import and run tests
	from customer_api.tests.test_customer_api import run_all_tests as run_tests
	
	result = run_tests()
	
	# Return exit code based on test results
	if result.wasSuccessful():
		print("\n✅ All tests passed successfully!")
		return 0
	else:
		print("\n❌ Some tests failed!")
		return 1


if __name__ == "__main__":
	try:
		exit_code = run_all_tests()
		sys.exit(exit_code)
	except Exception as e:
		print(f"\n❌ Error running tests: {str(e)}")
		import traceback
		traceback.print_exc()
		sys.exit(1)

