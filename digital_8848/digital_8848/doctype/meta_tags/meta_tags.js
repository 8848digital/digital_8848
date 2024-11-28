// Copyright (c) 2024, digital_8848 and contributors
// For license information, please see license.txt

frappe.ui.form.on("Meta Tags", {
    onload(frm) {
        if (frm.is_new()) {
            frappe.db.get_value("File", { file_name: "8848_Favicon_32x32-White.png" }, "file_url")
                .then(response => {
                    if (response.message) {
                        const file_url = response.message.file_url;
                        if (file_url) {
                            frm.set_value("fav_icon_image", file_url);
                            frm.refresh_field("fav_icon_image");
                        }
                    } else {
                        
                    }
                });
        }
    }
});
