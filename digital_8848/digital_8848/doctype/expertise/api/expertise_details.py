import frappe

@frappe.whitelist(allow_guest=True)
def get_expertise_details(**kwargs):
    try:
        response = []
        title = kwargs.get("title")
        slug = kwargs.get("slug")
        if not title and not slug:
            return error_response("Please provide a title or slug", response)
        if slug:
            expertise_doctype_title = frappe.db.get_value("Expertise",{'slug': kwargs.get("slug")})
            if not expertise_doctype_title:
                return error_response("No expertise found with the given slug",response)
            expertise_doctype = frappe.get_doc("Expertise",expertise_doctype_title)
        if title:
            expertise_doctype = frappe.get_doc("Expertise",kwargs.get("title"))

        details = get_details(expertise_doctype)
        expertise_details = get_expertise_details_data(expertise_doctype)
        banner_details = get_banner_details(expertise_doctype)
        services_details = get_services_details(expertise_doctype)
        process_details = get_process_details(expertise_doctype)
        type = expertise_doctype.get("type")
        filtered_tab_details = filter_tab_details_based_on_type(type,expertise_doctype)
        case_study_details = get_case_study_details(expertise_doctype)
        faq_details = get_faq_details(expertise_doctype)

        response = [{**details,**expertise_details,**banner_details,**services_details,**process_details,**filtered_tab_details,
                    **case_study_details,**faq_details}]        
        return success_response(data=response)
          
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}",response)
    

def get_details(expertise_doctype):
    details = {}
    get_details_default_field_values = {
        "title": None,
        "logo": None,
        "url": None,
        "type": None,
        "slug": None,
        "short_description": None,
        "truncate_text": None,
        "sequence": None,
    }
    for field, default_value in get_details_default_field_values.items():
        details[field] = expertise_doctype.get(field, default_value)
    return details

def get_expertise_details_data(expertise_doctype):
    expertise_details = {}
    subtitle = expertise_doctype.get("subtitle") if expertise_doctype.get("subtitle") else None
    expertise_details.update({"subtitle": subtitle})

    if expertise_doctype.get("expertise_detail"):
        expertise_detail_child = [
                {
                    "title":expertise.get("title") or None,
                    "short_description":expertise.get("short_description") or None,
                    "truncate_text":expertise_doctype.get("truncate_text_1"),
                    "url":expertise.get("url") or None,
                    "sequence":expertise.get("sequence") or None
                } 
                for expertise in sorted(expertise_doctype.get("expertise_detail"), key=lambda x: x.get("sequence"))
            ]
        expertise_details.update({"expertise_detail":expertise_detail_child})
    else:
        expertise_details.update({"expertise_detail":[]})
    return expertise_details

def get_banner_details(expertise_doctype):
    banner_details = {}
    banner_details_default_field_values = {
        "banner_title": None,
        "banner_image": None,
        "banner_description": None
    }
    for field, default_value in banner_details_default_field_values.items():
        banner_details[field] = expertise_doctype.get(field, default_value)
    return banner_details

def get_services_details(expertise_doctype):
    services_details = {}
    if expertise_doctype.get("service_title"):
        services_details.update({"service_title":expertise_doctype.get("service_title")})
    else:
        services_details.update({"service_title": None})

    if expertise_doctype.get("services_detail"):
        services_detail_child = [
                {
                    "title":service.get("title") or None,
                    "short_description":service.get("short_description") or None,
                    "truncate_text":expertise_doctype.get("truncate_text_2"),
                    "logo":service.get("logo") or None,
                    "sequence":service.get("sequence") or None,
                    "url":service.get("url") or None
                } 
                for service in sorted(expertise_doctype.get("services_detail"), key=lambda x: x.get("sequence"))
            ]
        services_details.update({"services_detail":services_detail_child})
    else:
        services_details.update({"services_detail":[]})
    return services_details

