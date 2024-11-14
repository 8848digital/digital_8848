import frappe

@frappe.whitelist(allow_guest=True)
def get_technology():
    # Fetch platforms
    platforms = frappe.get_all(
        "Expertise",
        filters={"technology_type": "Platform"},
        fields=["title", "logo","url"]
    )

    # Fetch languages
    languages = frappe.get_all(
        "Expertise",
        filters={"technology_type": "Language"},
        fields=["title", "logo","url"]
    )

    # Structure the data as requested
    data = {
        "platforms": [{"title": platform["title"], "logo": platform["logo"],"url": platform["url"],} for platform in platforms],
        "languages": [{"title": language["title"], "logo": language["logo"],"url": language["url"],} for language in languages]
    }

    return success_response(data=data)


def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    return response

def error_response(err_msg, response):
    return {"status": "Error", "msg": err_msg, "data" : response}