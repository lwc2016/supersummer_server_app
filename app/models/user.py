#encoding=utf-8
from app import db, bcrypt
from datetime import datetime
import random

class User(db.Model):
	'''用户数据模型'''
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	# name值是唯一的，使用程序进行判断
	name = db.Column(db.String(20), nullable=False)
	# phone值是唯一的，使用程序进行判断
	phone = db.Column(db.String(20), nullable=False)
	real_name = db.Column(db.String(20))
	nick_name = db.Column(db.String(20))
	logo = db.Column(db.String(80))
	# openid值是唯一的，使用程序进行判断
	openid = db.Column(db.String(20))
	password = db.Column(db.String(60))
	role = db.Column(db.Enum("admin", "common"), default="common")
	created_time = db.Column(db.DateTime)
	is_valid = db.Column(db.Boolean, default=True)

	def __init__(self, data):
		self.name = data.get("name") or self.__generate_randomStr__()
		self.phone = data.get("phone")
		self.real_name = data.get("real_name")
		self.nick_name = data.get("nick_name")
		self.logo = data.get("logo")
		self.openid = data.get("openid")
		self.password = bcrypt.generate_password_hash(data.get("password")).decode("utf-8")
		self.role = data.get("role")
		self.created_time = datetime.now()

	def __repr__(self):
		return "<User {0}>".format(self.name or self.phone)

	@staticmethod
	def Query():
		return User.query.filter_by(is_valid=True)

	#生成随机的8位字符串
	def __generate_randomStr__(self):
		usableName_char = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
		username_str = []
		for i in range(8):
			username_str.append(random.choice(usableName_char))
		username = "".join(username_str)
		return username

