frappe.ui.form.on('Purchase', {
    onload: function(frm) {
        // Set query to filter items based on the selected company
        frm.set_query('item', 'purchase_item', function(doc, cdt, cdn) {
            return {
                filters: {
                    company_name: doc.company  // Assuming the Item doctype has a 'company_name' field
                }
            };
        });
    },

    // Recalculate the total amount when the form is loaded or refreshed
    purchase_item: function(frm) {
        calculate_total_amount(frm);
    }
});

frappe.ui.form.on('Purchase Item', {
    item: function(frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        
        if (row.item) {
            // Fetch the purchase rate from the Item doctype
            frappe.db.get_value('Item', row.item, 'purchase_rate')
                .then(r => {
                    if (r && r.message) {
                        const rate = r.message.purchase_rate || 0;

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

// Function to calculate the total amount in the parent form and update cash balance
function calculate_total_amount(frm) {
    let total_amount = 0;

    frm.doc.purchase_item.forEach(item => {
        total_amount += item.amount || 0; // Sum all amounts in the child table
    });

    frm.set_value('amount', total_amount); // Update the total amount field in the parent doc

    // Update cash balance by subtracting the total amount
    const new_cash_balance = (frm.doc.cash_balance || 0) - total_amount;
    
}
