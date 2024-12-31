frappe.ui.form.on('Sales', {
    onload: function(frm) {
        // Set query to filter items based on the selected company
        frm.set_query('item', 'sales_item', function(doc, cdt, cdn) {
            return {
                filters: {
                    company_name: doc.company  // Assuming the Item doctype has a 'company_name' field
                }
            };
        });
    },

    refresh: function(frm) {
        calculate_total_amount(frm); // Recalculate total amount on form refresh
    }
});

frappe.ui.form.on('Sales Item', {
    item: function(frm, cdt, cdn) {
        const row = locals[cdt][cdn];

        if (row.item) {
            // Fetch the sales rate from the Item doctype
            frappe.db.get_value('Item', row.item, 'sales_rate')
                .then(r => {
                    if (r && r.message) {
                        const rate = r.message.sales_rate || 0;

                        if (rate > 0) {
                            // Automatically set the rate if it's available
                            frappe.model.set_value(cdt, cdn, 'rate', rate).then(() => {
                                calculate_item_amount(frm, cdt, cdn);
                            });
                        }
                    }
                });
        }
    },
    quantity: function(frm, cdt, cdn) {
        calculate_item_amount(frm, cdt, cdn);
    },
    rate: function(frm, cdt, cdn) {
        calculate_item_amount(frm, cdt, cdn);
    }
});

// Function to calculate amount for a single row in the child table
function calculate_item_amount(frm, cdt, cdn) {
    const row = locals[cdt][cdn];

    if (row.quantity && row.rate) {
        const amount = row.quantity * row.rate; // Calculate amount
        frappe.model.set_value(cdt, cdn, 'amount', amount).then(() => {
            calculate_total_amount(frm); // Recalculate the total amount in the parent form
        });
    }
}

// Function to calculate the total amount in the parent form
function calculate_total_amount(frm) {
    let total_amount = 0;
    frm.doc.sales_item.forEach(item => {
        total_amount += item.amount || 0;
    });
    frm.set_value('amount', total_amount); // Update total amount in the parent doc
}
