def success_response(data=None, id=None):
	return {"msg": "success", "data": data or {"id": id, "name": id} if id else data}


def error_response(err_msg):
	return {"msg": "error", "error": err_msg}

