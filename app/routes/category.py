#encoding=utf-8
from flask import request
from app import app, db, api, Resource
from sqlalchemy import and_, or_
from app.models import Category, Question
from app.modules import error
from datetime import datetime
import math
import config

class Category_add(Resource):
	def post(self):
		form = request.form
		name = form.get("name")
		subject = form.get("subject")
		print(form)
		# 判断name和subject是否为空
		if not name or not subject:
			return error.error_1001()
		# 同一科目下分类名称不能重复
		name_count = Category.Query().filter_by(name=name, subject=subject).count()
		if name_count:
			return error.error_1002("此分类已存在")
		# 判断subject是否合法
		if subject not in config.subjects:
			return error.error_1006()

		# 提交到数据库
		category = Category(form)
		try:
			db.session.add(category)
			db.session.commit()
		except:
			return error.error_1003()
		return error.success()

class Category_query(Resource):
	def get(self):
		return self.query()
	def post(self):
		return self.query()
	def query(self):
		pageNo = int(request.args.get("pageNo") or request.form.get("pageNo") or 1)
		pageSize = int(request.args.get("pageSize") or request.form.get("pageSize") or 10)
		subject = request.args.get("subject") or request.form.get("subject") or ""
		# 查询数据库
		query = Category.Query().filter(subject and (Category.subject == subject))
		rows = query.offset((pageNo - 1)*pageSize).limit(pageSize).all()
		count = query.count()
		pageCount = math.ceil(count / pageSize)
		categories = []
		for r in rows:
			question_count = Question.Query().filter_by(category_id = r.id).count()
			category = {
				"id": r.id,
				"name": r.name,
				"subject": r.subject,
				"chapter": r.chapter,
				"question_count": question_count,
				"created_time": datetime.timestamp(r.created_time) 
			}
			categories.append(category)
		return error.success({"list": categories, "page": {"total": count, "pageCount": pageCount}})

class Category_all(Resource):
	def get(self):
		return self.query()
	def post(self):
		return self.query()
	def query(self):
		subject = request.args.get("subject") or request.form.get("subject")
		# 判断subject是否存在
		if not subject:
			return error.error_1001()
		# 判断subject值是否正确
		if subject not in config.subjects:
			return error.error_1006()
		# 查询数据库
		rows = Category.Query().filter_by(subject=subject).all()
		categories = []
		for r in rows:
			question_count = Question.Query().filter_by(category_id=r.id).count()
			category = {
				"id": r.id,
				"name": r.name,
				"subject": r.subject,
				"chapter": r.chapter,
				"question_count": question_count,
				"created_time": datetime.timestamp(r.created_time)
			}
			categories.append(category)
		return error.success(categories)

class Category_delete(Resource):
	def post(self):
		id = request.form.get("id")
		# 判断id是否为空
		if not id:
			return error.error_1001()
		# 查看该分类下是否有题目
		question_count = Question.Query().filter_by(category_id=id).count()
		if question_count:
			return error.error_1008("该分类中有题目，不能被删除");

		# 查询数据库
		category = Category.Query().filter_by(id=id).first()
		# 判断category是否存在
		if category:
			# 修改并提交到数据库
			category.is_valid = False
			db.session.add(category)
			db.session.commit()
		return error.success()

class Category_edit(Resource):
	def post(self):
		id = request.form.get("id")
		name = request.form.get("name")
		chapter = request.form.get("chapter")
		# 判断id是否为空
		if not id or not name:
			return error.error_1001()
		# 获取category
		category = Category.Query().filter_by(id=id).first()

		# 判处category是否存在
		if category:
			# 判断name是否存在
			category_count = Category.Query().filter(and_(Category.name == name, Category.id != id)).count()
			if category_count:
				return error.error_1002("此分类已存在")
			category.name = name
			if chapter:
				category.chapter = chapter
			db.session.add(category)
			db.session.commit()
		return error.success()

class Category_detail(Resource):
	def get(self):
		return self.query()
	def post(self):
		return self.query()
	def query(self):
		id = request.args.get("id") or request.form.get("id")
		# 判断id是否为空
		if not id:
			return error.error_1001()
		# 查询数据库
		row = Category.Query().filter_by(id=id).first()
		category = {}
		if row:
			category = {
				"id": row.id,
				"name": row.name,
				"subject": row.subject,
				"chapter": row.chapter,
				"created_time": datetime.timestamp(row.created_time)
			}
		return error.success(category)
class Category_byName(Resource):
	def get(self):
		return self.query()
	def post(self):
		return self.query()
	def query(self):
		name = request.args.get("name") or request.form.get("name")
		print(name)
		if not name:
			return error.error_1001()
		row = Category.Query().filter_by(name=name).first()
		category = {}
		if row:
			category = {
				"id": row.id,
				"name": row.name,
				"subject": row.subject
			}

		return error.success(category)


# 添加分类接口
api.add_resource(Category_add, "/category/add")
# 获取分类列表接口
api.add_resource(Category_query, "/category/list")
# 获取全部分类接口
api.add_resource(Category_all, "/category/all")
# 删除分类
api.add_resource(Category_delete, "/category/delete")
# 编辑分类
api.add_resource(Category_edit, "/category/edit")
# 获取分类详情接口
api.add_resource(Category_detail, "/category/detail")
# 按照名称获取分类
api.add_resource(Category_byName, "/category/byName")

