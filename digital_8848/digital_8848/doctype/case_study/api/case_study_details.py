import re
import frappe
from frappe.utils import get_url
from bs4 import BeautifulSoup
from digital_8848.digital_8848.doctype.case_study.api.case_study_listing import get_button_url

@frappe.whitelist(allow_guest=True)
def get_case_study_details(**kwargs):
    try:
        response = []
        title = kwargs.get("title")
        slug = kwargs.get("slug")
        if not title and not slug:
            return error_response("Please provide a title or slug",response)
        if slug:
            case_study_doctype_title = frappe.db.get_value("Case Study",{'slug': kwargs.get("slug")})
            if not case_study_doctype_title:
                return error_response("No case study found with the given slug",response)
            case_study_doctype = frappe.get_doc("Case Study",case_study_doctype_title)
        if title:
            case_study_doctype = frappe.get_doc("Case Study", {"title": title})
        base_url = get_url()
        tab_list = get_tab_details(case_study_doctype)
        case_study_doctype_details = get_details(case_study_doctype)
        banner_details = get_banner_details(case_study_doctype)
        client_details = get_client_details(case_study_doctype, base_url)
        challenge_details = get_challenge_details(case_study_doctype, base_url)
        reason_details = get_reason_details(case_study_doctype, base_url)
        solution_details = get_solution_details(case_study_doctype, base_url)
        result_details = get_result_details(case_study_doctype, base_url)
        next_steps_details = get_next_steps_details(case_study_doctype, base_url)
        impact_details = get_impact_details(case_study_doctype, base_url)
        tag_details = get_tag_details(case_study_doctype)

        combined_details = { **case_study_doctype_details,**banner_details,**client_details,**challenge_details,
                                **reason_details,**solution_details,**result_details,**next_steps_details,**impact_details,**tag_details  }
        
        response.append(combined_details)
        return success_response(tab_list, response)

    except Exception as e:
        return error_response(f"An error occurred: {str(e)}", response)
    
def get_details(case_study_doctype):
    case_study_doctype_details = {}
    case_study_doctype_details.update({
            "title": case_study_doctype.get("title") or None,
            "publish_on_site":case_study_doctype.get("publish_on_site") or None,
            "url":get_button_url(case_study_doctype) or None,
            "type": case_study_doctype.get("type") or None,
            "slug": case_study_doctype.get("slug") or None,
            "short_description": case_study_doctype.get("short_description") or None,
            "truncate_text": case_study_doctype.get("truncate_text_1"),
            "image": case_study_doctype.get("image") or None
        })
    return case_study_doctype_details

def get_banner_details(expertise_doctype):
    banner_details = {}
    banner_details_default_field_values = {
        "banner_title": None,
        "banner_image": None,
        "banner_description": None,
        "cta_btn_url": None,
        "cta_btn_text": None,
        "btn_description": None 
    }
    for field, default_value in banner_details_default_field_values.items():
        banner_details[field] = expertise_doctype.get(field, default_value)
    return banner_details

def get_client_details(case_study_doctype, base_url):
    client_details = {}
    client_details.update({
        "client_title": case_study_doctype.get("client_title") or None,
        "client_description": validate_txt_editor_content(update_image_url(case_study_doctype.get("client_description"), base_url)) or None
    })
    return client_details

def get_challenge_details(case_study_doctype, base_url):
    challenge_details = {}
    challenge_details.update({
        "challenge_title": case_study_doctype.get("challenge_title") or None,
        "challenge_description": validate_txt_editor_content(update_image_url(case_study_doctype.get("challenge_description"), base_url)) or None,
        "bullet_points": validate_txt_editor_content(update_image_url(case_study_doctype.get("bullet_points"), base_url)) or None,
    })
    return challenge_details

