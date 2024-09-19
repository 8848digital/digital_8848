import frappe
from frappe.contacts.doctype.contact.contact import Contact

class CustomContact(Contact):
    def autoname(self):
        if self.custom_full_names:
            self.name = self.custom_full_names
