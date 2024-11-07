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
        client_details = get_client_details(case_study_doctype)
        challenge_details = get_challenge_details(case_study_doctype)
        reason_details = get_reason_details(case_study_doctype)
        solution_details = get_solution_details(case_study_doctype)
        result_details = get_result_details(case_study_doctype)
        next_steps_details = get_next_steps_details(case_study_doctype)
        impact_details = get_impact_details(case_study_doctype)

        combined_details = { **case_study_doctype_details,**banner_details,**client_details,**challenge_details,
                                **reason_details,**solution_details,**result_details,**next_steps_details,**impact_details }
        
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

def get_client_details(case_study_doctype):
    client_details = {}
    client_details.update({
        "client_title": case_study_doctype.get("client_title") or None,
        "client_description": case_study_doctype.get("client_description") or None
    })
    return client_details

def get_challenge_details(case_study_doctype):
    challenge_details = {}
    challenge_details.update({
        "challenge_title": case_study_doctype.get("challenge_title") or None,
        "challenge_description": case_study_doctype.get("challenge_description") or None
    })
    return challenge_details

def get_reason_details(case_study_doctype):
    reason_details = {}
    reason_details.update({
        "reason_title": case_study_doctype.get("reason_title") or None,
        "reason_description": case_study_doctype.get("reason_description") or None
    })
    return reason_details

def get_solution_details(case_study_doctype):
    solution_details = {}
    solution_details.update({
        "solution_title": case_study_doctype.get("solution_title") or None,
        "solution_description": case_study_doctype.get("solution_description") or None
    })
    return solution_details

def get_result_details(case_study_doctype):
    result_details = {}
    result_details.update({
        "result_title": case_study_doctype.get("result_title") or None,
        "result_description": case_study_doctype.get("result_description") or None
    })
    return result_details

def get_next_steps_details(case_study_doctype):
    next_steps_details = {}
    next_steps_details.update({
        "next_steps_title": case_study_doctype.get("next_steps_title") or None,
        "next_steps_description": case_study_doctype.get("next_steps_description") or None
    })
    return next_steps_details

def get_impact_details(case_study_doctype):
    impact_details = {}
    impact_details.update({
        "impact_title": case_study_doctype.get("impact_title") or None,
        "impact_description": case_study_doctype.get("impact_description") or None
    })
    return impact_details

def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    return response

def error_response(err_msg, response):
    return {"status": "Error", "msg": err_msg, "data" : response}