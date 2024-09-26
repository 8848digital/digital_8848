import frappe

@frappe.whitelist(allow_guest=True)
def get_insights_details(**kwargs):
    try:
        response = []
        title = kwargs.get("title")
        slug = kwargs.get("slug")

        if not title and not slug:
            return error_response("Please provide a title or slug")
        if title:
            insights_doctype = frappe.get_doc("Insights",kwargs.get("title"))
        if slug:
            insights_doctype_title = frappe.db.get_value("Insights",{'slug': kwargs.get("slug")})
            if not insights_doctype_title:
                return error_response("No insights found with the given slug")
            insights_doctype = frappe.get_doc("Insights",insights_doctype_title)

        response.append({
            "title": insights_doctype.get("title"),
            "url": insights_doctype.get("url"),
            "type": insights_doctype.get("type"),
            "slug": insights_doctype.get("slug"),
            "short_description": insights_doctype.get("short_description"),
            "image": insights_doctype.get("image")
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