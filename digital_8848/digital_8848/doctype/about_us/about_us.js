// Copyright (c) 2024, digital_8848 and contributors
// For license information, please see license.txt

frappe.ui.form.on("About Us", {
    before_save(frm) {
        validate_sequence(frm, "why_choose_us_detail_tab", "Why Choose Us Table");
    }
});

function validate_sequence(frm, table_field, label) {
    if (frm.doc[table_field] && frm.doc[table_field].length > 0) {
        let sequences = frm.doc[table_field].map(item => item.sequence);
        sequences.sort((a, b) => a - b);

        let is_sequence_valid = true;
        let expected_sequence = 1;

        for (let i = 0; i < sequences.length; i++) {
            if (sequences[i] !== expected_sequence) {
                frappe.msgprint(__(`${label} : Sequence should start from 1 and increase sequentially. <br>Found ${sequences[i]} instead of ${expected_sequence}.`));
                is_sequence_valid = false;
                break;
            }
            expected_sequence++;
        }

        if (!is_sequence_valid) {
            frappe.validated = false; 
        }
        frm.refresh_field(table_field);
    }
}
