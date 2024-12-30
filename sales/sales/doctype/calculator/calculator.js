// Copyright (c) 2024, sowmi and contributors
// For license information, please see license.txt

frappe.ui.form.on("calculator", {	
    formula(frm) {
        frm.call("get_answer").then((res)=>{
            frm.set_value("answer", res.message)
        })
	},
});
