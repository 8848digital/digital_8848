import frappe

@frappe.whitelist(allow_guest=True)
def get_insights_listing(**kwargs):
    try:
        response = []
        filters = {"publish_on_site" : 1,}

        insights_doctypes_list = frappe.get_all("Insights", filters=filters, pluck="name", order_by="published_on desc")
        if insights_doctypes_list:
            for doctype in insights_doctypes_list:
                insights_doctype = frappe.get_doc("Insights", doctype)
                insights_doctype_details = {
                    "title": insights_doctype.get("title") or None,
                    "author": insights_doctype.get("author") or None,
                    "published_on": insights_doctype.get("published_on") or None
                }
                response.append(insights_doctype_details)
            return success_response(response)
        else:
            return error_response("No data found.")
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}")

def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    return response

def error_response(err_msg):
    return {"status": "error", "error": err_msg}