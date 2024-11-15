# Copyright (c) 2024, digital_8848 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Industry(Document):
	def before_save(self):
		category = self.category
		# category_doc = frappe.get_doc("Category", category)
		# category_doc.enable_category = self.publish_on_site
		# category_doc.enable_footer = self.publish_on_site
		# category_doc.save(ignore_permissions=True)

		if self.file_url:
			self.url = self.file_url + "/" + self.slug
		elif self.slug == "" and self.file_url:
			self.url = ""
		elif self.slug == "" or self.file_url == "":
			self.url = ""
		else:
			self.url = "/" + self.slug


