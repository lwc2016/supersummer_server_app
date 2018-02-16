# encoding=utf-8
from flask import request, g
from app import db, api, Resource
from sqlalchemy import and_, or_, func, exists, not_
from datetime import datetime
from app.models import Question, Option, Category, Answer
from app.modules import error
from functools import reduce
import json
import math

class Question_add(Resource):
	def post(self):
		form = request.form
		print(form)
		content = form.get("content")
		category_id = form.get("category_id")
		right_answer = form.get("right_answer")
		options = form.get("options")
		# 判断参数是否为空
		if not content or not right_answer or not category_id:
			return error.error_1001()

		# 判断right_answer是否合法
		answers_lst = right_answer.split(",")
		for answer in answers_lst:
			if answer not in ["A", "B", "C", "D", "E"]:
				return error.error_1007()

		# 判断题目是否重复
		content_count = Question.Query().filter_by(content=content).count()
		if content_count:
			return error.error_1002("题目不能重重")

		# 将题目添加到到数据库
		question = Question(form)
		db.session.add(question)
		db.session.flush()
		# 获取题目的临时id
		question_id = question.id

		# 解析选项
		options = json.loads(options)
		for r in options:
			r["question_id"] = question_id
			# 判断label是否合法
			if not r.get("label") or r.get("label") not in ["A", "B", "C", "D", "E"]:
				return error.error_1007()
			# 同一题目A,B,C,D,E出现两次
			label_count = Option.Query().filter_by(question_id=question_id, label=r["label"]).count()
			print("label_count ", label_count)
			if label_count:
				return error.error_1002(r["label"] + "重复")
			option = Option(r)
			db.session.add(option)
		db.session.commit()
		return error.success()


class Question_query(Resource):
	def get(self):
		return self.query()
	def post(self):
		return self.query()
	def query(self):
		pageNo = int(request.args.get("pageNo") or request.form.get("pageNo") or 1)
		pageSize = int(request.args.get("pageSize") or request.form.get("pageSize") or 10) 
		subject = request.args.get("subject") or request.form.get("subject")
		print(subject)
		# 获取答案和分类
		query = Question.QueryJoinCategory()
		if subject:
			query = query.filter(Category.subject==subject)
		rows = query.offset((pageNo - 1)*pageSize).limit(pageSize).all()
		count = query.count()
		pageCount = math.ceil(count / pageSize)
		questions = []
		for r in rows:
			# 查询选项
			ops = Option.Query().filter_by(question_id=r.Question.id).all()
			print(ops)
			options = []
			for op in ops:
				option = {
					"id": op.id,
					"label": op.label,
					"content": op.content,
					"created_time": datetime.timestamp(op.created_time)
				}
				options.append(option)
			# 整理question数据
			question = {
				"id": r.Question.id,
				"content": r.Question.content,
				"type": r.Question.type,
				"category_id": r.Question.category_id,
				"category_name": r.Category.name,
				"subject": r.Category.subject,
				"options": options,
				"created_time": datetime.timestamp(r.Question.created_time)
			}
			questions.append(question)
		return error.success({"list": questions, "page": {"total": count, "pageCount": pageCount}})



class Question_delete(Resource):
	def post(self):
		id = request.form.get("id")
		if not id:
		 	return error.error_1001()
		# 查询数据库
		question = Question.Query().filter_by(id=id).first()
		if question:
			question.is_valid = False
			db.session.add(question)
			db.session.commit()

		# 返回结果
		return error.success()

class Question_detail(Resource):
	def post(self):
		return self.query()
	def get(self):
		return self.query()
	def query(self):
		id = request.args.get("id") or request.form.get("id")
		#判断参数是否存在
		if not id:
			return error.error_1001()

		row = Question.QueryJoinCategory().filter(Question.id==id).first()
		question = {}
		if row:
			opts = Option.Query().filter_by(question_id=row.Question.id).all()
			options = []
			for op in opts:
				option = {
					"id": op.id,
					"label": op.label,
					"content": op.content,
					"created_time": datetime.timestamp(op.created_time)
				}
				options.append(option)
			question = {
				"id": row.Question.id,
				"content": row.Question.content,
				"type": row.Question.type,
				"category_id": row.Question.category_id,
				"category_name": row.Category.name,
				"subject": row.Category.subject,
				"right_answer": row.Question.right_answer,
				"answer_analyze": row.Question.answer_analyze,
				"options": options,
				"created_time": datetime.timestamp(row.Question.created_time)
			}

		return error.success(question)

class Question_edit(Resource):
	def post(self):
		form = request.form
		# 获取参数
		id = form.get("id")
		content = form.get("content")
		category_id = form.get("category_id")
		right_answer = form.get("right_answer")
		options = form.get("options")
		answer_analyze = form.get("answer_analyze")
		print(answer_analyze)
		#判断参数是否为空
		if not id:
			return error.error_1001()
		# 查询数据库
		question = Question.Query().filter_by(id=id).first()
		# 判断需要修改的数据
		# 修改题目标题
		if content:
			question.content = content
		# 修改题目分类
		if category_id:
			question.category_id = category_id
		# 修改正确答案
		if right_answer:
			question.right_answer = right_answer
			answers_lst = right_answer.split(",")
			length = len(answers_lst)
			type = "single"
			if length > 1:
				type = "double"
			question.type = type
		# 修改题目选项
		if options:
			options = json.loads(options)
			for op in options:
				option = Option.Query().filter_by(id=op.get("id")).first()
				option.content = op.get("content")
				option.label = op.get("label")
				db.session.add(option)
		# 修改题目答案解析
		if answer_analyze:
			question.answer_analyze = answer_analyze

		# 提交到数据库
		db.session.add(question)
		db.session.commit()
		return error.success()

class Question_random(Resource):
	def get(self):
		return self.query()
	def post(self):
		return self.query()
	def query(self):
		subject = request.args.get("subject") or request.form.get("subject")
		# 判断是否选择学科
		if not subject:
			return error.error_1001()
		

		# 查询用户已答题
		user_id = g.uid
		user_answered = Answer.Query().filter_by(user_id=user_id).all()
		user_answered_ids = []
		for r in user_answered:
			user_answered_ids.append(r.question_id)
		print(user_answered_ids)
		user_answered_ids_t = tuple(user_answered_ids)

		# 查出没有答过的题目
		res = Question.QueryJoinCategory().filter(Category.subject == subject).filter(not_(Question.id.in_(user_answered_ids_t))).order_by(func.rand()).first()
		count = Question.QueryJoinCategory().filter(Category.subject == subject).filter(not_(Question.id.in_(user_answered_ids_t))).count()
		print(count)

		question = {}
		if res:
			# 获取题目选项
			rows = Option.Query().filter_by(question_id=res.Question.id).all()
			options = []
			for r in rows:
				option = {
					"id": r.id,
					"label": r.label,
					"content": r.content
				}
				options.append(option)

			question = {
				"id": res.Question.id,
				"type": res.Question.type,
				"content": res.Question.content,
				"category_name": res.Category.name,
				"category_id": res.Category.id,
				"options": options
			}

		return error.success(question)


# 添加题目接口
api.add_resource(Question_add, "/question/add")
# 添加获取问题列表接口
api.add_resource(Question_query, "/question/list")
# 删除题目接口
api.add_resource(Question_delete, "/question/delete")
# 获取详情接口 ------------> 用于后台获取详情
api.add_resource(Question_detail, "/question/detail")
# 编辑问题接口
api.add_resource(Question_edit, "/question/edit")
# 随机获取问题
api.add_resource(Question_random, "/question/random");


