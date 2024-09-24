import frappe

@frappe.whitelist(allow_guest=True)
def get_logo_details(**kwargs):
    try:
        logo_details = frappe.get_all("Logo", fields = ["logo_name", "image", "sequence"], order_by='sequence asc')
        return success_response(logo_details)
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}")
    
def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    return response

def error_response(err_msg):
    return {"status": "error", "error": err_msg}