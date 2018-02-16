#encoding=utf-8
def success(result=""):
	return {"code": 0, "result": result}
def error_1001():
	'''1001错误表示：缺少必要参数'''
	return {"code": 1001, "errorMsg": "缺少必要参数"}

def error_1002(errorMsg):
	'''1002错误表示：数据已存在'''
	return {"code": 1002, "errorMsg": errorMsg}

def error_1003():
	'''1003错误表示：数据库错误'''
	return {"code": 1003, "errorMsg": "数据库错误"}

def error_1004():
	'''1004错误表示：用户名或密码错误'''
	return {"code": 1004, "errorMsg": "用户名或密码错误"}

def error_1005():
	'''1005错误表示：用户未登录'''
	return {"code": 1005, "errorMsg": "请重新登录"}

def error_1006():
	'''1006错误表示：科目错误'''
	return {"code": 1006, "errorMsg": "科目错误"}

def error_1007():
	return {"code": 1007, "errorMsg": "参数错误"}

def error_1008(errorMsg):
	return {"code": 1008, "errorMsg": errorMsg}

def error_1009(errorMsg):
	'''数据不存在'''
	return {"code": 1009, "errorMsg": errorMsg}