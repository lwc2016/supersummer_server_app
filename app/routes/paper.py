#encoding=utf-8
from flask import request
from sqlalchemy import and_
from app import db, api, Resource
from datetime import datetime
from app.models import Paper, Question
from app.modules import error
import math
import config

class Paper_add(Resource):
	def post(self):
		form = request.form
		name = form.get("name")
		subject = form.get("subject")
		# 判断name和subject是否为空
		if not name or not subject:
			return error.error_1001()
		# 判断sucject是否合法
		if subject not in config.subjects:
			return error.error_1006()
		# 判断name是否存在
		paper_count = Paper.Query().filter_by(name=name).count()
		if paper_count:
			return error.error_1002("此考试名称已经存在")
		# 提交到数据库
		paper = Paper(form)
		try:
			db.session.add(paper)
			db.session.commit()
		except:
			return error.error_1003()
		return error.success()

class Paper_query(Resource):
	def get(self):
		return self.query()
	def post(self):
		return self.query()
	def query(self):
		pageNo = int(request.args.get("pageNo") or request.form.get("pageNo") or 1)
		pageSize = int(request.args.get("pageSize") or request.form.get("pageSize") or 10)
		# 查询数据库
		rows = Paper.Query().offset((pageNo - 1)*pageSize).limit(pageSize).all()
		count = Paper.Query().count()
		pageCount = math.ceil(count / pageSize)
		papers = []
		for r in rows:
			question_count = Question.Query().filter_by(paper_id=r.id).count()
			paper = {
				"id": r.id,
				"name": r.name,
				"question_count": question_count,
				"subject": r.subject,
				"created_time": datetime.timestamp(r.created_time)
			}
			papers.append(paper)
		return error.success({"list": papers, "page": {"total": count, "pageCount": pageCount}})

class Paper_all(Resource):
	def get(self):
		return self.query()
	def post(self):
		return self.query()
	def query(self):
		subject = request.args.get("subject") or request.form.get("subject")
		# 判断subject是否为空
		if not subject:
			return error.error_1001()
		# 判断subject值是否有效
		if subject not in config.subjects:
			return error.error_1006()
		# 查询数据库
		rows = Paper.Query().filter_by(subject=subject).all()
		papers = []
		for r in rows:
			paper = {
				"id": r.id,
				"name": r.name,
				"subject": r.subject,
				"created_time": datetime.timestamp(r.created_time)
			}
			papers.append(paper)
		return error.success(papers)

class Paper_delete(Resource):
	def post(self):
		id = request.form.get("id")
		if not id:
			return error.error_1001()
		# 查询该考试中是否有题目
		question_count = Question.Query().filter_by(paper_id=id).count()
		if question_count:
			return error.error_1008("此考试中有题目，不能被删除！")

		# 查询数据库
		paper = Paper.Query().filter_by(id=id).first()
		if paper:
			paper.is_valid = False
			db.session.add(paper)
			db.session.commit()
		return error.success()

class Paper_edit(Resource):
	def post(self):
		id = request.form.get("id")
		name = request.form.get("name")
		# 判断id和name是否为空
		if not id or not name:
			return error.error_1001()
		# 查询数据库
		paper = Paper.Query().filter_by(id=id).first()
		if paper:
			# 判断name是否重复
			name_count = Paper.Query().filter(and_(Paper.name == name, Paper.id != id)).count()
			if name_count:
				return error.error_1002("此考试名称已存在")
			# 提交到数据库
			paper.name = name
			db.session.add(paper)
			db.session.commit()
		return error.success()

class Paper_detail(Resource):
	def post(self):
		return self.query()
	def get(self):
		return self.query()
	def query(self):
		id = request.args.get("id") or request.form.get("id")
		if not id:
			return error.error_1001()
		# 查询数据库
		row = Paper.Query().filter_by(id=id).first()
		paper = {}
		if row:
			paper = {
				"id": row.id,
				"name": row.name,
				"subject": row.subject
			}

		return error.success(paper)

#添加考试接口
api.add_resource(Paper_add, "/paper/add")
#获取考试列表接口
api.add_resource(Paper_query, "/paper/list")
#按照科目获取全部考试接口
api.add_resource(Paper_all, "/paper/all")
#删除考试接口
api.add_resource(Paper_delete, "/paper/delete")
#编辑考试接口
api.add_resource(Paper_edit, "/paper/edit")
#获取试卷详情接口
api.add_resource(Paper_detail, "/paper/detail")


