import frappe

@frappe.whitelist(allow_guest=True)
def get_header(**kwargs):
	try:
		category = frappe.qb.DocType("Category")
		query = (
			frappe.qb.from_(category)
			.select(category.name)
		).run(as_dict=True)

		if not query:
			return {{"msg": "error", "error": "No category found for the project"}}

		parent_categories_list = frappe.get_list(
			"Category",
			filters={
				"is_group": 1,
				"enable_category": 1,
				"old_parent": ["=", ""],
				"parent_category": ["=", ""],
			},
			pluck="name",
		)

		parent_categories = frappe.get_all(
			"Category",
			filters={
				"is_group": 1,
				"enable_category": 1,
				"name": ["in", parent_categories_list],
			},
			fields=[
				"name",
				"label",
				"url",
				"sequence",
				"slug",
				"image",
				"short_description",
			],
			order_by="sequence",
		)

		navbar_data = [build_category_tree(category) for category in parent_categories]

		return {"msg": "success", "data": navbar_data}
	except Exception as e:
		frappe.logger("Category").exception(e)
		return error_response(str(e))


def build_category_tree(category):
	category_item = {
		"name": category["name"],
		"label": category["label"],
		"url": category["url"],
		"seq": category["sequence"],
		"slug": category["slug"],
		"image": category["image"],
		"short_description": category["short_description"],
		"values": [],
	}

	sub_categories = frappe.get_all(
		"Category",
		filters={"parent_category": category["name"], "enable_category": 1},
		fields=[
			"name",
			"label",
			"url",
			"sequence",
			"slug",
			"image",
			"short_description",
		],
		order_by="sequence",
	)

	for sub_category in sub_categories:
		sub_category_item = build_category_tree(sub_category)
		category_item["values"].append(sub_category_item)

	return category_item


def success_response(data=None, id=None):
    return {"msg": "success", "data": data or {"id": id, "name": id} if id else data}


def error_response(err_msg):
	return {"msg": "error", "error": err_msg}

