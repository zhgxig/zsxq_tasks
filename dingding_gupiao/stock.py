import tushare as ts


class Stock(object):
    def __init__(self):
        pass

    def query_gupiao(self, gupiao_list=None):
        """
        查询股票单日实时数据(main price)
        :param gupiao:
        :return:
        """
        df = ts.get_realtime_quotes(gupiao_list)  # Single stock symbol
        res = df[['code', 'name', 'price', 'bid', 'ask', 'volume', 'amount', 'time']]
        return res

    def the_history_the_day(self, gupiao_code=None):
        """
        当日历史分笔
        :param gupiao_code:
        :return:
        """
        df = ts.get_today_ticks(gupiao_code)
        res = df.head(10)
        return res

    def market_index(self):
        """
        获取大盘指数实时行情列表，以表格的形式展示大盘指数实时行情
        :return:
        """
        df = ts.get_index()
        df = df[["code", "name", "change", "preclose", "close"]]
        return df

    def history_data(self, gupiao_code, date):
        """
        获取历史数据
        :param gupiao_code:
        :param date:
        :return:
        """
        df = ts.get_tick_data(gupiao_code, date=date, src='tt')
        return df

