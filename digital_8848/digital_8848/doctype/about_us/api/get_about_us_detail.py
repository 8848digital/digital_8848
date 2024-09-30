import frappe

@frappe.whitelist(allow_guest=True)
def get_about_us_detail(**kwargs):
    try:
        about_us_doc = frappe.get_doc("About Us")

        about_us_data = {
           "heading" : about_us_doc.heading,
           "banner_image" : about_us_doc.banner
        }
        about_section = get_about_section_details(about_us_doc)
        home_page = get_home_page_details(about_us_doc)
        our_mission = get_our_mission_details(about_us_doc)
        founder_details = get_founder_details(about_us_doc)
        client_details = get_client_details(about_us_doc)
        global_delivery = get_global_delivery_details(about_us_doc)
        our_values = get_our_value_details(about_us_doc)
        industry = get_industry_details(about_us_doc)

        about_us_data["about_section"] = about_section
        about_us_data["home_page"] = home_page
        about_us_data["our_mission"] = our_mission
        about_us_data["founder_details"] = founder_details
        about_us_data["client_details"] = client_details
        about_us_data["global_delivery"] = global_delivery
        about_us_data["our_values"] = our_values
        about_us_data["industry_info"] = industry

        return success_response(data=about_us_data)
    
    except frappe.DoesNotExistError:
        return error_response("About Us document not found.")
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}")
    
def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    return response

def error_response(err_msg):
    return {"status": "error", "error": err_msg}

def get_about_section_details(about_us_doc):
    about_section = {
            "section_title" : about_us_doc.about_section_title,
            "description" : about_us_doc.about_description,
            "btn_text" : about_us_doc.about_btn_text,
            "btn_url" : about_us_doc.about_btn_url
        }
    about_section_certified_partners = []
    for partners in about_us_doc.certified_partners:
        partner_details = {}
        partner_details["certified_partner_logo"] = partners.certified_partner_logo
        partner_details["img_alt"] = partners.img_alt
        partner_details["height"] = partners.height
        partner_details["width"] = partners.width
        about_section_certified_partners.append(partner_details)

    about_section["certified_partners"] = about_section_certified_partners
    return about_section

def get_home_page_details(about_us_doc):
    home_page = {
            "description" : about_us_doc.home_page_description,
            "btn_text" : about_us_doc.home_page_btn_text,
            "btn_url" : about_us_doc.home_page_btn_url
        }
    home_page_certified_partners = []
    for partners in about_us_doc.certified_partners_table:
        partner_details = {}
        partner_details["certified_partner_logo"] = partners.certified_partner_logo
        partner_details["img_alt"] = partners.img_alt
        partner_details["height"] = partners.height
        partner_details["width"] = partners.width
        home_page_certified_partners.append(partner_details)

    home_page["certified_partners"] = home_page_certified_partners
    return home_page

def get_our_mission_details(about_us_doc):
    our_mission = {
            "section_title" : about_us_doc.our_mission_section_title,
            "description" : about_us_doc.our_mission_description
        }
    
    return our_mission

def get_founder_details(about_us_doc):
    founder_details = {
            "founder_name" : about_us_doc.founder_name,
            "founder_image" : about_us_doc.founder_image,
            "founder_designation" : about_us_doc.founder_designation,
            "description" : about_us_doc.founder_description,
            "quote" : about_us_doc.founder_quote,
            "quote_icon" : about_us_doc.founder_quote_icon
        }
    
    return founder_details

def get_client_details(about_us_doc):
    client_data = []
    for client in about_us_doc.client_details:
        client_doc = frappe.get_doc("Clients", client.client)
        client_logo_and_name = {
            "company_name" : client_doc.company_name,
            "company_logo" : client_doc.company_logo
        }
        client_data.append(client_logo_and_name)

    return client_data

def get_global_delivery_details(about_us_doc):
    global_delivery = {
            "section_title" : about_us_doc.global_delivery_section_title,
            "description" : about_us_doc.global_delivery_description
        }
    global_delivery_counts = []
    for delivery in about_us_doc.global_delivery_counts:
        delivery_detail = {}
        delivery_detail["delivery_counts"] = delivery.delivery_counts
        delivery_detail["description"] = delivery.description
        global_delivery_counts.append(delivery_detail)

    global_delivery["global_delivery_details"] = global_delivery_counts
    return global_delivery

def get_our_value_details(about_us_doc):
    our_values = {
            "section_title" : about_us_doc.our_values_section_title,
            "background_image" : about_us_doc.background_image
        }
    our_value_details = []
    for value in about_us_doc.our_values_details:
        values = {}
        values["title"] = value.title
        values["image"] = value.image
        values["short_description"] = value.short_description
        values["icon"] = value.icon
        values["url"] = value.url
        our_value_details.append(values)

    our_values["our_value_details"] = our_value_details
    return our_values

def get_industry_details(about_us_doc):
    industry_details = {}
    industry_details.update({
        "industry_title": about_us_doc.get("industry_title") or None,
        "industry_short_description": about_us_doc.get("industry_short_description") or None
    })
    return industry_details