#encoding=utf-8
from flask import request, jsonify, g
from app import app, redisClient
import config
from app.modules import error

#关系升级
@app.before_request
def before_request():
	# 获取token和uid
	token = request.headers.get("token")
	uid = request.headers.get("uid")
	# 更新token
	if token:
		redisClient.expire(token, config.redis_expireTime)
	# 判断路由是否需要权限验证
	#if request.path in config.auth_path:
	print(request.path)
	if request.path != "/user/login" and request.path != "/user/register":
		print("------ok-----")
		# 判断token是否存在
		if not token:
			return jsonify(error.error_1005())
		token_result = redisClient.get(token)
		# 判断缓存中是否有token
		if not token_result:
			return jsonify(error.error_1005())
		# 获取缓存中id
		id = bytes.decode(token_result)
		# 判断id和uid是否相等
		if id != uid:
			return jsonify(error.error_1005())

	g.uid = uid
	
