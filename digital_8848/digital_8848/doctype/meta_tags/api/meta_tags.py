import frappe

@frappe.whitelist(allow_guest=True)
def get_meta_tags(**kwargs):
    try:
        page_name = kwargs.get("page_name") or None
        if not page_name:
            return error_response("Please provide a page name")

        meta_tags_docname = frappe.db.get_value("Meta Tags", {"page_name": page_name})
        if not meta_tags_docname:
            return error_response("No meta tag found with the given page name")

        meta_tags_doctype = frappe.get_doc("Meta Tags", meta_tags_docname)

        # Fetching keywords from the Key Words child table
        keywords = ", ".join(
            [kw.get("tag") for kw in meta_tags_doctype.get("key_words") if kw.get("tag")]
        )
        response_data = {
            "page_name": meta_tags_doctype.get("page_name") or None,
            "title": meta_tags_doctype.get("meta_title") or None,
            "description": meta_tags_doctype.get("description") or None,
            "icons": {
                "icon": meta_tags_doctype.get("fav_icon_image") or None,
            },
            "robots": meta_tags_doctype.get("robots") or None,
            "keywords": keywords or None
        }

        # Open Graph data - Dynamic assignment
        open_graph = {
            "type": meta_tags_doctype.get("open_graph_type") or None,
            "url": meta_tags_doctype.get("open_graph_url") or None,
            "images": meta_tags_doctype.get("open_graph_images") or None,
            "title": meta_tags_doctype.get("open_graph_title") or None,
            "description": meta_tags_doctype.get("open_graph_description") or None,
        }

        # Twitter data - Dynamic assignment
        twitter = {
            "card": meta_tags_doctype.get("twitter_card") or None,
            "title": meta_tags_doctype.get("twitter_title") or None,
            "description": meta_tags_doctype.get("twitter_description") or None,
            "image": meta_tags_doctype.get("twitter_image") or None,
        }

        # Remove openGraph from the response if all values are None
        if all(value is None for value in open_graph.values()):
            open_graph = {}

        # Remove twitter from the response if all values are None
        if all(value is None for value in twitter.values()):
            twitter = {}

        # Construct the final response
        response = {
            "status": "success",
            "data": {
                **response_data,
                "openGraph": open_graph,  # This will be empty if all values were None
                "twitter": twitter          # This will be empty if all values were None
            }
        }

        return response

    except Exception as e:
        return error_response(f"An error occurred: {str(e)}")

def error_response(err_msg):
    return {"status": "error", "error": err_msg}
