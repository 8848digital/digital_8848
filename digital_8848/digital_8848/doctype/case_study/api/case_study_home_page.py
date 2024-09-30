import frappe

@frappe.whitelist(allow_guest=True)
def get_home_page_case_study(**kwargs):
    try:
        response = []
        case_study_doctype_title = frappe.db.get_value("Case Study",{"display_on_home_page":1})
        if not case_study_doctype_title:
            return error_response("No case study found with the display_on_home_page checkbox enabled.")
        
        case_study_doctype = frappe.get_doc("Case Study",case_study_doctype_title)
        case_study_doctype_details = get_details(case_study_doctype)
        banner_details = get_banner_details(case_study_doctype)
        overview_details = get_overview_details(case_study_doctype)
        challenge_details = get_challenge_details(case_study_doctype)
        objective_details = get_objective_details(case_study_doctype)
        solution_details = get_solution_details(case_study_doctype)
        impact_details = get_impact_details(case_study_doctype)
        tag_details = get_tag_details(case_study_doctype)

        combined_details = { **case_study_doctype_details,**banner_details,**overview_details,**challenge_details,
                                **objective_details,**solution_details,**impact_details,**tag_details }
        combined_details.update({"display_on_home_page":1})

        response.append(combined_details)
        return success_response(data=response)
          
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}")

def get_details(case_study_doctype):
    case_study_doctype_details = {}
    case_study_doctype_details.update({
            "title": case_study_doctype.get("title") or None,
            "url": case_study_doctype.get("url") or None,
            "type": case_study_doctype.get("type") or None,
            "slug": case_study_doctype.get("slug") or None,
            "short_description": case_study_doctype.get("short_description") or None,
            "image": case_study_doctype.get("image") or None
        })
    return case_study_doctype_details

def get_banner_details(case_study_doctype):
    banner_details = {}
    banner_details.update({
        "banner_title": case_study_doctype.get("banner_title") or None,
        "banner_image": case_study_doctype.get("banner_image") or None,
        "banner_description": case_study_doctype.get("banner_description") or None
    })
    return banner_details

def get_overview_details(case_study_doctype):
    overview_details = {}
    overview_details.update({
        "overview_title": case_study_doctype.get("overview_title") or None,
        "overview_description": case_study_doctype.get("overview_description") or None
    })
    return overview_details

def get_challenge_details(case_study_doctype):
    challenge_details = {}
    challenge_details.update({
        "challenge_title": case_study_doctype.get("challenge_title") or None,
        "challenge_short_description": case_study_doctype.get("challenge_short_description") or None,
        "challenge_description": case_study_doctype.get("challenge_description") or None
    })
    return challenge_details

def get_objective_details(case_study_doctype):
    objective_details = {}
    objective_details.update({
        "objective_title": case_study_doctype.get("objective_title") or None,
        "objective_description": case_study_doctype.get("objective_description") or None
    })
    return objective_details

def get_solution_details(case_study_doctype):
    solution_details = {}
    solution_details.update({
        "solution_title": case_study_doctype.get("solution_title") or None,
        "solution_description": case_study_doctype.get("solution_description") or None
    })
    return solution_details

def get_impact_details(case_study_doctype):
    impact_details = {}
    impact_details.update({
        "impact_title": case_study_doctype.get("impact_title") or None,
        "impact_short_description": case_study_doctype.get("impact_short_description") or None,
        "impact_description": case_study_doctype.get("impact_description") or None
    })
    return impact_details

def get_tag_details(case_study_doctype):
    tag_details = {}
    if case_study_doctype.get("tag_detail"):
        tag_details_child = [
                {
                    "tag_name":tag.get("tag_name") or None,
                } 
                for tag in case_study_doctype.get("tag_detail")
            ]
        tag_details.update({"tag_detail":tag_details_child})
    else:
        tag_details.update({"tag_detail":[]})
    return tag_details

def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    return response

def error_response(err_msg):
    return {"status": "error", "error": err_msg}