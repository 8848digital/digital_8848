# Copyright (c) 2024, digital_8848 and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.nestedset import NestedSet


class Category(NestedSet):
	def before_save(self):
		if self.file_url:
			self.url = self.file_url + "/" + self.slug
		else:
			self.url = "/" + self.slug
