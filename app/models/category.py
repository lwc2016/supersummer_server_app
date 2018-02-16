#encoding=utf-8
from app import db
from datetime import datetime
class Category(db.Model):
	'''分类数据模型'''
	__tablename__ = "categories"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	subject = db.Column(db.Enum("kuaiji", "shenji", "caiwu", "jingji", "shuifa", "fengkong"), nullable=False)
	chapter = db.Column(db.String(30))
	created_time = db.Column(db.DateTime)
	is_valid = db.Column(db.Boolean, default=True)

	def __init__(self, data):
		self.name = data.get("name")
		self.subject = data.get("subject")
		self.chapter = db.get("chapter")
		self.created_time = datetime.now()

	def __repr__(self):
		return "<Category {0}>".format(self.name)

	@staticmethod
	def Query():
		return Category.query.filter_by(is_valid=True)