def get_reason_details(case_study_doctype, base_url):
    reason_details = {}
    reason_details.update({
        "reason_title": case_study_doctype.get("reason_title") or None,
        "reason_image": case_study_doctype.get("reason_image") or None,
        "reason_description": validate_txt_editor_content(update_image_url(case_study_doctype.get("reason_description"), base_url)) or None
    })
    return reason_details

def get_solution_details(case_study_doctype, base_url):
    solution_details = {}
    solution_details.update({
        "solution_title": case_study_doctype.get("solution_title") or None,
        "solution_description": validate_txt_editor_content(update_image_url(case_study_doctype.get("solution_description"), base_url)) or None
    })
    return solution_details

def get_result_details(case_study_doctype, base_url):
    result_details = {}
    result_details.update({
        "result_title": case_study_doctype.get("result_title") or None,
        "result_description": validate_txt_editor_content(update_image_url(case_study_doctype.get("result_description"), base_url)) or None
    })
    return result_details

def get_next_steps_details(case_study_doctype, base_url):
    next_steps_details = {}
    next_steps_details.update({
        "next_steps_title": case_study_doctype.get("next_steps_title") or None,
        "next_steps_description": validate_txt_editor_content(update_image_url(case_study_doctype.get("next_steps_description"), base_url)) or None
    })
    return next_steps_details

def get_impact_details(case_study_doctype, base_url):
    impact_details = {}
    impact_details_child = [
        {
            "impact_counts":impact.get("impact_counts") or None,
            "description":impact.get("description") or None
        } 
        for impact in case_study_doctype.get("impact_detail")
    ]
    impact_details.update({
        "impact_title": case_study_doctype.get("impact_title") or None,
        "impact_description": validate_txt_editor_content(update_image_url(case_study_doctype.get("impact_description"), base_url)) or None,
        "impact_detail": impact_details_child,
    })
    return impact_details

def get_tag_details(case_study_doctype):
    tag_details = {}
    if case_study_doctype.get("tags"):
        tag_details_child = [
                {
                    "tag_name":tag.get("tag_name") or None,
                } 
                for tag in case_study_doctype.get("tags")
            ]
        tag_details.update({"tag_detail":tag_details_child})
    else:
        tag_details.update({"tag_detail":[]})
    return tag_details


def get_tab_details(case_study_doctype):
    case_study_meta_fields = frappe.get_meta("Case Study")
    tab_list = []
    
    for field in case_study_meta_fields.get("fields"):
        if field.fieldtype == "Tab Break":
            title_field_name = f"{field.label.lower().replace(' ', '_')}_title"
            if hasattr(case_study_doctype, title_field_name):
                if getattr(case_study_doctype, title_field_name):
                    tab_detail = {
                        "label": getattr(case_study_doctype, title_field_name),  
                        "href": field.fieldname
                    }
                    if field.label != "Details":
                        tab_list.append(tab_detail)
    
    return tab_list

def update_image_url(description, base_url):
    if description:
        description = re.sub(
            r'src="(/files/[^"]+)"',
            rf'src="{base_url}\1"',
            description
        )
        return description
    else:
        return description

def success_response(tab_section=None, data=None):
    response = {"status": "success"}
    response["tab_section"] = tab_section
    response["data"] = data
    return response

def error_response(err_msg, response):
    return {"status": "Error", "msg": err_msg, "data" : response}


def validate_txt_editor_content(txt):
    if txt:
        soup = BeautifulSoup(txt, "html.parser")
        if soup.get_text(strip=True) == '':
            descrption = None
        else:
            descrption = text_editor_content_modifications(str(soup))
        return descrption

def text_editor_content_modifications(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    for li in soup.find_all("li", {"data-list": "bullet"}):
        parent_ol = li.find_parent("ol")
        if parent_ol:
            new_ul = soup.new_tag("ul")
            parent_ol.insert_before(new_ul)
            for bullet_li in parent_ol.find_all("li", {"data-list": "bullet"}):
                new_ul.append(bullet_li.extract())
            if not parent_ol.find_all("li"):
                parent_ol.decompose()
                
    return str(soup)
