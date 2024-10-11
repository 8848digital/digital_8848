import frappe

@frappe.whitelist(allow_guest=True)
def get_expertise_listing(**kwargs):
    try:
        # Get the 'type' from the request
        expertise_type = kwargs.get("type")
        
        if not expertise_type:
            return error_response("Please provide a type.")
        
        # Fetch expertise documents based on the 'type'
        expertise_doctypes_list = frappe.get_all("Expertise", filters={'type': expertise_type}, pluck="name")
        
        if not expertise_doctypes_list:
            return error_response("No data found.")
        
        response = []
        technology = []
        section_title = None  # Placeholder for section title

        # Iterate through each expertise document
        for doctype_name in expertise_doctypes_list:
            expertise_doctype = frappe.get_doc("Expertise", doctype_name)
            
            # Capture the section title from the first document
            if not section_title:
                section_title = expertise_doctype.get("section_title") or None

            # Gather expertise details
            expertise_doctype_details = {
                "title": expertise_doctype.get("title"),
                "logo": expertise_doctype.get("logo"),
                "short_description": expertise_doctype.get("short_description"),
                "slug": expertise_doctype.get("slug"),
                "url": expertise_doctype.get("url"),
                "background_image": expertise_doctype.get("background_image"),
                "sequence": expertise_doctype.get("sequence") or 0,
            }
            response.append(expertise_doctype_details)
            
            # If 'type' is "Technology", process expertise modules
            if expertise_type == "Technology" and expertise_doctype.expertise_module:
                for module in expertise_doctype.expertise_module:
                    technology.append({
                        "module_sequence": module.get("module_sequence"),
                        "module_name": module.get("module_name"),
                        "module_icon": module.get("module_icon"),
                    })
        
        # Sort response and technology lists by their respective sequence
        response = sorted(response, key=lambda x: x.get("sequence", 0))
        technology = sorted(technology, key=lambda x: x.get("module_sequence", 0))
        
        # Prepare final response with section title
        final_response = {
            "status": "success",
            "section_title": section_title,  # Use the first retrieved section title
            "data": response,
            "technology": technology if technology else None
        }
        
        return final_response
    
    except Exception as e:
        # Log the error and return an error response
        frappe.log_error(f"Error in get_expertise_listing: {str(e)}")
        return error_response(f"An error occurred: {str(e)}")


def error_response(err_msg):
    return {
        "status": "error",
        "error": err_msg
    }
