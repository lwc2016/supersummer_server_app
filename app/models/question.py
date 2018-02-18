#encoding=utf-8
from app import db
from app.models import Category
from datetime import datetime

class Question(db.Model):
	'''问题数据模型'''
	__tablename__ = "questions"
	id = db.Column(db.Integer, primary_key = True)
	no = db.Column(db.String("20"))
	content = db.Column(db.String(2000), nullable=False)
	right_answer = db.Column(db.String(10), nullable=False)
	category_id = db.Column(db.Integer, nullable=False)
	answer_analyze = db.Column(db.String(2000))
	paper_id = db.Column(db.Integer)
	type = db.Column(db.Enum("single", "double"), nullable=False)
	created_time = db.Column(db.DateTime)
	is_valid = db.Column(db.Boolean, default = True)

	def __init__(self, data):
		self.no = data.get("no")
		self.content = data.get("content")
		self.right_answer = data.get("right_answer")
		self.category_id = data.get("category_id")
		self.paper_id = data.get("paper_id")
		self.answer_analyze = data.get("answer_analyze")
		answers_list = data.get("right_answer").split(",")
		length = len(answers_list)
		type = "single"
		if length > 1:
			type = "double"
		self.type = type
		self.created_time = datetime.now()

	def __repr__(self):
		return "<Question {0}>".format(self.id)

	@staticmethod
	def QueryJoinCategory():
		return Question.query.join(Category, Category.id == Question.category_id).add_entity(Category).filter(Question.is_valid==True)

	@staticmethod
	def Query():
		return Question.query.filter_by(is_valid=True)