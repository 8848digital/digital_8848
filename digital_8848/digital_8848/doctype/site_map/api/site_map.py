import frappe

@frappe.whitelist(allow_guest=True)
def get_site_map(**kwargs):
    site_map = frappe.db.sql("""
        SELECT url,last_modified,change_frequency,priority
        FROM `tabSite Map`
    """, as_dict=True)
    response = {
        "status": "success",
        "data": site_map
    }
    return response
