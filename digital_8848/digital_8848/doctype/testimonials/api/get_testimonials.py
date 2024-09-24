import frappe
from pypika.terms import Order

@frappe.whitelist(allow_guest=True)
def get_testimonials(**kwargs):
    try:
        testimonial = frappe.qb.DocType('Testimonials')

        testimonial_detail = frappe.qb.from_(
            testimonial
        ).select(
            testimonial.sequence,
            testimonial.full_name.as_("name"),
            testimonial.designation.as_("role"),
            testimonial.company_name.as_("company"),
            testimonial.company_logo.as_("company_logo_image"),
            testimonial.quote,
            testimonial.quote_icon
        ).orderby(
            testimonial.sequence, order=Order.asc
        ).run(as_dict=True)

        testimonial_header = frappe.get_doc("Testimonial Heading")
        testimonial_data = {
            "section_title" : testimonial_header.heading,
            "values" : testimonial_detail
        }

        return success_response(data=testimonial_data)

    except frappe.DoesNotExistError:
        return error_response("Testimonial document not found.")
    except Exception as e:
        return error_response(f"An error occurred: {str(e)}")
    
def success_response(data=None, id=None):
    response = {"status": "success"}
    response["data"] = data
    return response

def error_response(err_msg):
    return {"status": "error", "error": err_msg}