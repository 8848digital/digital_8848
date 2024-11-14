# Copyright (c) 2024, digital_8848 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from bs4 import BeautifulSoup
class CaseStudy(Document):
	def validate(self):
		self.validate_display_on_home_page_checkbox()
		self.validate_content()
	
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
	
	def validate_content(self):
		if (not self.client_title) and  validate_txt_editor_content(self.client_description):
			frappe.throw(_("Client Title is Mandatory"))
		if (not self.challenge_title) and (validate_txt_editor_content(self.challenge_description) or validate_txt_editor_content(self.bullet_points)):
			frappe.throw(_("Challenge Title is Mandatory"))
		if (not self.reason_title) and validate_txt_editor_content(self.reason_description):
			frappe.throw(_("Reason Title is Mandatory"))
		if (not self.solution_title) and validate_txt_editor_content(self.solution_description):
			frappe.throw(_("Solution Title is Mandatory"))
		if (not self.result_title) and validate_txt_editor_content(self.result_description):
			frappe.throw(_("Result Title is Mandatory"))
		if (not self.next_steps_title) and validate_txt_editor_content(self.next_steps_description):
			frappe.throw(_("Next Step Title is Mandatory"))
		if (not self.impact_title) and validate_txt_editor_content(self.impact_description):
			frappe.throw(_("Impact Title is Mandatory"))


def validate_txt_editor_content(txt):
	if txt:
		soup = BeautifulSoup(txt, "html.parser")
		if soup.get_text(strip=True) == '':
			descrption = None
		else:
			descrption = str(soup)
		return descrption