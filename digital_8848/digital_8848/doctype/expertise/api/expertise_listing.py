import frappe

@frappe.whitelist(allow_guest=True)
def get_expertise_listing(**kwargs):
    try:
        if kwargs.get("type"):
            response = []
            expertise_doctypes_list = frappe.get_all("Expertise", filters={'type': kwargs.get("type")}, pluck="name")
            if expertise_doctypes_list:
                for doctype in expertise_doctypes_list:
                    expertise_doctype = frappe.get_doc("Expertise", doctype)
                    expertise_doctype_details = {
                        "title": expertise_doctype.get("title") or None,
                        "logo": expertise_doctype.get("logo") or None,
                        "short_description": expertise_doctype.get("short_description") or None,
                        "slug": expertise_doctype.get("slug") or None,
                        "url": expertise_doctype.get("url") or None,
                        "background_image": expertise_doctype.get("background_image") or None,
                        "sequence": expertise_doctype.get("sequence") or 0
                    }
                    response.append(expertise_doctype_details)
                
                response = sorted(response, key=lambda x: x.get("sequence") or 0)
                return success_response(response)
            else:
                return error_response("No data found.")
        else:
            return error_response("Please provide a type.")
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}")
    
def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    return response

def error_response(err_msg):
    return {"status": "error", "error": err_msg}