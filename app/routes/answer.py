#encoding=utf-8
from flask import request, g
from app import app, db, api, Resource
from app.models import Question, Answer, User, Category
from datetime import datetime
from app.modules import error

class Answer_commit(Resource):
	def post(self):
		form = request.form
		# 获取参数
		question_id = form.get("question_id")
		user_answer = form.get("user_answer")

		# 判断参数是否存在
		if not question_id or not user_answer:
			return error.error_1001()
		# 判断用户是否重复回答
		answer_count = Answer.Query().filter_by(user_id=g.uid, question_id=question_id).count()
		if answer_count:
			return error.error_1002("此题已经回答")

		# 查询数据库
		question = Question.Query().filter_by(id=question_id).first()
		if not question:
			return error.error_1009("题目不存在")

		is_right = user_answer == question.right_answer
		postData = {
			"question_id": question_id,
			"user_answer": user_answer,
			"user_id": g.uid,
			"is_right": is_right
		}
		answer = Answer(postData)
		db.session.add(answer)
		db.session.commit()

		result = {
			"id": answer.id,
			"is_right": is_right,
			"right_answer": question.right_answer,
			"user_answer": user_answer
		}
		return error.success(result)

class Answer_Query(Resource):
	def get(self):
		return self.query()
	def post(self):
		return self.query()
	def query(self):
		pageNo = int(request.args.get("pageNo") or request.form.get("pageNo") or 1)
		pageSize = int(request.args.get("pageSize") or request.form.get("pageSize") or 10)
		query = Answer.Query()
		rows = query.offset((pageNo - 1)*pageSize).limit(pageSize).all()
		answers = []
		for r in rows:
			user = User.Query().filter_by(id=r.user_id).first()
			question = Question.Query().filter_by(id=r.question_id).first()
			print(question.category_id)
			category = Category.Query().filter_by(id=question.category_id).first() 
			answer = {
				"id": r.id,
				"username": user.name,
				"subject": question.subject,
				"category": category.name,
				"question_id": question.id,
				"question_content": question.content,
				"is_right": r.is_right,
				"user_answer": r.user_answer
			}
			answers.append(answer)

		return error.success({"list": answers})


# 用户答题接口
api.add_resource(Answer_commit, "/answer/commit")

# 用户答题列表
api.add_resource(Answer_Query, "/answer/list")