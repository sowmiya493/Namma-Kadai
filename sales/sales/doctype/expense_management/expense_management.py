# Copyright (c) 2025, sowmi and contributors
# For license information, please see license.txt

import frappe,json
from frappe.model.document import Document


class ExpenseManagement(Document):
	pass
	# def validate(self):
	# 	self.expense_validate()







@frappe.whitelist()
def expense_validate(self):
	self = frappe._dict(json.loads(self))
	# import pdb;pdb.set_trace()
	expense = frappe.get_doc({
		"doctype": "Expense",
		"date": self.date,
		"expense_type": self.expense_type,
		"amount": self.amount,
		"user": self.user,
		"expenseapprover": self.expenseapprover,
	})
	expense.insert()

	return expense.name