def get_process_details(expertise_doctype):
    process_details = {}
    if expertise_doctype.get("process_title"):
        process_details.update({"process_title":expertise_doctype.get("process_title")})
    else:
        process_details.update({"process_title":None})
    if expertise_doctype.get("process_details"):
        process_details_child = [
                {
                    "title":process.get("title") or None,
                    "short_description":process.get("short_description") or None,
                    "truncate_text":expertise_doctype.get("truncate_text_3"),
                    "sequence":process.get("sequence") or None,
                    "url":process.get("url") or None
                } 
                for process in sorted(expertise_doctype.get("process_details"), key=lambda x: x.get("sequence"))
            ]
        process_details.update({"process_details":process_details_child})
    else:
        process_details.update({"process_details":[]})
    return process_details

def filter_tab_details_based_on_type(type,expertise_doctype):
    filtered_data = {}
    if type in ["Services","Technology"]:
        filtered_data = get_why_choose_8848_details(expertise_doctype)
    else:
        filtered_data = get_advantages_details(expertise_doctype)
    return filtered_data
    
def get_why_choose_8848_details(expertise_doctype):
    why_choose_8848_details = {}
    if expertise_doctype.get("why_choose_8848_title"):
        why_choose_8848_details.update({"why_choose_8848_title": expertise_doctype.get("why_choose_8848_title")})
    else:
        why_choose_8848_details.update({"why_choose_8848_title": None})
    if expertise_doctype.get("why_choose_8848"):
        why_choose_8848_child = [
                {
                    "title":entry.get("title") or None,
                    "image":entry.get("image") or None,
                    "url":entry.get("url") or None,
                    "sequence":entry.get("sequence") or None,
                    "Service_details": get_service_details_info(entry.get("title"), expertise_doctype.get("slug"))
                } 
                for entry in sorted(expertise_doctype.get("why_choose_8848"), key=lambda x: x.get("sequence"))
            ]
        why_choose_8848_details.update({"why_choose_8848":why_choose_8848_child})
    else:
        why_choose_8848_details.update({"why_choose_8848":[]})
    return why_choose_8848_details

def get_service_details_info(services_detail_title, slug):
    service_details_info = []
    logo_image = frappe.get_value('Expertise', filters={'slug':slug}, fieldname='bullet_image')
    service_details_doctype = frappe.get_doc("Service Details", services_detail_title)
    for entry in service_details_doctype.get("service_details_info"):
        service_details_info.append({
            "icon_image": logo_image,
            "service_info": entry.get("service_info")
        })
    return service_details_info

def get_advantages_details(expertise_doctype):
    advantage_details = {}
    if expertise_doctype.get("advantages_title"):
        advantage_details.update({"advantages_title": expertise_doctype.get("advantages_title")})
    else:
        advantage_details.update({"advantages_title": None})
    if expertise_doctype.get("advantages"):
        advantages_child = [
                {
                    "title":advantage.get("title") or None,
                    "short_description":advantage.get("short_description") or None,
                    "truncate_text":expertise_doctype.get("truncate_text_4"),
                    "image":advantage.get("image") or None,
                    "sequence":advantage.get("sequence") or None,
                    "url":advantage.get("url") or None
                } 
                for advantage in sorted(expertise_doctype.get("advantages"), key=lambda x: x.get("sequence"))
            ]
        advantage_details.update({"advantages":advantages_child})
    else:
        advantage_details.update({"advantages":[]})
    return advantage_details 

def get_case_study_details(expertise_doctype):
    case_study_details = {}
    case_study_default_field_values = {
        "case_study_title": None,
        "case_study_image": None,
        "case_study_description": None,
        "case_study_short_description": None
    }
    for field, default_value in case_study_default_field_values.items():
        case_study_details[field] = expertise_doctype.get(field, default_value)
    return case_study_details
    

def get_faq_details(expertise_doctype):
    faqs_details = {}
    if expertise_doctype.get("faqs_detail"):
        faqs_detail_child = [
                {
                    "title":faqs.get("title") or None,
                    "short_description":faqs.get("short_description") or None,
                    "url":faqs.get("url") or None,
                    "sequence":faqs.get("sequence") or None
                } 
                for faqs in sorted(expertise_doctype.get("faqs_detail"), key=lambda x: x.get("sequence"))
            ]
        faqs_details.update({"faqs_detail":faqs_detail_child})
    else:
        faqs_details.update({"faqs_detail":[]})
    return faqs_details

def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    return response

def error_response(err_msg, response):
    return {"status": "Error", "msg": err_msg, "data" : response}