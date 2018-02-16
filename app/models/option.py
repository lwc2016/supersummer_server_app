#encoding=utf-8
from app import db
from datetime import datetime

class Option(db.Model):
	'''问题选项数据模型'''
	__tablename__ = "options";
	id = db.Column(db.Integer, primary_key = True)
	question_id = db.Column(db.Integer, nullable=False)
	content = db.Column(db.String(1000), nullable=False)
	label = db.Column(db.Enum("A", "B", "C", "D", "E"), nullable=False)
	created_time = db.Column(db.DateTime)
	is_valid = db.Column(db.Boolean, default=True)

	def __init__(self, data):
		self.content = data.get("content")
		self.label = data.get("label")
		self.question_id = data.get("question_id")
		self.created_time = datetime.now()

	def __repr__(self):
		return "<Option {0}>".format(self.id)

	@staticmethod
	def Query():
		return Option.query.filter_by(is_valid=True)