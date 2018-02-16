#encoding=utf-8
from app import db
from datetime import datetime

class Paper(db.Model):
	'''考试数据模型'''
	__tablename__ = "papers"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), nullable=False)
	subject = db.Column(db.Enum("kuaiji", "shenji", "caiwu", "jingji", "shuifa", "fengkong"), nullable=False)
	created_time = db.Column(db.DateTime)
	is_valid = db.Column(db.Boolean, default=True)

	def __init__(self, data):
		self.name = data.get("name")
		self.subject = data.get("subject")
		self.created_time = datetime.now()

	def __repr__(self):
		return "<Paper {0}>".format(self.name)

	@staticmethod
	def Query():
		return Paper.query.filter_by(is_valid=True)