// Copyright (c) 2024, suga and contributors
// For license information, please see license.txt

frappe.ui.form.on('Customer', {
    // Triggered when the form is refreshed
    refresh(frm) {
        // You can add custom actions when the form is refreshed here.
        // For example, adding a button to the form:
        frm.add_custom_button(__('Custom Action'), function() {
            frappe.msgprint(__('This is a custom action.'));
        });
    },

    // Triggered when a field value changes
    customer_name: function(frm) {
        // Custom code when customer_name is changed
        console.log('Customer Name: ' + frm.doc.customer_name);
    }
});
