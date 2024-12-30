frappe.ui.form.on('custom button example', {
    refresh: function(frm) {
        // Always make 'title' mandatory
        frm.set_df_property('title', 'reqd', 1);

        // If 'status' is 'Open', allow editing of 'description' and set its fieldtype to 'Text'
        if (frm.doc.status === 'Open') {
            frm.set_df_property('description', 'read_only', 0); // Make editable
            frm.set_df_property('description', 'fieldtype', 'Text');
        } 
        // If 'status' is 'Closed', make 'description' read-only and change its fieldtype to 'Small Text'
        else if (frm.doc.status === 'Closed') {
            frm.set_df_property('description', 'read_only', 1); // Make read-only
            frm.set_df_property('description', 'fieldtype', 'Small Text');
        }

        // Set 'status' dropdown options dynamically
        frm.set_df_property('status', 'options', ['Open', 'In Progress', 'Closed']);
    },

    // Trigger changes dynamically when the 'status' field changes
    status: function(frm) {
        if (frm.doc.status === 'Open') {
            frm.set_df_property('description', 'read_only', 0); // Make editable
            frm.set_df_property('description', 'fieldtype', 'Text');
            frappe.msgprint('You can now edit the description as the status is Open.');
        } else if (frm.doc.status === 'Closed') {
            frm.set_df_property('description', 'read_only', 1); // Make read-only
            frm.set_df_property('description', 'fieldtype', 'Small Text');
            frappe.msgprint('The description is now read-only as the status is Closed.');
        }
    }
});
