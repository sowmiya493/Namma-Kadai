# Copyright (c) 2025, sowmi and contributors
# For license information, please see license.txt

import frappe
def execute(filters=None):
    columns, data = get_columns(),get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "label": "Expense ID", 
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Expense",
        },
        {
            "label": "Date",
            "fieldname": "date",
            "fieldtype": "Date",
        },
        {
            "label": "Expense Type",
            "fieldname": "expense_type", 
            "fieldtype": "Data",
        },
        {
            "label": "Amount",
            "fieldname": "amount",
            "fieldtype": "Currency", 
        },
        {
            "label": "User",
            "fieldname": "user",
            "fieldtype": "Link",
            "options": "User",
        },
        {
            "label": "Created On",
            "fieldname": "creation",
            "fieldtype": "Datetime",
        },
    ]

def get_data(filters):
    query = """
        SELECT 
            name, date, expense_type, amount, user, creation
        FROM 
            `tabExpense`
        WHERE 
            docstatus < 2
        ORDER BY 
            creation DESC
    """
    return frappe.db.sql(query, as_dict=True)
