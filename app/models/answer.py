#encoding=utf-8
from app import db
from datetime import datetime

class Answer(db.Model):
	__tablename__ = "answers"
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, nullable=False)
	question_id = db.Column(db.Integer, nullable=False)
	user_answer = db.Column(db.String(10), nullable=False)
	is_right = db.Column(db.Boolean, nullable=False)
	effect = db.Column(db.Enum("1","2","3"))
	# 1:完全不懂 2:模棱两可 3:熟练掌握
	created_time = db.Column(db.DateTime)
	is_valid = db.Column(db.Boolean, default=True)

	def __init__(self, data):
		self.user_id = data.get("user_id")
		self.question_id = data.get("question_id")
		self.user_answer = data.get("user_answer")
		self.is_right = data.get("is_right")
		self.created_time = datetime.now()

	def __repr__(self):
		return "<Answer {0}>".format(self.question_id)

	@staticmethod
	def Query():
		return Answer.query.filter_by(is_valid=True)
 