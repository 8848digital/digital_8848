// Copyright (c) 2024, digital_8848 and contributors
// For license information, please see license.txt

frappe.ui.form.on("Case Study", {
    title: function(frm) {
        frm.doc.slug = frm.doc.title
            .toLowerCase()
            .replace(/&/g, 'and')
            .replace(/\s+/g, '-');
        frm.refresh_field("slug");
    },
    before_save(frm) {
        generate_url(frm);
    },

});

function generate_url(frm) {
    if (frm.doc.url && frm.doc.slug && !frm.doc.url.includes(frm.doc.slug)) {
        frm.doc.url = frm.doc.url + "/" + frm.doc.slug;
    }
}
