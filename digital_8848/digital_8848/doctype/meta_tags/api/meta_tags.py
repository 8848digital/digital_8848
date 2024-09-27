import frappe

@frappe.whitelist(allow_guest=True)
def get_meta_tags(**kwargs):
    try:
        response = []
        page_name = kwargs.get("page_name") or None
        if not page_name:
            return error_response("Please provide a page name")
        
        meta_tags_docname = frappe.db.get_value("Meta Tags", {"page_name":page_name})
        if not meta_tags_docname:
            return error_response("No meta tag found with the given page name")
        meta_tags_doctype = frappe.get_doc("Meta Tags", meta_tags_docname)
        
        response.append({
            "page_name": meta_tags_doctype.get("page_name") or None,
            "meta_title": meta_tags_doctype.get("meta_title") or None,
            "fav_icon_image": meta_tags_doctype.get("fav_icon_image") or None,
            "robots": meta_tags_doctype.get("robots") or None,
            "description": meta_tags_doctype.get("description") or None
        })
        return success_response(response)
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}")

def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    return response

def error_response(err_msg):
    return {"status": "error", "error": err_msg}