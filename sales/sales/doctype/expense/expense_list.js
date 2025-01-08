// Copyright (c) 2025, sowmi and contributors
// For license information, please see license.txt

frappe.listview_settings["Expense"] = {
    onload: function (listview) {
        listview.page.add_inner_button(("Report View"),
            function () {
                frappe.set_route("query-report", "expense management system");
            }
        );
        listview.page.add_inner_button(("Go to expense chart"),
            function () {
                frappe.set_route("form","Expense Chart");
            }
        );

    },
    hide_name_column: true,
};



