import frappe
from frappe.contacts.doctype.contact.contact import Contact

class CustomContact(Contact):
    def autoname(self):
        if self.email_ids:
            self.name = self.email_ids[0].email_id