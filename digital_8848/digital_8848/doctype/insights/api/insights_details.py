import frappe
import re
from frappe.utils import get_url

@frappe.whitelist(allow_guest=True)
def get_insights_details(**kwargs):
    try:
        response = []
        slug = kwargs.get("slug")

        if frappe.db.exists("Insights", {"slug": slug}):
            insights_doctype = frappe.get_doc("Insights", {"slug": slug})

        if frappe.db.exists("Insights", {"title": slug}):
            insights_doctype = frappe.get_doc("Insights", {"title": slug})

        insights_doctype_details = get_details(insights_doctype)
        response.append(insights_doctype_details)
        return success_response(data=response)

    except Exception as e:
        return error_response(f"An error occurred: {str(e)}", response)
    
def get_details(insights_doctype):
    insights_doctype_details = {}
    base_url = get_url()
    description = insights_doctype.get("description") or None
    if description:
        description = re.sub(
            r'src="(/files/[^"]+)"',
            rf'src="{base_url}\1"',
            description
        )
    insights_doctype_details.update({
            "title": insights_doctype.get("title") or None,
            "image": insights_doctype.get("image") or None,
            "tags": get_tag_details(insights_doctype) or [],
            "author": insights_doctype.get("author") or None,
            "published_on": insights_doctype.get("published_on") or None,
            "description": description or None,
        })

    return insights_doctype_details

def get_tag_details(insights_doctype):
    tag_details= []
    
    if insights_doctype.get("tags"):
        tag_details = [
                {
                    "tag_name":tag.get("tag_name") or None,
                } 
                for tag in insights_doctype.get("tags")
            ]
    return tag_details

def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    return response

def error_response(err_msg, response):
    return {"status": "Error", "msg": err_msg, "data" : response}