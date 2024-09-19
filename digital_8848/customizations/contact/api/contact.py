import frappe

@frappe.whitelist(allow_guest=True)
def create_contact(**kwargs):
    print("Processing contact creation")
    try:
        custom_full_names = kwargs.get("full_name")
        email_id = kwargs.get("email")
        phone_no = kwargs.get('phone_no')
        custom_company_name = kwargs.get("company_name")
        how_can_we_help = kwargs.get("how_can_we_help")
        i_want_to_receive_news_and_updates = kwargs.get("i_want_to_receive_news_and_updates")
        if i_want_to_receive_news_and_updates == "True":
            i_want_to_receive_news_and_updates = 1
        if i_want_to_receive_news_and_updates == "False":
            i_want_to_receive_news_and_updates = 0
        email_ids = email_id.split(',') if email_id else []
        phone_nos = phone_no.split(',') if phone_no else []

        existing_contact = frappe.get_all(
            "Contact Email", 
            filters={"email_id": ["in", email_ids]},
            fields=["parent"]  
        )
        
        if existing_contact:
            return error_response("User already exists.")

        contact_us = frappe.new_doc("Contact")
        contact_us.custom_full_names = custom_full_names
        contact_us.custom_company_name = custom_company_name
        contact_us.how_can_we_help = how_can_we_help
        contact_us.i_want_to_receive_news_and_updates = i_want_to_receive_news_and_updates


        for value in email_ids:  
            contact_us.append(
                "email_ids",  
                {
                    "email_id": value.strip(),  
                }
            )

        for phone in phone_nos:
            contact_us.append(
                "phone_nos",
                {
                    "phone": phone.strip(), 
                }
            )

        contact_us.insert(ignore_permissions=True)

        return success_response(
            {
                "message": "We have successfully received your request and will get back to you shortly.",
                "email": value.email_id, 
            }
        )

    except frappe.exceptions.DuplicateEntryError:
        return error_response("User already exists.")

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "create_contact_us")
        return error_response(str(e))


def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    if id:
        response["data"] = {"id": id, "name": id}
    return response

def error_response(err_msg):
    return {"status": "error", "error": err_msg}

