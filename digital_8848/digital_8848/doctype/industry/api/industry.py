import frappe

@frappe.whitelist(allow_guest=True)
def get_industry_details(**kwargs):
    try:
        filters = {}
        if kwargs.get("title"):
            filters["title"] = kwargs.get("title")
        industries = frappe.get_all("Industry", filters = filters, fields = ["name","title", "url", "slug", "sequence", "image", "short_description", "banner_title", "banner_image", "banner_description", "industry_detail_sub_title", "advantages_sub_title"])
        industry_names = [industry.name for industry in industries]
        industry_details = frappe.get_all("Industry Detail", filters = {"parent": ["in", industry_names]}, fields = ["parent","title", "description"])
        industry_details_map = get_parent_child_map(industry_details)
        advantages = frappe.get_all("Advantages", filters = {"parent": ["in", industry_names]}, fields = ["parent","title", "short_description", "image", "sequence"])
        advantages_map = get_parent_child_map(advantages)
        for industry in industries:
            industry.update({"industry_detail": industry_details_map.get(industry.name) or []})
            industry.update({"advantages": advantages_map.get(industry.name) or []})
            industry.pop("name")
        return success_response(industries)
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}")
    

@frappe.whitelist(allow_guest=True)
def get_industry_list(**kwargs):
    try:
        industry_banner = frappe.get_value("Banner", "Industry", ["name", "title", "slug"], as_dict = 1) or {}
        industry_banner_details = frappe.get_value("Banner Detail", {"parent": industry_banner.get("name")}, ["title", "short_description", "banner_image"], as_dict = 1) or {}
        industries = frappe.get_all("Industry", fields = ["banner_title", "banner_image", "banner_description", "slug", "sequence"])
        industry_banner.update(industry_banner_details)
        industry_banner.update({"industries": industries})
        industry_banner.pop("name", None)
        return success_response(industry_banner)
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}")

    
def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    if id:
        response["data"] = {"id": id, "name": id}
    return response
def error_response(err_msg):
    return {"status": "error", "error": err_msg}


def get_parent_child_map(details):
    parent_child_map = {}
    for detail in details:
        parent = detail.pop("parent", None)
        if parent is not None:
            if parent_child_map.get(parent):
                parent_child_map[parent].append(detail)
            else:
                parent_child_map[parent] = [detail]
    return parent_child_map
    
        


