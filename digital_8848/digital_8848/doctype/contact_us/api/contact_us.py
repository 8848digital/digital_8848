import frappe

@frappe.whitelist(allow_guest=True)
def get_contact_us(**kwargs):
    try:
        contact_us = frappe.get_doc("Contact US")
        return success_response(data={"heading": contact_us.heading, "description": contact_us.description})
    
    except frappe.DoesNotExistError:
        return error_response("Contact US document not found.")
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}")
def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    if id:
        response["data"] = {"id": id, "name": id}
    return response
def error_response(err_msg):
    return {"status": "error", "error": err_msg}
