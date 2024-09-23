import frappe
from pypika.terms import Order

@frappe.whitelist(allow_guest=True)
def get_banner_list(**kwargs):
    try:
        title = kwargs.get("title")

        banner = frappe.qb.DocType('Banner')
        banner_detail = frappe.qb.DocType('Banner Detail')

        banner_data = frappe.qb.from_(
            banner
        ).select(
            banner_detail.idx.as_("id"),
            banner_detail.banner_image.as_("image"),
            banner_detail.title.as_("heading"),
            banner_detail.short_description.as_("text"),
            banner_detail.btn_text,
            banner_detail.btn_url
        ).left_join(
            banner_detail
        ).on(
            banner_detail.parent == banner.name
        ).where(
            (banner.title == title)
        ).orderby(
            banner_detail.idx, order=Order.asc
        ).run(as_dict=True)

        return success_response(data=banner_data)
    
    except frappe.DoesNotExistError:
        return error_response("Banner document not found.")
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}")
    
def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    return response

def error_response(err_msg):
    return {"status": "error", "error": err_msg}