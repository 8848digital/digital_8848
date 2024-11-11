# Copyright (c) 2024, digital_8848 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class CaseStudy(Document):
	def validate(self):
		self.validate_display_on_home_page_checkbox()
	
	def before_save(self):
		if self.file_url:
			self.url = self.file_url + "/" + self.slug
		else:
			self.url = "/" + self.slug

        
	def validate_display_on_home_page_checkbox(self):
		if self.display_on_home_page:
			other_case_studies = frappe.get_all(
				"Case Study", filters={"name": ["!=", self.name], "display_on_home_page": 1}
			)
			if other_case_studies:
				other_case_study_names = [case_study["name"] for case_study in other_case_studies]
				frappe.throw(
					_(
						"Another Case Study ({0}) is already displayed on the home page. "
						"Please uncheck 'Display on Home Page' for that Case Study first."
					).format(", ".join(other_case_study_names))
				)
				
