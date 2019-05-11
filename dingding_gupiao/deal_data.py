class Deal(object):
    def __init__(self):
        pass

    def df_to_list(self, gupiao_list, res) -> list:
        """
        将实时数据df转成list
        :param gupiao_list: ["000001", "000002"]
        :param res : 股票df数据
        :return:
        """
        all_gupiao_data = []
        n = len(gupiao_list)
        for idx in range(n):
            each_dict = {}
            for k, v in res.to_dict().items():
                value = v.get(idx, "")
                if value:
                    each_dict[k] = value
            if each_dict:
                all_gupiao_data.append(each_dict)
        return all_gupiao_data

    def to_text(self, data) -> str:
        """
        将实时股票数据转成字符
        :param data: [{"code": "", "price": ""}]
        :return:
        """
        string = ""
        for idx, each in enumerate(data):
            each_string = """\t股票名: {name}\n\t编码: {code}\n\t当前价格: {price}元\n\t成交量: {volume}\n\t成交金额: {amount}元\n\t时间: {time}\n\n""".format(idx + 1, **each)
            string += each_string
        string = string.lstrip("\n")
        return string
