#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json

import requests

config_json = {"Account": {"enable": "false",
                           "username": "用户名",
                           "password": "密码"},
               "Token": {"enable": "false",
                         "ID": "5位ID",
                         "Token": "Token"}}

post_data = {"format": "json",
             "login_token": "",
             "lang": "cn"}

APIVersion = "https://dnsapi.cn/Info.Version"
DDNSUpdate = "https://dnsapi.cn/Record.Ddns"
RecordList = "https://dnsapi.cn/Record.List"


# def detect_login():
#     if os.path.exists('/etc/pDNDPod.json'):
#         load_json(r'/etc/pDNDPod.json')
#     elif os.path.exists('./pDNDPod.json'):
#         load_json(r'./pDNDPod.json')
#     else:
#         if os.name == "posix":
#             open('/etc/pDNDPod.json', 'a', encoding="utf-8").write(json.dumps())
#         else:
#             pass

#
# def load_json():
#     pass


def main():
    if str(json.loads(requests.post(APIVersion, data=post_data).text)['status']['code']) != "1":
        print("登录失败，请检查")
        return
    record_data = {'domain': "kdajv.com",
                   "sub_domain": "@",
                   "record_type": "A"}
    record_id = str(json.loads(requests.post(RecordList, data={**record_data, **post_data}).text)['records'][0]['id'])

    ddns_data = {'domain': 'kdajv.com',
                 'sub_domain': '@',
                 'value': '2.2.2.3',
                 'record_line': '默认',
                 "record_id": record_id}
    print(requests.post(DDNSUpdate, data={**ddns_data, **post_data}).text)


if __name__ == "__main__":
    # detect_login()
    main()
