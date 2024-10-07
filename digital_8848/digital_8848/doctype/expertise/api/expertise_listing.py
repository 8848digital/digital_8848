import frappe

@frappe.whitelist(allow_guest=True)
def get_expertise_listing(**kwargs):
    try:
        if kwargs.get("type"):
            response = []
            expertise_doctypes_list = frappe.get_all("Expertise", filters={'type': kwargs.get("type")}, pluck="name")
            technology = []  
            
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
                        "sequence": expertise_doctype.get("sequence") or 0,
                    }

                    response.append(expertise_doctype_details)

                    if kwargs.get("type") == "Technology":
                        for module in expertise_doctype.expertise_module:  
                            technology.append({
                                "module_sequence": module.module_sequence or None,  
                                "module_name": module.module_name or None,          
                                "module_icon": module.module_icon or None,          
                            })

                response = sorted(response, key=lambda x: x.get("sequence") or 0)

                final_response = {
                    "message": {
                        "status": "success",
                        "data": response
                    }
                }
                if technology:
                    final_response["message"]["technology"] = technology

                return final_response
            else:
                return error_response("No data found.")
        else:
            return error_response("Please provide a type.")
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}")

def error_response(err_msg):
    return {
        "message": {
            "status": "error",
            "error": err_msg
        }
    }
