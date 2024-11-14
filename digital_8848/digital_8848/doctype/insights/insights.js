// Copyright (c) 2024, digital_8848 and contributors
// For license information, please see license.txt

frappe.ui.form.on("Insights", {
    title: function(frm) {
        frm.doc.slug = frm.doc.title
            .toLowerCase()
            .replace(/&/g, 'and')
            .replace(/\s+/g, '-');
        frm.refresh_field("slug");
    },
    refresh: function(frm) {
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
});
