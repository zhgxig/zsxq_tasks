import datetime
import json

from celery.schedules import crontab
from celery import Celery
from kombu import Queue, Exchange
from dingding import DingDing
from stock import Stock
from deal_data import Deal
from utils import str_to_num

import configparser

config = configparser.ConfigParser()
config.read_file(open('config.ini'))

app = Celery("tasks")
app.config_from_object("setting")

deal = Deal()
stock = Stock()
dingding = DingDing()

# 定时任务配置
app.conf.update(
    # # 默认交换机名字为tasks
    # CELERY_DEFAULT_EXCHANGE = 'tasks',
    # 交换类型是topic
    CELERY_DEFAULT_EXCHANGE_TYPE='topic',
    # 默认的路由键是task.default
    CELERY_DEFAULT_ROUTING_KEY='default',
    CELERY_DEFAULT_EXCHANGE='default',
    CELERY_DEFAULT_QUEUE='default',
    CELERY_QUEUES=(
        Queue('default', Exchange='default', routing_key='default'),
        Queue('normal', Exchange='normal', routing_key='normal.#'),
    ),

    CELERY_ROUTES={
        "tasks.warning_gupiao": {"queue": "normal", "routing_key": "normal.warning_gupiao"},

    },

    CELERYBEAT_SCHEDULE={
        "warning_gupiao": {
            "task": "tasks.warning_gupiao",
            "schedule": crontab(minute="*/120", hour="1-7")
        }
    })


@app.task()
def warning_gupiao(now=None):
    """达到要求进行通知"""
    gupiao_list = config.get("gupiao_list", "one")
    gupiao_list = json.loads(gupiao_list)

    res = stock.query_gupiao(gupiao_list)

    # dataframe to dict
    gupiao_msg = json.loads(res.to_json(orient='records'))

    # compare
    for each_gupiao in gupiao_msg:
        each_gupiao_name = each_gupiao.get("name", "")
        each_gupiao_price = str_to_num(each_gupiao.get("price", 0))
        low = str_to_num(config.get(each_gupiao_name, "low"))
        high = str_to_num(config.get(each_gupiao_name, "high"))
        if low > each_gupiao_price:
            string = """股票名字: {name}\t编码: {code}\t价格到了{price}, 低于设定最低值{low}需要加仓""".format(**each_gupiao, low=low)
            send_to_dingding.delay(string)
        elif high < each_gupiao_price:
            string = """股票名字: {name}\t编码: {code}\t价格到了{price}, 高于设定最高值{high}需要减仓""".format(**each_gupiao, high=high)
            send_to_dingding.delay(string)


@app.task()
def send_to_dingding(dealed_data):
    # 发送数据
    res = dingding.send_text(dealed_data)
    return res


if __name__ == "__main__":
    res = warning_gupiao()
    print(res)
