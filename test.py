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
last modified: 2015-09-22 21:15:39
version:
"""

import logging
import hashlib
from flask import Flask
from flask import request

app = Flask(__name__)

TOKEN = "biubiz"


def responseMsg():
    postStr = request.data
    if postStr:


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


@app.route('/test')
def test():
    echostr = str(request.args.get('echostr', ''))
    signature = str(request.args.get('signature', ''))
    timestamp = str(request.args.get('timestamp', ''))
    nonce = str(request.args.get('nonce', ''))
    if checkSignature(signature, timestamp, nonce):
        return '%s' % echostr
    else:
        return 'oops: %s' % echostr


def main():
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: "
                        "%(asctime)s: %(filename)s: %(lineno)d * "
                        "%(thread)d %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    app.run('101.200.198.128', port=80)

if __name__ == '__main__':
    main()
