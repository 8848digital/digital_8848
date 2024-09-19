import frappe
from frappe.contacts.doctype.contact.contact import Contact

class CustomContact(Contact):
    def autoname(self):
        if self.full_names:
            self.name = self.full_names
        # if self.company_name:
        #     self.name = self.company_name
