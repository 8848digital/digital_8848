import frappe

@frappe.whitelist(allow_guest=True)
def get_insights_details(**kwargs):
    try:
        response = []
        title = kwargs.get("title")
        slug = kwargs.get("slug")
        if not title and not slug:
            return error_response("Please provide a title or slug", response)
        if slug:
            insights_doctype_title = frappe.db.get_value("Insights",{'slug': kwargs.get("slug")})
            if not insights_doctype_title:
                return error_response("No insights found with the given slug", response)
            insights_doctype = frappe.get_doc("Insights",insights_doctype_title)
        if title:
            insights_doctype = frappe.get_doc("Insights", {"title": title})

        insights_doctype_details = get_details(insights_doctype)
        banner_details = get_banner_details(insights_doctype)
        capabilities_details = get_capabilities_details(insights_doctype)   
        functionality_details = get_functionality_details(insights_doctype) 
        integration_details = get_integration_details(insights_doctype)
        services_details = get_services_details(insights_doctype) 
        visibility_and_security_details = get_visibility_and_security_details(insights_doctype)  
        benefits_details = get_benefits_details(insights_doctype)

        combined_details = { **insights_doctype_details,**banner_details,**capabilities_details,**functionality_details,
                                **integration_details,**services_details,**visibility_and_security_details, **benefits_details }
        response.append(combined_details)
        return success_response(data=response)

    except Exception as e:
        return error_response(f"An error occurred: {str(e)}", response)
    
def get_details(insights_doctype):
    insights_doctype_details = {}
    insights_doctype_details.update({
            "title": insights_doctype.get("title") or None,
            "url": insights_doctype.get("url") or None,
            "type": insights_doctype.get("type") or None,
            "slug": insights_doctype.get("slug") or None,
            "short_description": insights_doctype.get("short_description") or None,
            "image": insights_doctype.get("image") or None
        })
    return insights_doctype_details

def get_banner_details(insights_doctype):
    banner_details = {}
    banner_details.update({
        "banner_title": insights_doctype.get("banner_title") or None,
        "banner_image": insights_doctype.get("banner_image") or None,
        "banner_description": insights_doctype.get("banner_description") or None
    })
    return banner_details

def get_capabilities_details(insights_doctype):
    capabilities_details = {}
    capabilities_title = insights_doctype.get("capabilities_title") if insights_doctype.get("capabilities_title") else None
    capabilities_details.update({"capabilities_title":capabilities_title})

    if insights_doctype.get("capabilities_detail"):
        capabilities_details_child = [
                    {
                        "title": capability.get("title") or None,
                        "description": capability.get("short_description") or None,
                        "url": capability.get("url") or None,
                        "sequence": capability.get("sequence") or None
                    }
                        for capability in sorted(insights_doctype.get("capabilities_detail"), key=lambda x: x.get("sequence"))
                ]
        capabilities_details.update({"capabilities_detail":capabilities_details_child})
    else:
        capabilities_details.update({"capabilities_detail":[]})
    return capabilities_details

def get_functionality_details(insights_doctype):
    functionality_details = {}
    functionality_title = insights_doctype.get("functionality_title") if insights_doctype.get("functionality_title") else None
    functionality_details.update({"functionality_title": functionality_title})

    if insights_doctype.get("functionality_detail"):
        functionality_details_child = [
            {
                "title": functionality.get("title") or None,
                "short_description": functionality.get("short_description") or None,
                "url": functionality.get("url") or None,
                "sequence": functionality.get("sequence") or None
            }
            for functionality in sorted(insights_doctype.get("functionality_detail"), key=lambda x: x.get("sequence"))
        ]
        functionality_details.update({"functionality_detail": functionality_details_child})
    else:
        functionality_details.update({"functionality_detail":[]})
    return functionality_details

def get_integration_details(insights_doctype):
    integration_details = {}
    integration_title = insights_doctype.get("integration_title") if insights_doctype.get("integration_title") else None
    integration_details.update({"functionality_title": integration_title})

    if insights_doctype.get("integration_detail"):
        integration_details_child = [
            {
                "title": integration.get("title") or None,
                "short_description": integration.get("short_description") or None,
                "url": integration.get("url") or None,
                "sequence": integration.get("sequence") or None
            }
            for integration in sorted(insights_doctype.get("integration_detail"), key=lambda x: x.get("sequence"))
        ]
        integration_details.update({"integration_detail": integration_details_child})
    else:
        integration_details.update({"integration_detail":[]})
    return integration_details

def get_services_details(insights_doctype):
    services_details = {}
    services_title = insights_doctype.get("services_title") if insights_doctype.get("services_title") else None
    services_details.update({"services_title": services_title})

    if insights_doctype.get("services_detail"):
        services_details_child = [
            {
                "title": service.get("title") or None,
                "image": service.get("image") or None,
                "url": service.get("url") or None,
                "sequence": service.get("sequence") or None,
                "Service_details": get_service_details_info(service.get("title"), insights_doctype.get("slug"))
            }
            for service in sorted(insights_doctype.get("services_detail"), key=lambda x: x.get("sequence"))
        ]
        services_details.update({"services_detail": services_details_child})
    else:
        services_details.update({"services_detail": []})
    return services_details

def get_service_details_info(services_detail_title, slug):
    service_details_info = []
    logo_image = frappe.get_value('Insights', filters={'slug':slug}, fieldname='bullet_image')
    service_details_doctype = frappe.get_doc("Service Details", services_detail_title)
    for entry in service_details_doctype.get("service_details_info"):
        service_details_info.append({
            "icon_image": logo_image,
            "service_info": entry.get("service_info")
        })
    return service_details_info

def get_visibility_and_security_details(insights_doctype):
    visibility_and_security_details = {}
    visibility_and_security_details.update({
        "visibility_and_security_title": insights_doctype.get("visibility_and_security_title") or None,
        "visibility_and_security_short_description": insights_doctype.get("visibility_and_security_short_description") or None
    })
    return visibility_and_security_details

def get_benefits_details(insights_doctype):
    benefits_details = {}
    benefits_title = insights_doctype.get("benefits_title") if insights_doctype.get("benefits_title") else None
    benefits_details.update({"benefits_title": benefits_title}) 

    if insights_doctype.get("benefits_detail"):
        benefits_details_child = [
            {
                "title": benefit.get("title") or None,
                "short_description": benefit.get("description") or None,
                "url": benefit.get("url") or None,
                "sequence": benefit.get("sequence") or None,
                "logo": benefit.get("logo") or None
            }
            for benefit in sorted(insights_doctype.get("benefits_detail"), key=lambda x: x.get("sequence"))
        ]
        benefits_details.update({"benefits_detail": benefits_details_child})
    else:
        benefits_details.update({"benefits_detail": []})
    return benefits_details

def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    return response

def error_response(err_msg, response):
    return {"status": "Error", "msg": err_msg, "data" : response}