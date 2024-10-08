import frappe

@frappe.whitelist(allow_guest=True)
def get_meta_tags(**kwargs):
    try:
        response = {
            "status": "success",
            "data": {}  # Change this to a dictionary
        }

        page_name = kwargs.get("page_name") or None
        if not page_name:
            return error_response("Please provide a page name")

        meta_tags_docname = frappe.db.get_value("Meta Tags", {"page_name": page_name})
        if not meta_tags_docname:
            return error_response("No meta tag found with the given page name")

        meta_tags_doctype = frappe.get_doc("Meta Tags", meta_tags_docname)

        # Construct the response data
        meta_tag = {
            "page_name": meta_tags_doctype.get("page_name") or None,
            "meta_title": meta_tags_doctype.get("meta_title") or None,
            "fav_icon_image": meta_tags_doctype.get("fav_icon_image") or None,
            "robots": meta_tags_doctype.get("robots") or None,
            "description": meta_tags_doctype.get("description") or None
        }

        # Open Graph data (add as needed)
        open_graph = {
            "images": meta_tags_doctype.get("open_graph_images") or None,
            "title": meta_tags_doctype.get("open_graph_title") or None,
            "url": meta_tags_doctype.get("open_graph_url") or None,
            "type": meta_tags_doctype.get("open_graph_type") or None,
            "description": meta_tags_doctype.get("open_graph_description") or None,
        }

        # Twitter data (add as needed)
        twitter = {
            "card": meta_tags_doctype.get("twitter_card") or None,
            "site": meta_tags_doctype.get("twitter_site") or None,
            "title": meta_tags_doctype.get("twitter_title") or None,
            "description": meta_tags_doctype.get("twitter_description") or None,
            "image": meta_tags_doctype.get("twitter_image") or None,
        }

        # Assign dictionaries directly to the data field
        response["data"] = {
            "meta_tag": meta_tag,
            "open_graph": open_graph,
            "twitter": twitter
        }

        return response

    except Exception as e:
        return error_response(f"An error occurred: {str(e)}")

def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    return response

def error_response(err_msg):
    return {"status": "error", "error": err_msg}
