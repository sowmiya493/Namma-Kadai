// Copyright (c) 2025, sowmi and contributors
// For license information, please see license.txt

frappe.ui.form.on("Expense Management", {
    refresh(frm) {
        frm.add_custom_button('Add Expense', () => {
            const ans = new frappe.ui.Dialog({
                title: 'Add Expense',
                fields: [
                    {
                        fieldname: 'date',
                        label: 'Date',
                        fieldtype: 'Date',
                        reqd: 1
                    },
                    {
                        fieldname: 'expense_type',
                        label: 'Expense Type',
                        fieldtype: 'Select',
                        options: ['Travel', 'Food', 'Accommodation','Petrol','Others'],
                        reqd: 1
                    },
                    {
                        fieldname: 'amount',
                        label: 'Amount',
                        fieldtype: 'Currency',
                        reqd: 1
                    },
                    {
                        fieldname: 'user',
                        label: 'User',
                        fieldtype: 'Data',
                        default: frappe.session.user,
                        read_only: 1
                    },
                    {
                        fieldname: 'expenseapprover',
                        label: 'Expense Approver',
                        fieldtype: 'Data',
                        default: 'Administrator',
                        read_only:1
                    }
                ],
                primary_action_label: 'Switch to expense approver',
                primary_action(data) {
                    if (data.date && data.expense_type && data.amount) {
                        frappe.call({
                            method: "frappe.client.insert", 
                            args: {
                                doc: {
                                    doctype: "Expense",
                                    date: data.date,
                                    expense_type: data.expense_type,
                                    amount: data.amount,
                                    user: data.user
                                }
                            },
                            callback: function (response) {
                                if (response.message) {
                                    frappe.msgprint(`Expense record created successfully:
                                        <br> Date: ${data.date}
                                        <br> Type: ${data.expense_type}
                                        <br> Amount: ${data.amount}
                                        <br> User: ${data.user}`);
                                    frappe.set_route('Form', 'Expense', response.message.name);
                                    
                                }
                            },
                        });
                    } 
                }
            });

            ans.show();
        });
    }
});
