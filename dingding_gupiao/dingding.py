import requests
import logging
import configparser

config = configparser.ConfigParser()
config.read_file(open('config.ini'))


class DingDing(object):
    def __init__(self, base_url=None, token=None):
        """
        初始化数据
        :param base_url: 请求地址
        :param token: 请求秘钥
        """
        self.people_list = []
        self.call_all = True
        self.base_url = config.get("dingding", "request_url")
        self.token = config.get("dingding", "token")

    def call_list(self, people_list=None):
        """
        广播列表
        :param people_list: 需要广播人
        :return:
        """
        if not people_list:
            self.people_list = []
        else:
            self.people_list = people_list
        return self.people_list

    def call_all_status(self, call_status=None):
        """
        广播状态
        :param call_status: 是否广播所有人
        :return:
        """
        if not call_status:
            self.call_all = False
        else:
            self.call_all = True
        return self.call_all

    def send_text(self, text=None, people_list=None, call_status=True):
        """
        发送广播
        :param text:
        :param people_list:
        :param call_status:
        :return:
        """
        people_list = self.call_list(people_list)
        call_status = self.call_all_status(call_status)

        data = {
            "msgtype": "text",
            "text": {
                "content": text
            },
            "at": {
                "atMobiles": people_list,
                "isAtAll": call_status
            }

        }

        try:
            r = requests.post(
                url=self.base_url,
                json=data,
                params={
                    "access_token": self.token
                },
                headers={
                    "Content-Type": "application/json"
                }
            )

            resp = r.json()
        except Exception as e:
            logging.error("request dingding error!", exc_info=True)
            return {"code": -1, "msg": e, "data": {}}
        else:
            return {"code": 0, "msg": resp, "data": {}}
