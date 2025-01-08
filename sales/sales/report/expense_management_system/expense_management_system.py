import frappe

def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
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

def get_data(filters=None):
    conditions = []
    if filters.get("from_date"):
        conditions.append("date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append("date <= %(to_date)s")
    if filters.get("expense_type"):
        conditions.append("expense_type = %(expense_type)s")
    if filters.get("user"):
        conditions.append("user = %(user)s")

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f"""
        SELECT
            name, date, expense_type, amount, user, creation
        FROM
            `tabExpense`
        WHERE
            {where_clause} AND docstatus < 2
        ORDER BY
            creation DESC
    """
    return frappe.db.sql(query, filters, as_dict=True)
