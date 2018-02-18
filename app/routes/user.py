#encoding=utf-8
from flask import request, g
from sqlalchemy import or_, and_
from app import app, api, Resource, db, bcrypt, redisClient
from app.models import User, Answer
import hashlib
import math
from time import time
from datetime import datetime
from app.modules import error
import config

class User_add(Resource):
	def post(self):
		form = request.form
		name = form.get("name")
		phone = form.get("phone")
		print(form)
		print(request.get_data())
		print(type(request.get_data()))
		password = form.get("password")
		openid = form.get("openid")
		#phone,password不可以为空,username可以为空
		if not phone or (not password):
			return error.error_1001()

		# 判断phone手机号是否存在
		phone_count = User.Query().filter_by(phone=phone).count()
		if phone_count:
			return error.error_1002("此手机号已存在")

		# 判断name用户名是否存在
		name_count = User.Query().filter_by(name=name).count()
		if name_count:
			return error.error_1002("此用户已存在")

		# 判断openid是否存在
		if openid:
			openid_count = User.Query().filter_by(openid=openid).count()
			if openid_count:
				return error.error_1002("此微信号已存在")

		# 提交数据到数据库
		user = User(form)
		try:
			db.session.add(user)
			db.session.commit()
		except:
			return error.error_1003()
		return error.success()

class User_login(Resource):
	def post(self):
		print(request.headers)
		form = request.form
		username = form.get("username")
		password = form.get("password")
		print(form)
		print(request.get_data())
		#username 和 password不能为空
		if not username or not password:
			return error.error_1001()
		user = User.Query().filter(or_(User.name==username, User.phone==username)).first()
		#判断user是否存在
		if not user:
			return error.error_1004()
		#判断密码是否正确
		if not bcrypt.check_password_hash(user.password, password):
			return error.error_1004()
		#获取uid
		uid = user.id
		#生成token
		token_str = "{0}{1}{2}".format(user.name, uid, time()).encode("utf-8")
		token = hashlib.sha1(token_str).hexdigest()
		redisClient.set(token, uid)
		redisClient.expire(token, config.redis_expireTime)
		return error.success({"token": token, "uid": uid})

class User_query(Resource):
	def get(self):
		return self.query()
	def post(self):
		return self.query()
	def query(self):
		pageNo = int(request.args.get("pageNo") or request.form.get("pageNo") or 1)
		pageSize = int(request.args.get("pageSize") or request.form.get("pageSize") or 10)
		rows = User.Query().offset((pageNo - 1)*pageSize).limit(pageSize).all()
		count = User.Query().count()
		pageCount = math.ceil(count / pageSize)
		users = []
		for r in rows:
			user = {
				"id": r.id,
				"name": r.name,
				"phone": r.phone,
				"real_name": r.real_name,
				"nick_name": r.nick_name,
				"openid": r.openid,
				"role": r.role,
				"logo": r.logo,
				"created_time": datetime.timestamp(r.created_time) 
			}
			users.append(user)
		return error.success({"list": users, "page":{"total": count, "pageCount": pageCount}})

class User_delete(Resource):
	def post(self):
		id = request.form.get("id")
		if not id:
			return error.error_1001()
		user = User.Query().filter_by(id=id).first()
		# 判断user是否存在
		if user:
			user.is_valid = False
			db.session.add(user)
			db.session.commit()
		return error.success()

class User_edit(Resource):
	def post(self):
		form = request.form
		id = form.get("id")
		if not id:
			return error.error_1001()
		user = User.Query().filter_by(id=id).first()
		# 可以修改的信息：real_name, password, phone
		real_name = form.get("real_name")
		password = form.get("password")
		phone = form.get("phone")
		# 判断real_name是否存在
		if real_name:
			user.real_name = real_name
		# 判断password是否存在
		if password:
			user.password = bcrypt.generate_password_hash(password).decode("utf-8")
		# 判断phone是否存在
		if phone:
			phone_count = User.Query().filter(and_(User.phone == phone, User.id != id)).count()
			if phone_count:
				return error.error_1002("此手机号已存在")
			user.phone = phone

		# 提交到数据库
		db.session.add(user)
		try:
			db.session.commit()
		except:
			return error.error_1003()
		return error.success()

class User_info(Resource):
	def post(self):
		return self.query()
	def get(self):
		return self.query()
	def query(self):
		id = g.uid
		row = User.Query().filter_by(id=id).first()

		has_answered = Answer.Query().filter_by(user_id=g.uid).count()
		has_incorrect = Answer.Query().filter_by(user_id=g.uid, is_right=False).count()
		user = {
			"id": row.id,
			"name": row.name,
			"phone": row.phone,
			"has_answered": has_answered,
			"has_incorrect": has_incorrect
		}
		return error.success(user)


# 用户注册接口
api.add_resource(User_add, "/user/register")
# 用户登录接口
api.add_resource(User_login, "/user/login")
# 获取用户列表接口
api.add_resource(User_query, "/user/list")
# 删除用户接口
api.add_resource(User_delete, "/user/delete")
# 修改用户信息接口
api.add_resource(User_edit, "/user/edit")
# 获取用户信息
api.add_resource(User_info, "/user/info")


