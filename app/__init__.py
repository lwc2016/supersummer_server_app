# encoding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_bcrypt import Bcrypt
import redis
import config


app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
api = Api(app)
bcrypt = Bcrypt(app)
redisClient = redis.StrictRedis(host=config.redis_host, port=config.redis_port)

from app import routes, models, modules

# 创建数据表
db.create_all()