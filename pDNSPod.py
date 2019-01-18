# !/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import os

import requests

config_name = "./pDNSPod.json"

config_json = {"Login": {"Account": {"enable": False, "username": "用户名", "password": "密码"},
                         "Token": {"enable": False, "ID": "5位ID", "Token": "Token"}}, "Domains": [
    {"enable": False, "domain": "域名", "sub_domain": "子域名，如是一级域名填@即可", "record_type": "记录类型，默认为A",
     "record_line": "域名线路，默认或电信或联通等等，中文即可", "value": "记录内容,如需自动获取请输入auto"}]}

post_data = {"format": "json",
             "lang": "cn"}
domain_data = []

APIVersion = "https://dnsapi.cn/Info.Version"
DDNSUpdate = "https://dnsapi.cn/Record.Ddns"
RecordList = "https://dnsapi.cn/Record.List"


def check_login():
    ret = json.loads(requests.post(APIVersion, data=post_data).text)
    if ret['status']['code'] == '1':
        return True, ret['status']['message']
    else:
        return False, ret['status']['message']


def get_ID():
    global domain_data
    for tmp in domain_data:
        ret = json.loads(requests.post(RecordList, data={**post_data, **tmp, 'length': '1'}).text, encoding='utf-8')
        tmp['record_id'] = ret['records'][0]['id']
        tmp['ovalue'] = ret['records'][0]['value']
        pass


def update_ddns():
    for tmp in domain_data:
        ret = json.loads(requests.post(DDNSUpdate, data={**tmp, **post_data}).text)
        if ret['status']['code'] == "1":
            print("更新成功")
            print("IP: %s" % ret['record']['value'])
            exit(0)
        else:
            print("更新失败")
            print(ret['status']['message'])
            exit(1)


def process_value():
    ip = requests.get("https://api.ip.sb/ip").text.strip()
    for tmp in domain_data:
        if tmp['value'] == "auto":
            tmp['value'] = ip
    for tmp in domain_data:
        if tmp['value'] == tmp['ovalue']:
            print("%s%s 记录未发生变化忽略" % (tmp['sub_domain'] is not "@" and tmp['sub_domain'] + "." or "", tmp['domain']))
            domain_data.remove(tmp)
        pass


def main():
    # Login
    flg, msg = check_login()
    if not flg:
        print("!!! 登录失败")
        print(msg)
        exit(1)
    print("登录成功，服务版本 %s " % msg)
    # Record ID
    get_ID()
    print('记录获取成功')
    print("共 %s 个数据" % len(domain_data))
    # Process Value
    process_value()
    # Update DDNS
    update_ddns()
    print("更新成功")


def detect_config():
    global config_json
    if not os.path.exists(config_name):
        print("没有检测到配置文件")
        try:
            json.dump(config_json, open(config_name, "w+", encoding="utf-8"), ensure_ascii=False, indent=4)
        except Exception as e:
            print("在当前目录创建配置文件失败")
            print("请检查当前目录的写入权限")
            print(e)
            exit(1)
        print("已写入默认配置文件，请加以修改")
    else:
        print("检测到配置文件，正在读取")
        try:
            read_config()
        except Exception as e:
            print("出现错误")
            print("可能配置文件出现问题")
            print(e)
            exit(1)
        print("配置读取完成")


def read_config():
    global config_json
    config_json = json.load(open(config_name, encoding='utf-8'))
    if config_json['Login']['Token']['enable']:
        print("使用 Token 进行验证")
        post_data['login_token'] = \
            config_json['Login']['Token']['ID'] + "," + config_json['Login']['Token']['Token']
    elif config_json['Login']['Account']['enable']:
        print("使用 账号密码 进行验证")
        post_data['login_email'] = config_json['Login']['Account']['username']
        post_data['login_password'] = config_json['Login']['Account']['password']
    else:
        print("请选择一种认证方式")
        exit(1)
    domains = config_json['Domains']
    if len(domains) == 0:
        print("请至少填写一个域名")
        exit(1)
    print("共检测到 %r 个域名" % len(domains))
    for tmp in domains:
        if not tmp['enable']:
            continue
        del tmp['enable']
        domain_data.append(tmp)
    print("共 %r 个启用域名" % len(domain_data))
    if len(domain_data) == 0:
        print("请至少启用一个域名")
        exit(1)
    pass


if __name__ == "__main__":
    detect_config()
    main()
