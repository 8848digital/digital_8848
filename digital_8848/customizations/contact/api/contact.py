import frappe

@frappe.whitelist(allow_guest=True)
def create_contact(**kwargs):
    try:
        custom_full_names = kwargs.get("full_name")
        email_id = kwargs.get("email")
        phone_no = kwargs.get('phone_no')
        custom_company_name = kwargs.get("company_name")
        how_can_we_help = kwargs.get("how_can_we_help")
        i_want_to_receive_news_and_updates = kwargs.get("i_want_to_receive_news_and_updates")

        i_want_to_receive_news_and_updates, email_ids, phone_nos = get_news_updates_email_id_phone_no(i_want_to_receive_news_and_updates, email_id, phone_no)
        existing_contact = get_existing_contacts(email_ids)
        if existing_contact:
            return error_response("User already exists.")

        contact_us = create_contact_us_detail(custom_full_names,custom_company_name,how_can_we_help,
                                            i_want_to_receive_news_and_updates,email_ids,phone_nos)
        if contact_us.email_ids:
            for email in contact_us.email_ids:
                email_id_from_child = email.email_id
                break

        return success_response(
            {
                "message": "We have successfully received your request and will get back to you shortly.",
                "email": email_id_from_child
            }
        )
    except frappe.exceptions.DuplicateEntryError:
        return error_response("User already exists.")
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "create_contact_us")
        return error_response(str(e))

def get_existing_contacts(email_ids):
    existing_contacts = frappe.get_all(
            "Contact Email", 
            filters={"email_id": ["in", email_ids]},
            fields=["parent"]  
        )
    return existing_contacts

def create_contact_us_detail(custom_full_names,custom_company_name,how_can_we_help,i_want_to_receive_news_and_updates,email_ids,phone_nos):
    contact_us = frappe.new_doc("Contact")
    contact_us.custom_full_names = custom_full_names
    contact_us.custom_company_name = custom_company_name
    contact_us.how_can_we_help = how_can_we_help
    contact_us.i_want_to_receive_news_and_updates = i_want_to_receive_news_and_updates

    for value in email_ids:  
        contact_us.append("email_ids",  
            {
                "email_id": value.strip(),  
            }
        )

    for phone in phone_nos:
        contact_us.append("phone_nos",
            {
                "phone": phone.strip(), 
            }
        )

    contact_us.insert(ignore_permissions=True)
    return contact_us

def get_news_updates_email_id_phone_no(i_want_to_receive_news_and_updates, email_id, phone_no):
    if i_want_to_receive_news_and_updates == "True":
        i_want_to_receive_news_and_updates = 1
    if i_want_to_receive_news_and_updates == "False":
        i_want_to_receive_news_and_updates = 0

    email_ids = email_id.split(',') if email_id else []
    phone_nos = phone_no.split(',') if phone_no else []

    return i_want_to_receive_news_and_updates, email_ids, phone_nos

def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    if id:
        response["data"] = {"id": id, "name": id}
    return response

def error_response(err_msg):
    return {"status": "error", "error": err_msg}

