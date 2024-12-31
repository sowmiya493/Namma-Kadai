import frappe
from frappe.model.document import Document

class Sales(Document):
    def validate(self):
        total_amount = 0  # Initialize the total sales amount

        for item in self.sales_item:
            # Calculate item amount
            item.amount = item.quantity * item.rate
            total_amount += item.amount  # Add to total amount

            # Update the item's stock and sales rate
            self.update_item_details(item)

        # Set the total amount in the Sales document
        self.amount = total_amount

        # Add the total amount to the company's cash balance
        self.update_company_cash_balance(total_amount)

    def update_item_details(self, item):
        """Update the stock quantity and sales rate in the Item doctype."""
        item_doc = frappe.get_doc('Item', item.item)
        if item_doc:
            # Check stock availability
            if item_doc.quantity < item.quantity:
                frappe.throw(
                    frappe._(
                        "Insufficient stock for item '{0}'. Available quantity is {1}, but you requested {2}.".format(
                            item.item, item_doc.quantity, item.quantity
                        )
                    )
                )
            # Deduct the quantity from stock
            new_quantity = item_doc.quantity - item.quantity
            frappe.db.set_value('Item', item_doc.name, "quantity", new_quantity)

            # Update sales rate
            frappe.db.set_value('Item', item_doc.name, "sales_rate", item.rate)

    def update_company_cash_balance(self, total_amount):
        """Add the total amount to the company's cash balance."""
        company = frappe.get_doc("Company", self.company)  # Assuming `company` field is in the Sales document
        if company.cash_balance is None:
            company.cash_balance = 0

        # Increment the company's cash balance
        new_balance = company.cash_balance + total_amount
        frappe.db.set_value('Company', company.name, "cash_balance", new_balance)

@frappe.whitelist()
def get_item_rate(item_name):
    """Fetch the rate for the given item."""
    rate = frappe.db.get_value("Item", {"name": item_name}, "sales_rate")
    return rate or 0
