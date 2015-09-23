#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2015 .com, Inc. All Rights Reserved
#
################################################################################
"""
description:
author: liufengxu
date: 2015-09-22 16:54:50
last modified: 2015-09-23 20:32:13
version:
"""

import logging
import hashlib
from xml.etree import ElementTree
import time
from flask import Flask
from flask import request

app = Flask(__name__)

TOKEN = "biubiz"


def load_index(index_file):
    index_dict = {}
    with open(index_file) as fp:
        for line in fp:
            segs = line[:-1].split('\t')
            key = segs[0].decode('utf8')
            value = ','.join(segs[1:]).decode('utf8')
            index_dict[key] = value
    return index_dict


def responseMsg():
    postStr = request.data
    logging.debug('%s', postStr)
    if postStr:
        root = ElementTree.fromstring(postStr)
    fromUsername = root.find('FromUserName').text
    toUsername = root.find('ToUserName').text
    keyword = root.find('Content').text.strip()
    cur_time = str(int(time.time()))
    # 返回消息模板
    textTpl = ("<xml>"
               "<ToUserName><![CDATA[%s]]></ToUserName>"
               "<FromUserName><![CDATA[%s]]></FromUserName>"
               "<CreateTime>%s</CreateTime>"
               "<MsgType><![CDATA[%s]]></MsgType>"
               "<Content><![CDATA[%s]]></Content>"
               "<FuncFlag>0</FuncFlag>"
               "</xml>")
    logging.debug('%s', textTpl)
    # 初始化索引
    mem_index = load_index('./index.txt')
    if keyword:
        msgType = "text"
        contentStr = keyword
        logging.debug('%s', contentStr)
        # 从微信服务器接收到的数据是Unicode的
        if contentStr == '你好'.decode('utf8'):
            contentStr = '你好，我是小饭盒'
        elif contentStr in mem_index:
            contentStr = mem_index[contentStr]
        else:
            contentStr = '我不知道你在说神马'
        ret_xml = textTpl % (fromUsername, toUsername, cur_time,
                             msgType, contentStr)
        logging.debug('%s', ret_xml)
        return ret_xml
    else:
        return 'Input something'


def checkSignature(signature, timestamp, nonce):
    logging.debug('Token defined')
    token = TOKEN
    to_check_list = [timestamp, nonce, token]
    logging.debug('%s', to_check_list)
    to_check_list.sort()
    logging.debug('%s', to_check_list)
    checker = hashlib.sha1()
    checker.update(''.join(to_check_list))
    check_sum = checker.hexdigest()
    logging.debug('%s:%s', check_sum, signature)
    if check_sum == signature:
        logging.debug('Checking pass')
        return True
    logging.debug('Checking failed')
    return False


@app.route('/test', methods=['POST'])
def test():
    echostr = str(request.args.get('echostr', ''))
    signature = str(request.args.get('signature', ''))
    timestamp = str(request.args.get('timestamp', ''))
    nonce = str(request.args.get('nonce', ''))
    if checkSignature(signature, timestamp, nonce):
        return responseMsg()
        # 接口信息配置验证时使用这个return
        return '%s' % echostr
    else:
        return 'oops: %s' % echostr


def main():
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: "
                        "%(asctime)s: %(filename)s: %(lineno)d * "
                        "%(thread)d %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    app.run(host='101.200.198.128', port=80, debug='True')

if __name__ == '__main__':
    main()
