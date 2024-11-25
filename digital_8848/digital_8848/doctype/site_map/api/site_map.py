import frappe
from frappe.query_builder import Field
from datetime import datetime

@frappe.whitelist(allow_guest=True)
def get_site_map(**kwargs):
    # Fetch the list of doctypes from the 'Website URL Settings' doctype
    try:
        settings = frappe.get_doc("Website URL Settings")
        doctypes = [row.document_type for row in settings.doctypes]
    except Exception as e:
        frappe.log_error(f"Error fetching 'Website URL Settings': {str(e)}", "Get Site Map Error")
        return {"status": "error", "message": "Failed to fetch Website URL Settings."}

    # Initialize the site map data list
    site_map_data = []

    # Function to fetch and process results for a doctype
    def process_doctype(doctype):
        try:
            # Dynamically fetch fields for the doctype
            meta = frappe.get_meta(doctype)
            fields = [Field(field.fieldname) for field in meta.fields if field.fieldname in ["title", "url", "change_frequency", "priority"]]
            fields.append(Field("modified"))

            if not fields:
                frappe.log_error(f"No matching fields found for {doctype}", "Get Site Map Warning")
                return []

            # Use Frappe's query builder to fetch data dynamically
            table = frappe.qb.DocType(doctype)
            query = frappe.qb.from_(table).select(*fields)
            results = query.run(as_dict=True)

            # Format the 'modified' field to dd-mm-yyyy and add doctype to each result
            for result in results:
                result["doctype"] = doctype
                if result.get("modified"):
                    result["modified"] = result["modified"].strftime("%d-%m-%Y")

            return results
        except Exception as e:
            # Log errors for specific doctype processing
            frappe.log_error(f"Error fetching data from {doctype}: {str(e)}", "Get Site Map Error")
            return []

    # Process each doctype and aggregate the results
    for doctype in doctypes:
        site_map_data.extend(process_doctype(doctype))

    # Prepare the response
    return {
        "status": "success",
        "data": site_map_data
    }
