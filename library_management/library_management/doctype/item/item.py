import frappe
from frappe.model.document import Document
from frappe import _

class Item(Document):
    def validate(self):
        """Validate the Item document."""
        # Set default values to zero if they are not provided
        self.quantity = self.quantity or 0
        self.purchase_rate = self.purchase_rate or 0
        self.sales_rate = self.sales_rate or 0

        # Validate values
        if self.quantity < 0:
            frappe.throw(_("Quantity cannot be negative."))
        
        if self.purchase_rate < 0:
            frappe.throw(_("Purchase Rate cannot be negative."))
        
        if self.sales_rate < 0:
            frappe.throw(_("Sales Rate cannot be negative."))

        # Calculate the amount only if both quantity and purchase_rate are non-zero
        self.amount = self.quantity * self.purchase_rate

    def update_stock(self, quantity_change):
        """Update the stock quantity for the item."""
        self.quantity += quantity_change

        if self.quantity < 0:
            frappe.throw(_("Insufficient stock for item: {0}").format(self.name))

        # Save the updated document
        self.save(ignore_permissions=True)
        frappe.msgprint(_("Stock for {0} updated to {1}").format(self.name, self.quantity))

    def on_submit(self):
        """Example: Update purchase and sales amounts after submit."""
        # Recalculate total purchase and sales amounts (if required)
        self.total_purchase_amount = self.quantity * self.purchase_rate
        self.total_sales_amount = self.quantity * self.sales_rate
        frappe.msgprint(_("Purchase and sales amounts updated for item: {0}").format(self.name))
