# Copyright (c) 2024, digital_8848 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Insights(Document):
	def before_save(self):
		if self.file_url:
			self.url = self.file_url + "/" + self.slug
		else:
			self.url = "/" + self.slug

