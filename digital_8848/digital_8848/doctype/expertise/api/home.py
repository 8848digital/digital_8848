import frappe

@frappe.whitelist(allow_guest=True)
def get_technology():
    # Fetch platforms
    platforms = frappe.get_all(
        "Expertise",
        filters={"technology_type": "Platform"},
        fields=["title","publish_on_site", "logo","url","sequence"],
        order_by="sequence"
    )

    # Fetch languages
    languages = frappe.get_all(
        "Expertise",
        filters={"technology_type": "Language"},
        fields=["title","publish_on_site", "logo","url","sequence"],
        order_by="sequence"
    )

    # Structure the data as requested
    data = {
        "platforms": [{"title": platform["title"],"publish_on_site": platform["publish_on_site"], "logo": platform["logo"],"url": platform["url"],"sequence":platform["sequence"]} for platform in platforms],
        "languages": [{"title": language["title"],"publish_on_site": language["publish_on_site"], "logo": language["logo"],"url": language["url"],"sequence":language["sequence"]} for language in languages]
    }

    return success_response(data=data)


def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    return response

def error_response(err_msg, response):
    return {"status": "Error", "msg": err_msg, "data" : response}