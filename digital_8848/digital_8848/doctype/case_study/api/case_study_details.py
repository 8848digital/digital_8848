import frappe

@frappe.whitelist(allow_guest=True)
def get_case_study_details(**kwargs):
    try:
        response = []
        title = kwargs.get("title")
        slug = kwargs.get("slug")

        if not title and not slug:
            return error_response("Please provide a title or slug")
        if title:
            case_study_doctype = frappe.get_doc("Case Study",kwargs.get("title"))
        if slug:
            case_study_doctype_title = frappe.db.get_value("Case Study",{'slug': kwargs.get("slug")})
            if not case_study_doctype_title:
                return error_response("No case study found with the given slug")
            case_study_doctype = frappe.get_doc("Case Study",case_study_doctype_title)

        response.append({
            "title": case_study_doctype.get("title"),
            "url": case_study_doctype.get("url"),
            "type": case_study_doctype.get("type"),
            "slug": case_study_doctype.get("slug"),
            "short_description": case_study_doctype.get("short_description"),
            "image": case_study_doctype.get("image")
        })
        return success_response(data=response)
          
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}")
    
def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    return response

def error_response(err_msg):
    return {"status": "error", "error": err_msg}