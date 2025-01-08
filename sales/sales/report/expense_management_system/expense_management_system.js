frappe.query_reports["expense management system"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("Date"),
            "fieldtype": "Date",
            default:frappe.datetime.now_date(),
            "reqd": 0
            
        },
        {
            "fieldname": "expense_type",
            "label": __("Expense Type"),
            "fieldtype": "Select",
            "options": ["", "Travel", "Food", "Accommodation", "Petrol", "Others"],
            "reqd": 0
        },
        {
            
            "fieldname": "user",
            "label": __("User"),
            "fieldtype": "Link",
            "options": "User", 
            "default": frappe.session.user
        }
    ]
};
