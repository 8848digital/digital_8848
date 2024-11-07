import frappe

@frappe.whitelist(allow_guest=True)
def get_industry_details(**kwargs):
    try:
        filters = {}
        response = []
        title = kwargs.get("title")
        slug = kwargs.get("slug")
        if not title and not slug:
            return error_response("Please Provide a title or slug.", response)
        if slug:
            filters["slug"] = kwargs.get("slug")
        if title:
            filters["title"] = kwargs.get("title")

        
        industries = frappe.get_all("Industry", filters=filters, 
                                    fields=["name", "title", "url", "slug", "sequence", "image", "short_description", 
                                            "banner_title", "banner_image", "banner_description", "industry_detail_sub_title", 
                                            "advantages_sub_title", "section_title"]) 
        
        if industries:
            industry_names = [industry.name for industry in industries]
            industry_details = frappe.get_all(
                "Industry Detail",
                filters={"parent": ["in", industry_names]},
                fields=["parent", "title", "description"],
                order_by="idx ASC"
            )
            industry_details_map = get_parent_child_map(industry_details)
            advantages = frappe.get_all("Advantages", filters={"parent": ["in", industry_names]}, 
                                        fields=["parent", "title", "short_description", "sequence"], 
                                        order_by="sequence asc")
            advantages_map = get_parent_child_map(advantages)
            services = frappe.get_all("Service Table", filters={"parent": ["in", industry_names]}, 
                                        fields=["parent", "service_name", "service_image", "sequence"], 
                                        order_by="sequence asc")
            service_map = get_parent_child_map(services)
            for industry in industries:
                industry.update({"industry_detail": industry_details_map.get(industry.name) or []})
                industry.update({"advantages": advantages_map.get(industry.name) or []})
                services_with_section_title = {
                    "section_title": industry.get("section_title"),
                    "services": [
                        {
                            "service_name": service.get("service_name"),
                            "service_image": service.get("service_image"),
                            "sequence": service.get("sequence")
                        }
                        for service in service_map.get(industry.name, [])
                    ]
                }
                
                industry.update({"service_table": services_with_section_title})
                industry.pop("name")
                response = industries
            return success_response(data=response)
        else:
            return error_response("No data found", response)
    
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}", response)


@frappe.whitelist(allow_guest=True)
def get_industry_list(**kwargs):
    try:
        response = []
        industry_banner = frappe.get_value("Banner", "Industry", ["name"], as_dict = 1) or {}
        industry_banner_details = frappe.get_all("Banner Detail", {"parent": industry_banner.get("name")}, ["title", "short_description", "banner_image"])           
        industry_banner.update({"banner_details": industry_banner_details})
        industries = frappe.get_all("Industry", filters={"publish_on_site" : 1}, fields = ["title", "image", "short_description", "truncate_text_1 as truncate_text", "slug", "sequence", "url"])
        industries = sorted(industries, key=lambda x: x.get("sequence") or 0)
        industry_banner.update({"industries": industries})
        industry_banner.pop("name", None)
        response = industry_banner
        return success_response(data = response)
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}", response)

    
def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    if id:
        response["data"] = {"id": id, "name": id}
    return response
def error_response(err_msg, response):
    return {"status": "Error", "msg": err_msg, "data" : response}


def get_parent_child_map(details):
    parent_child_map = {}
    for detail in details:
        industry_titles = [industry.title for industry in frappe.get_all("Industry Detail", filters={"parent": detail.get("parent")}, fields=["title"])]
        advantages_titles = [adv.title for adv in frappe.get_all("Advantages", filters={"parent": detail.get("parent")}, fields=["title"])]
        if detail.get("title") in industry_titles:
            detail["truncate_text"] = frappe.db.get_value('Industry', detail.get("parent"), 'truncate_text_1')
        elif detail.get("title") in advantages_titles:
            detail["truncate_text"] = frappe.db.get_value('Industry', detail.get("parent"), 'truncate_text_2')

        parent = detail.pop("parent", None)
        if parent is not None:
            if parent_child_map.get(parent):
                parent_child_map[parent].append(detail)
            else:
                parent_child_map[parent] = [detail]
    return parent_child_map



