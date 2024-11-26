import frappe

@frappe.whitelist(allow_guest=True)
def get_insights_listing(**kwargs):
    try:
        response = []
        type = kwargs.get("type")
        filters = {"publish_on_site" : 1}

        if type == "All" or type == "":
            filters = {"publish_on_site" : 1}
        elif type:
            filters = {"publish_on_site" : 1, "type":type}
        tab_list = get_tab_details()

        insights_doctypes_list = frappe.get_all("Insights", filters=filters, pluck="name", order_by="published_on desc")
        if insights_doctypes_list:
            for doctype in insights_doctypes_list:
                insights_doctype = frappe.get_doc("Insights", doctype)
                insights_doctype_details = {
                    "title": insights_doctype.get("title") or None,
                    "publish_on_site":insights_doctype.get("publish_on_site") or None,
                    "image": insights_doctype.get("image") or None,
                    "type": insights_doctype.get("type") or None,
                    "slug": insights_doctype.get("slug") or None,
                    "url": insights_doctype.get("url") or None,
                    "tags": get_tag_details(insights_doctype),
                    "short_description": insights_doctype.get("short_descriptions") or None
                }
                response.append(insights_doctype_details)
            return success_response(tab_list, response)
        else:
            return error_response("No data found.", response)
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}", response)

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

def get_tab_details():
    tab_list = [
            {
                "key": "",
                "title": "All"
            }
        ]
    insights_doc = frappe.get_all("Insights", filters={"publish_on_site" : 1}, fields=["type"], order_by="published_on desc")
    type_list = list({doc.get('type') for doc in insights_doc})
    for insight in type_list:
        type_detail = {
                "key": insight,
                "title": insight,
            }
        tab_list.append(type_detail)
    return tab_list

def success_response(tab_list=None, data=None):
    response = {"status": "success"}
    response["tab_list"] = tab_list
    response["data"] = data
    return response

def error_response(err_msg, response):
    return {"status": "Error", "msg": err_msg, "data" : response}