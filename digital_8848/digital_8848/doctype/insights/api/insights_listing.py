import frappe

@frappe.whitelist(allow_guest=True)
def get_insights_listing(**kwargs):
    try:
        response = []
        filters = {"publish_on_site" : 1,}
        if kwargs.get("type"):
            filters.update({"type": kwargs.get("type")})

        insights_doctypes_list = frappe.get_all("Insights", filters=filters, pluck="name", order_by="sequence asc")
        if insights_doctypes_list:
            for doctype in insights_doctypes_list:
                insights_doctype = frappe.get_doc("Insights", doctype)
                insights_doctype_details = {
                    "title": insights_doctype.get("title") or None,
                    "sequence": insights_doctype.get("sequence") or None,
                    "image": insights_doctype.get("image") or None,
                    "short_description": insights_doctype.get("short_description") or None,
                    "slug": insights_doctype.get("slug") or None,
                    "url": insights_doctype.get("url") or None,
                    "type": insights_doctype.get("type") or None
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