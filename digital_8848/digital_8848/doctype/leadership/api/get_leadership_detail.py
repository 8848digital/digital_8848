import frappe

@frappe.whitelist(allow_guest=True)
def get_leadership_detail(**kwargs):
    try:
        leadership = frappe.qb.DocType('Leadership')

        leadership_details = frappe.qb.from_(
            leadership
        ).select(
            leadership.leader_name,
            leadership.designaton,
            leadership.short_description,
            leadership.leader_image,
            leadership.btn_text,
            leadership.btn_icon,
            leadership.btn_url
        ).run(as_dict=True)
        
        leadership_header_doc = frappe.get_doc("Leadership Heading")
        leadership_data = {
            "section_title" : leadership_header_doc.heading,
            "values" : leadership_details
        }

        return success_response(data=leadership_data)

    except frappe.DoesNotExistError:
        return error_response("Testimonial document not found.")
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}")
    
def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    return response

def error_response(err_msg):
    return {"status": "error", "error": err_msg}