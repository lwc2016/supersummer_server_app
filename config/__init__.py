# encoding=utf-8
# mysql配置信息
# 导入模块
import os
from config import development, production, test
env = os.environ.get("ENV")
SQLALCHEMY_DATABASE_URI = None
DEBUG = None
PORT = None

if env == "test":
    print("<------测试环境------->")
    SQLALCHEMY_DATABASE_URI = test.SQLALCHEMY_DATABASE_URI
    DEBUG = test.DEBUG
    PORT = test.PORT
elif env == "production":
    print("<------生产环境------->")
    SQLALCHEMY_DATABASE_URI = production.SQLALCHEMY_DATABASE_URI
    DEBUG = production.DEBUG
    PORT = production.PORT
else:
    print("<------开发环境------------>")
    SQLALCHEMY_DATABASE_URI = development.SQLALCHEMY_DATABASE_URI
    DEBUG = development.DEBUG
    PORT = development.PORT

SQLALCHEMY_TRACK_MODIFICATIONS=True
# redis配置信息
redis_host="127.0.0.1"
redis_port=6379
redis_expireTime = 24 * 60 * 60

# 需要权限的路由
auth_path=[
	# "/user/list",
	# "/user/delete",
	# "/user/edit",
	# "/category/add",
	# "/category/list",
	# "/answer/add"
]

# 科目配置
subjects = ["kuaiji", "shenji", "caiwu", "jingji", "shuifa", "fengkong"]

# 章节配置
chapters = {
    "kuaiji":[
        "第一章 总论",
        "第二章 会计政策和会计估计及其变更",
        "第三章 存货",
        "第四章 固定资产",
        "第五章 无形资产",
        "第六章 投资性房地产",
        "第七章 金融资产",
        "第八章 长期股权投资与企业合并",
        "第九章 资产减值",
        "第十章 负债和所有者权益",
        "第十一章 收入、费用和利润",
        "第十二章 非货币性资产交换",
        "第十三章 债务重组",
        "第十四章 所得税",
        "第十五章 外币折算",
        "第十六章 租赁",
        "第十七章 财务报告",
        "第十八章 合并财务报表",
        "第十九章 资产负债表日后事项",
        "第二十章 每股收益",
        "第二十一章 公允价值计算"
    ],
    "shuifa":[
        "第一章 税法总论",
        "第二章 增值税法",
        "第三章 消费税法",
        "第四章 城市维护建设税法和烟叶税法",
        "第五章 关税法",
        "第六章 资源税法、城镇土地使用税和耕地占有税法",
        "第七章 房产税法、契税法和土地增值税法",
        "第八章 车辆购置税、车船税法和印花税法",
        "第九章 企业所得税",
        "第十章 个人所得税",
        "第十一章 国际税收",
        "第十二章 税收征收管理法",
        "第十三章 税务行政法制"
    ]
}