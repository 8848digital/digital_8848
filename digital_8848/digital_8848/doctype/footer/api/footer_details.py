import frappe
from collections import defaultdict

@frappe.whitelist(allow_guest=True)
def get_footer_details(**kwargs):
    try:
        category = frappe.qb.DocType('Category')

        category_details = frappe.qb.from_(
            category
        ).select(
            category.category_name,
            category.old_parent
        ).where(
		(category.enable_category == 1) & (category.is_group == 0)
	    ).run(as_dict=True)
        
        categories = defaultdict(list)
        for item in category_details:
            categories[item["old_parent"]].append(item["category_name"])
        formatted_categories = dict(categories)

        footer_doc = frappe.get_doc("Footer")

        social_media_links = []
        for media in footer_doc.social_media_links:
            media_data = {
                "social_media_icon" : media.social_media_icon,
                "social_media_url" : media.social_media_url
            }
            social_media_links.append(media_data)

        footer_data = {}
        footer_data["footer_logo"] = footer_doc.footer_logo
        footer_data["social_media_links"] = social_media_links
        footer_data["categories"] = formatted_categories

        return success_response(data=footer_data)

    except frappe.DoesNotExistError:
        return error_response("Footer document not found.")
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}")
    
def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    return response

def error_response(err_msg):
    return {"status": "error", "error": err_msg}