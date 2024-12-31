import frappe
from frappe.model.document import Document

class Purchase(Document):
    def validate(self):

        total_amount = 0

        for item in self.purchase_item:
            
            # Calculate item amount
            item.amount = item.quantity * item.rate
            total_amount += item.amount  # Add to total amount

            # Update the item's stock and purchase rate
            self.update_item_details(item)

        # Set the total amount in the Purchase document
        self.amount = total_amount

        # Deduct the total amount from the company's cash balance
        self.update_company_cash_balance(total_amount)

    def update_item_details(self, item):
        """Update the stock quantity and purchase rate in the Item doctype."""
        item_doc = frappe.get_doc('Item', item.item)
        if item_doc:
            # Update stock quantity
            quantity = item_doc.quantity + item.quantity
            frappe.db.set_value('Item', item_doc.name, "quantity", quantity)
            # Update purchase rate only in draft state
            frappe.db.set_value('Item', item_doc.name, "purchase_rate", item.rate)
            # item_doc.purchase_rate = item.rate

            # item_doc.save()

    def update_company_cash_balance(self, total_amount):
        """Deduct the total amount from the company's cash balance."""
        company = frappe.get_doc("Company", self.company)  # Assuming `company` field is in the Purchase document
        if company.cash_balance is None or company.cash_balance < total_amount:
            frappe.throw(f"Insufficient cash balance in the company to make this purchase.")
        
        # Deduct the total amount
        new_balance =  company.cash_balance - total_amount
        
        frappe.db.set_value('Company', company.name, "cash_balance", new_balance)

        # Save the changes

@frappe.whitelist()
def get_item_rate(item_name):
    """Fetch the rate for the given item."""
    rate = frappe.db.get_value("Item", {"name": item_name}, "purchase_rate")
    return rate or 0
