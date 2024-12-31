// frappe.ui.form.on('Company', {
//     validate: function(frm) {
//         // Check that company_name is set
//         if (!frm.doc.company_name) {
//             frappe.msgprint(__('Please enter a company name.'));
//             validated = false;  // Prevent form from saving if company_name is not provided
//         }

//         // Set cash_balance to 10000 by default if not set
//         if (!frm.doc.cash_balance) {
//             frm.set_value('cash_balance', 10000);
            
//         }

//         // Check if cash_balance exceeds 50,000 and reset it to 10000 if it does
//         if (frm.doc.cash_balance > 50000) {
//             frm.set_value('cash_balance', 10000);
//             frappe.msgprint(__('Autoreset the amount'));
//             validated = false;  // Prevent form from saving if limit is exceeded
//         }
//     }
// });
