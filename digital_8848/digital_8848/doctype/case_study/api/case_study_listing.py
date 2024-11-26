import frappe

@frappe.whitelist(allow_guest=True)
def get_case_study_listing(**kwargs):
    try:
        response = []
        filters = {"publish_on_site": 1,}
        if kwargs.get("type"):
            filters.update({"type": kwargs.get("type")})
        tab_list = get_tab_details()
        case_study_doctypes_list = frappe.get_all("Case Study", filters=filters, pluck="name")
        if case_study_doctypes_list:
            for doctype in case_study_doctypes_list:
                case_study_doctype = frappe.get_doc("Case Study", doctype)
                case_study_doctype_details = {
                    "title": case_study_doctype.get("title") or None,
                    "publish_on_site":case_study_doctype.get("publish_on_site") or None,
                    "image": case_study_doctype.get("image") or None,
                    "short_description": case_study_doctype.get("short_description") or None,
                    "truncate_text": case_study_doctype.get("truncate_text_1"),
                    "slug": case_study_doctype.get("slug") or None,
                    "url":get_button_url(case_study_doctype) or None,
                    "type": case_study_doctype.get("type") or None,
                    "tag_detail": get_tag_details(case_study_doctype) or []
                }
                response.append(case_study_doctype_details)
            return success_response(tab_list, response)
        else:
            return error_response("No data found.", response)
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}", response)
    
def get_tag_details(case_study_doctype):
    tag_details_child = []
    
    if case_study_doctype.get("tags"):
        tag_details_child = [
                {
                    "tag_name":tag.get("tag_name") or None,
                } 
                for tag in case_study_doctype.get("tags")
            ]
    return tag_details_child

def get_tab_details():
    tab_list = [
            {
                "key": "",
                "title": "All"
            }
        ]
    case_study_doc = frappe.get_all("Case Study", filters={"publish_on_site" : 1}, fields=["type"])
    type_list = list({doc.get('type') for doc in case_study_doc})
    for case_study in type_list:
        type_detail = {
                "key": case_study,
                "title": case_study,
            }
        tab_list.append(type_detail)
    return tab_list

def success_response(tab_list = None, data=None):
    response = {"status": "success"}
    response["tab_list"] = tab_list
    response["data"] = data
    return response

def error_response(err_msg, response):
    return {"status": "Error", "msg": err_msg, "data" : response}


def get_button_url(case_study_doctype):
    if case_study_doctype.get("button_url") and case_study_doctype.get("use_button_url") == 1:
        url = case_study_doctype.get("button_url")
    else:
        url = case_study_doctype.get("url")
    return url    