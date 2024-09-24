import frappe

@frappe.whitelist(allow_guest=True)
def get_started_today(**kwargs):
    try:
        get_started_today_doc = frappe.get_doc("Get Started Today")
        get_started_data = {
            "heading" : get_started_today_doc.title,
            "text" : get_started_today_doc.short_description,
            "background_image" : get_started_today_doc.background_image,
            "btn_text" : get_started_today_doc.btn_text,
            "btn_url" : get_started_today_doc.btn_url
        }
        return success_response(data=get_started_data)
    
    except frappe.DoesNotExistError:
        return error_response("Get Started document not found.")
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}")
    
def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    return response

def error_response(err_msg):
    return {"status": "error", "error": err_msg}