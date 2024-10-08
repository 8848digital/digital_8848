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

        response_data = {
            "page_name": meta_tags_doctype.get("page_name") or "home",
            "title": "8848 DIGITAL LLP",
            "description": "At 8848 Digital, we combine cutting-edge technology with deep industry expertise to drive your digital transformation.",
            "icons": {
                "icon": "/favicon/8848 Favicon_32x32-White.svg"
            },
            "robots": meta_tags_doctype.get("robots") or "index,follow"
        }

        # Open Graph data
        open_graph = {
            "type": None,
            "url": None,
            "images": "/favicon/8848 Favicon_32x32-White.svg",
            "title": "8848 DIGITAL LLP",
            "description": "At 8848 Digital, we combine cutting-edge technology with deep industry expertise to drive your digital transformation."
        }

        # Twitter data
        twitter = {
            "card": "summary_large_image",
            "title": "8848 DIGITAL LLP",
            "description": "At 8848 Digital, we combine cutting-edge technology with deep industry expertise to drive your digital transformation.",
            "image": "/favicon/8848 Favicon_32x32-White.svg"
        }

        # Construct the final response
        response = {
           
                "status": "success",
                "data": {
                    **response_data,
                    "openGraph": open_graph,
                    "twitter": twitter
                }
        }

        return response

    except Exception as e:
        return error_response(f"An error occurred: {str(e)}")

def error_response(err_msg):
    return {"status": "error", "error": err_msg}
