import frappe
from frappe import _


def after_insert(self, method):
	doctypes = frappe.get_all("DocType", filters={"module":"digital_8848"}, fields=["name"], pluck="name")
	if self.attached_to_doctype in doctypes:
		self.db_set("is_private", 0)