# Copyright (c) 2024, digital_8848 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MetaTags(Document):
    def before_save(self):
        if self.meta_image:
            self.open_graph_images = self.meta_image
