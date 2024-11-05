import frappe

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
        
        response.append(combined_details)
        return success_response(data=response)
          
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}", response)
    
def get_details(case_study_doctype):
    case_study_doctype_details = {}
    case_study_doctype_details.update({
            "title": case_study_doctype.get("title") or None,
            "url": case_study_doctype.get("url") or None,
            "type": case_study_doctype.get("type") or None,
            "slug": case_study_doctype.get("slug") or None,
            "short_description": case_study_doctype.get("short_description") or None,
            "truncate_text": case_study_doctype.get("truncate_text_1"),
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
        "overview_description_1": case_study_doctype.get("overview_description") or None,
        "overview_description_2": case_study_doctype.get("overview_description_2") or None,
        "overview_truncate_text": case_study_doctype.get("truncate_text_2"),
    })
    return overview_details

def get_challenge_details(case_study_doctype):
    challenge_details = {}
    challenge_details.update({
        "challenge_title": case_study_doctype.get("challenge_title") or None,
        "challenge_short_description": case_study_doctype.get("challenge_short_description") or None,
        "challenge_truncate_text": case_study_doctype.get("truncate_text_3"),
        # "challenge_description": case_study_doctype.get("challenge_description") or None
    })

    if case_study_doctype.get("challenge_descriptions"):
        challenge_descriptions = [
            {
                "idx":desc.get("idx") or None,
                "challenge_description": desc.get("challenge_description") or None
            }
            for desc in case_study_doctype.get("challenge_descriptions")
        ]
        challenge_details.update({"challenge_descriptions": challenge_descriptions})
    else:
        challenge_details.update({"challenge_descriptions": []})
    
    return challenge_details


def get_objective_details(case_study_doctype):
    objective_details = {}
    objective_details.update({
        "objective_title": case_study_doctype.get("objective_title") or None,
        "objective_image": case_study_doctype.get("objective_image") or None,
        "objective_description": case_study_doctype.get("objective_description") or None,
        "objective_truncate_text": case_study_doctype.get("truncate_text_4")  
    })
    return objective_details

def get_solution_details(case_study_doctype):
    solution_details = {}
    solution_details.update({
        "solution_title": case_study_doctype.get("solution_title") or None,
        "solution_description_1": case_study_doctype.get("solution_description_1") or None,
        "solution_description_2": case_study_doctype.get("solution_description_2") or None,
        "solution_truncate_text": case_study_doctype.get("truncate_text_5") or None
    })
    return solution_details

def get_impact_details(case_study_doctype):
    impact_details = {}
    impact_details.update({
        "impact_title": case_study_doctype.get("impact_title") or None,
        "impact_short_description": case_study_doctype.get("impact_short_description") or None,
        "impact_description": case_study_doctype.get("impact_description") or None,
        "impact_truncate_text": case_study_doctype.get("truncate_text_6")
    })
    if case_study_doctype.get("impact_details"):
        impact_details_child = [
                {
                    "sequence":impact.get("sequence") or None,
                    "delivery_card":impact.get("delivery_card") or None,
                    "description":impact.get("description") or None,
                } 
                for impact in case_study_doctype.get("impact_details")
            ]
        impact_details.update({"impact_detail":impact_details_child})
    else:
        impact_details.update({"impact_detail":[]})
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

def error_response(err_msg, response):
    return {"status": "Error", "msg": err_msg, "data" : response}