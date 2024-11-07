// Copyright (c) 2024, digital_8848 and contributors
// For license information, please see license.txt

frappe.ui.form.on("Expertise", {
    refresh(frm) {
        frm.set_query("case_study_title", function() {
            return {
                filters: {
                    publish_on_site: 1
                }
            };
        });
        if (frm.doc.url && frm.doc.publish_on_site == 1) {
            frm.add_custom_button(__("Show on Website"), function () {
                const url = frm.doc.url
                frappe.db.get_single_value("Website URL Settings", "base_url")
                    .then(base_url => {
                        window.open(base_url + "/" + url, '_blank');
                    })
                    .catch(error => {
                        console.error("Error fetching base URL:", error);
                    });
            })
            .css({
                color: "#10635a",
                "background-color": "#e3e3e3",
                "border-radius": "8px",
                "font-weight": "bold",
                padding: "5px 10px"
            });
        }
    },
    before_save(frm) {
        validate_sequence(frm, "expertise_detail", "Expertise Detail");
        validate_sequence(frm, "services_detail", "Services Detail");
        validate_sequence(frm, "process_details", "Process Detail");
        validate_sequence(frm, "why_choose_8848", "Why Choose 8848");
        generate_url(frm);
    },
    title: function(frm) {
        frm.doc.slug = frm.doc.title
            .toLowerCase()
            .replace(/&/g, 'and')
            .replace(/\s+/g, '-');
        frm.refresh_field("slug");
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

function generate_url(frm) {
    if (frm.doc.file_url && frm.doc.slug) {
        frm.doc.url = frm.doc.file_url + "/" + frm.doc.slug;
    }
}
