import frappe
from frappe.utils.nestedset import NestedSet


class Category(NestedSet):
    def before_save(self):
        if self.file_url and self.slug:
            self.url = self.file_url + "/" + self.slug
        elif self.file_url and not self.slug:
            self.url = self.file_url
        elif not self.file_url and self.slug:
            self.url = "/" + self.slug
        else:
            self.url = ""
