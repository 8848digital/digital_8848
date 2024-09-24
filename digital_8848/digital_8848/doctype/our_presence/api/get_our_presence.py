import frappe

@frappe.whitelist(allow_guest=True)
def get_our_presence(**kwargs):
    try:
        our_presence = frappe.qb.DocType('Our Presence')

        our_presence_details = frappe.qb.from_(
            our_presence
        ).select(
            our_presence.city,
            our_presence.description.as_("content_text"),
            our_presence.contact_no,
            our_presence.email_id,
            our_presence.redirect_icon,
            our_presence.redirect_url
        ).run(as_dict=True)

        our_presence_header_doc = frappe.get_doc("Our Presence Heading")
        our_presence_data = {
            "section_title" : our_presence_header_doc.heading,
            "values" : our_presence_details
        }

        return success_response(data=our_presence_data)

    except frappe.DoesNotExistError:
        return error_response("Our Presence document not found.")
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}")
    
def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    return response

def error_response(err_msg):
    return {"status": "error", "error": err_msg}