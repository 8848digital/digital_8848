import frappe

@frappe.whitelist(allow_guest=True)
def get_subscriber(**kwargs):
    frappe.set_user("Administrator")
    try:
        sub = frappe.get_doc({
            "doctype": "Subscriber",
            "email": kwargs.get("email"),
            "mobile_number": kwargs.get("mobile_number")
        })
        sub.insert()
        frappe.set_user(frappe.session.user)
        return {
            "status": "success",
            "data": "Subscription to newsletter added successfully"
        }
    
    except Exception as e:
        frappe.set_user(frappe.session.user)
        return {
            "status": "error",
            "data": "Subscription already exists"
        }
