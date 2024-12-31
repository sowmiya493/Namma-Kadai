import frappe
from frappe.model.document import Document

class Company(Document):
    def validate(self):
        # Ensure the cash_balance is a number (float or int)
        if self.cash_balance:
            self.cash_balance = float(self.cash_balance)  # Convert to float to handle both integer and float values

        # Validate company_name: Ensure it's not empty
        if not self.company_name:
            frappe.throw("Company name is required.")
        
        if not self.cash_balance:
            self.cash_balance = 10000
        
        if self.cash_balance > 5000000:
            self.cash_balance = 10000  
            frappe.throw("Cash balance cannot exceed 5,000,000")
