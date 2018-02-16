# encoding=utf-8
from app import app
from config import DEBUG, PORT

# 启动程序
if __name__ == "__main__":
	app.run("127.0.0.1", PORT, debug=DEBUG)