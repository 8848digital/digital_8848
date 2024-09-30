import frappe
from collections import defaultdict

@frappe.whitelist(allow_guest=True)
def get_footer_details(**kwargs):
    try:
        category = frappe.qb.DocType('Category')

        base_category_details = get_base_category_details(category)
        parent_categories = get_parent_category_details(category)
        formatted_categories = get_formatted_category(parent_categories, base_category_details)
        
        footer_doc = frappe.get_doc("Footer")
        social_media_links = []
        for media in footer_doc.social_media_links:
            media_data = {
                "social_media_icon" : media.social_media_icon,
                "social_media_url" : media.social_media_url
            }
            social_media_links.append(media_data)

        legal_section_details = get_legal_section_details(footer_doc)
        footer_data = {}
        footer_data["footer_logo"] = footer_doc.footer_logo
        footer_data["social_media_links"] = social_media_links
        footer_data["categories"] = formatted_categories
        footer_data["legal_section"] = legal_section_details

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

def get_base_category_details(category):
    base_category_details = frappe.qb.from_(
        category
    ).select(
        category.category_name,
        category.old_parent,
        category.label,
        category.slug,
        category.sequence,
        category.url,
        category.image,
        category.short_description
    ).where(
    (category.enable_footer == 1) & (category.is_group == 0)
    ).run(as_dict=True)
    return base_category_details

def get_parent_category_details(category):
    parent_category_details = frappe.qb.from_(
            category
        ).select(
            category.category_name,
            category.old_parent
        ).where(
        (category.enable_footer == 1) & (category.is_group == 1)
        ).run(as_dict=True)
    parent_categories = []
    parent_of_parent_category = []
    for category in parent_category_details:
        if category.category_name not in parent_categories:
            parent_categories.append(category.category_name)
        if category.old_parent not in parent_of_parent_category:
            parent_of_parent_category.append(category.old_parent)
    
    for value in parent_of_parent_category:
        if value in parent_categories:
            parent_categories.remove(value)
    return parent_categories

def get_formatted_category(parent_categories, base_category_details):
    formatted_categories = {category: [] for category in parent_categories}

    for item in base_category_details:
        if item["old_parent"] in formatted_categories:
            category_data = {
                "name" : item["category_name"],
                "label" : item["label"],
                "slug" : item["slug"],
                "seq" : item["sequence"],
                "url" : item["url"],
                "image" : item["image"],
                "short_description" : item["short_description"]
            }
            formatted_categories[item["old_parent"]].append(category_data)
    return formatted_categories

def get_legal_section_details(footer_doc):
    legal_section_details = []
    for value in footer_doc.legal_section:
        values = {}
        values["legal_link"] = value.legal_link_text
        values["redirect_url"] = value.redirect_url
 
        legal_section_details.append(values)

    return legal_section_details