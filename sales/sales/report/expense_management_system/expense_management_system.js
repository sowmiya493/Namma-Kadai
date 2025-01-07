// Copyright (c) 2025, sowmi and contributors
// For license information, please see license.txt

frappe.query_reports["expense management system"] = {
    "filters": [
        {
            "fieldname": "date",
            "label": __("Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
        },
        {
            "fieldname": "expense_type",
            "label": __("Expense Type"),
            "fieldtype": "Select",
            "options": ["Travel", "Food", "Accommodation", "Petrol", "Others"],
        },
        {
            "fieldname": "user",
            "label": __("User"),
            "fieldtype": "Link",
            "options": "User",
        },
    ]
};
