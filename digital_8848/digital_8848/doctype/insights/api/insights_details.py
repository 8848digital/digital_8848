import frappe

@frappe.whitelist(allow_guest=True)
def get_insights_details(**kwargs):
    try:
        response = []
        title = kwargs.get("title")

        if title:
            insights_doctype = frappe.get_doc("Insights", {"title": title})

        insights_doctype_details = get_details(insights_doctype)
        response.append(insights_doctype_details)
        return success_response(data=response)

    except Exception as e:
        return error_response(f"An error occurred: {str(e)}", response)
    
def get_details(insights_doctype):
    insights_doctype_details = {}
    insights_doctype_details.update({
            "title": insights_doctype.get("title") or None,
            "tags": get_tag_details(insights_doctype) or [],
            "author": insights_doctype.get("author") or None,
            "published_on": insights_doctype.get("published_on") or None,
            "description": insights_doctype.get("description") or None,
        })

    return insights_doctype_details

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

def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    return response

def error_response(err_msg, response):
    return {"status": "Error", "msg": err_msg, "data" : response}