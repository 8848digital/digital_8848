import frappe

@frappe.whitelist(allow_guest=True)
def get_google_analytics(**kwargs):
    try:
        # Fetch the single Doctype record
        ga = frappe.get_doc("Google Analytics")
        return success_response(data={"google_analytics_id": ga.google_analytics_id})
    except Exception as e:
        return error_response(err_msg=str(e))


def success_response(data=None):
    """
    Format a success response.
    """
    response = {"status": "success"}
    if data:
        response["data"] = data
    return response


def error_response(err_msg):
    """
    Format an error response.
    """
    return {
        "status": "error",
        "error": err_msg
    }
