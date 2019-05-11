import datetime
import json

from dingding import DingDing
from stock import Stock
from deal_data import Deal
import configparser
config = configparser.ConfigParser()
config.read_file(open('config.ini'))


def real_time_data_acquisition():
    # 获取单日股票情况
    stock = Stock()
    gupiao_list = config.get("gupiao_list", "one")
    gupiao_list = json.loads(gupiao_list)
    res = stock.query_gupiao(gupiao_list)

    # 处理数据
    deal = Deal()
    all_gupiao_data = deal.df_to_list(gupiao_list, res)
    dealed_data = Deal().to_text(data=all_gupiao_data)
    print(dealed_data)

    # 发送数据
    dingding = DingDing()
    res = dingding.send_text(dealed_data)
    print(res)
    return res


def get_the_history_the_day():
    stock = Stock()
    gupeiao_code = config.get("single_gupiao", "涪陵榨菜")
    res = stock.the_history_the_day(gupeiao_code)
    return res


def get_market_index():
    stock = Stock()
    res = stock.market_index()
    return res


def get_history_data(now=None):
    stock = Stock()
    gupiao = config.get("single_gupiao", "涪陵榨菜")
    res = None
    if now is None:
        now = datetime.datetime.now()
    while res is None:
        date = datetime.datetime(year=now.year, month=now.month, day=now.day).strftime("%Y-%m-%d")
        res = stock.history_data(gupiao_code=gupiao, date=date)
        now = now - datetime.timedelta(days=1)
    return res


if __name__ == "__main__":
    # res = real_time_data_acquisition()
    # res = get_the_history_the_day()
    # res = get_market_index()
    res = get_history_data()
    res_dict = json.loads(res.to_json(orient='records'))
    from pprint import pprint

    pprint(res_dict)
    # print(res)
