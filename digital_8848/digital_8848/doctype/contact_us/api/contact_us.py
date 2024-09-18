import frappe

@frappe.whitelist(allow_guest=True)
def get_contact_us(**kwargs):
    try:
        # Retrieve the first "Contact US" document
        contact_us = frappe.get_doc("Contact US")
        
        # Return the heading and description fields
        return success_response(data={"heading": contact_us.heading, "description": contact_us.description})
    
    except frappe.DoesNotExistError:
        # Handle the case where "Contact US" document does not exist
        return error_response("Contact US document not found.")
    
    except Exception as e:
        # Handle any other unexpected errors
        return error_response(f"An error occurred: {str(e)}")


def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    if id:
        response["data"] = {"id": id, "name": id}
    return response


def error_response(err_msg):
    return {"status": "error", "error": err_msg}
