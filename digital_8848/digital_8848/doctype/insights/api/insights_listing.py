import frappe

@frappe.whitelist(allow_guest=True)
def get_insights_listing(**kwargs):
    """
    Retrieves a list of insights with optional filters for type and handles pagination.
    """
    try:
        limit = kwargs.get("limit")
        page_no = kwargs.get("page_no")
        
        limit = int(limit) if limit and limit.isdigit() else 10  # Default limit is 10
        page_no = int(page_no) if page_no and page_no.isdigit() and int(page_no) > 0 else 1  # Default to page 1

        start = (page_no - 1) * limit

        filters = {"publish_on_site": 1}
        type_filter = kwargs.get("type")

        if type_filter and type_filter != "All":
            filters["type"] = type_filter

        tab_list = get_tab_details()
        insights_list = frappe.get_all(
            "Insights",
            filters=filters,
            fields=["name"],
            order_by="published_on desc",
            start=start,
            limit_page_length=limit
        )

        total_count = frappe.db.count("Insights", filters=filters)

        response = []
        for insight in insights_list:
            insights_doc = frappe.get_doc("Insights", insight["name"])
            response.append({
                "title": insights_doc.get("title") or None,
                "publish_on_site": insights_doc.get("publish_on_site") or None,
                "image": insights_doc.get("image") or None,
                "type": insights_doc.get("type") or None,
                "slug": insights_doc.get("slug") or None,
                "url": insights_doc.get("url") or None,
                "tags": get_tag_details(insights_doc),
                "short_description": insights_doc.get("short_descriptions") or None
            })

        return success_response(tab_list, response, total_count)

    except Exception as e:
        frappe.log_error(f"Error in get_insights_listing: {str(e)}")
        return error_response(f"An error occurred: {str(e)}", [])


def get_tag_details(insights_doc):
    """
    Retrieves tag details for an insights document.
    """
    tags = insights_doc.get("tags") or []
    return [{"tag_name": tag.get("tag_name") or None} for tag in tags]


def get_tab_details():
    """
    Generates the tab details including unique types.
    """
    tab_list = [{"key": "", "title": "All"}]
    insights_types = frappe.get_all(
        "Insights",
        filters={"publish_on_site": 1},
        fields=["type"],
        order_by="published_on desc"
    )

    unique_types = {doc["type"] for doc in insights_types if doc["type"]}
    for insight_type in unique_types:
        tab_list.append({"key": insight_type, "title": insight_type})

    return tab_list


def success_response(tab_list=None, data=None, total_count=None):
    """
    Constructs a success response.
    """
    return {
        "status": "success",
        "total_count": total_count,
        "tab_list": tab_list,
        "data": data
    }


def error_response(err_msg, response):
    """
    Constructs an error response.
    """
    return {
        "status": "error",
        "msg": err_msg,
        "data": response
    }
