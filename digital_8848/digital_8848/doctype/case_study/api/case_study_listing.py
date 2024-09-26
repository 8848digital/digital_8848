import frappe

@frappe.whitelist(allow_guest=True)
def get_case_study_listing(**kwargs):
    try:
        response = []
        filters = {}
        if kwargs.get("type"):
            filters.update({"type": kwargs.get("type")})

        case_study_doctypes_list = frappe.get_all("Case Study", filters=filters, pluck="name")
        if case_study_doctypes_list:
            for doctype in case_study_doctypes_list:
                case_study_doctype = frappe.get_doc("Case Study", doctype)
                case_study_doctype_details = {
                    "title": case_study_doctype.get("title") or None,
                    "image": case_study_doctype.get("image") or None,
                    "short_description": case_study_doctype.get("short_description") or None,
                    "slug": case_study_doctype.get("slug") or None,
                    "url": case_study_doctype.get("url") or None,
                    "type": case_study_doctype.get("type") or None
                }
                response.append(case_study_doctype_details)
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