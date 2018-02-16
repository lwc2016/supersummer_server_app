#encoding=utf-8
from flask import request
from app import app, api, Resource
from config import chapters
from app.modules import error;

class Chapter_list(Resource):
    def get(self):
        return self.query()
    def post(self):
        return self.query()
    def query(self):
        subject = request.args.get("subject") or request.form.get("subject")
        result = chapters
        if subject:
            result = chapters[subject]

        # 返回结果
        return error.success(result)

api.add_resource(Chapter_list, "/chapter/list")