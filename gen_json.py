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
date: 2015-07-26 20:57:51
last modified: 2015-09-26 23:56:31
version:
"""

import logging
import random
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
mem_table = {}
with open('./0924.txt') as fp:
    for line in fp:
        segs = line[:-1].split('\t')
        mem_table[segs[0]] = segs


def pack_json(data_dict, message='error'):
    logging.debug('%s', data_dict)
    if not data_dict:
        return jsonify({'status': 1, 'message': message, 'data': {}})
    return jsonify({'status': 0, 'message': message, 'data': data_dict})


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/recipe_detail', methods=['GET', 'POST'])
def recipe_detail():
    return render_template('describe.html')


@app.route('/post_recipe_list', methods=['POST'])
def post_recipe_list():
    limit = request.json.get('limit')
    limit = int(limit)
    ret_dict = {}
    ret_dict['recipeList'] = []
    line_list = []
    with open('./0924.txt') as fp:
        for line in fp:
            segs = line[:-1].split('\t')
            line_list.append[segs]
    sample_list = random.sample(line_list, limit)
    for segs in sample_list:
        recipe_id, recipe_name = segs[:2]
        recipe_pic = segs[4]
        item = {}
        item['recipe_id'] = recipe_id
        item['recipe_name'] = recipe_name
        item['recipe_pic'] = recipe_pic
        ret_dict['recipeList'].append(item)
    return pack_json(ret_dict, 'success')


@app.route('/get_recipe_list', methods=['GET'])
def get_recipe_list():
    limit = request.args.get('limit')
    limit = int(limit)
    ret_dict = {}
    ret_dict['recipeList'] = []
    line_list = []
    with open('./0924.txt') as fp:
        for line in fp:
            segs = line[:-1].split('\t')
            line_list.append(segs)
    sample_list = random.sample(line_list, limit)
    for segs in sample_list:
        recipe_id, recipe_name = segs[:2]
        recipe_pic = segs[4]
        item = {}
        item['recipe_id'] = recipe_id
        item['recipe_name'] = recipe_name
        item['recipe_pic'] = recipe_pic
        ret_dict['recipeList'].append(item)
    return pack_json(ret_dict, 'success')


@app.route('/post_recipe_detail', methods=['POST'])
def post_recipe_detail():
    recipe_id = request.json.get('recipe_id')
    ret_dict = {}
    if recipe_id in mem_table:
        ret_dict['recipeDetail'] = []
        segs = mem_table[recipe_id]
        recipe_name = segs[1]
        recipe_pic = segs[4]
        recipe_desc = segs[-1]
        item = {}
        item['recipe_id'] = recipe_id
        item['recipe_name'] = recipe_name
        item['recipe_pic'] = recipe_pic
        item['recipe_desc'] = recipe_desc
        item['recipe_url'] = 'http://www.xiachufang.com/recipe/' + \
                             recipe_id
        ret_dict['recipeDetail'].append(item)
        return pack_json(ret_dict, 'success')
    return pack_json(ret_dict, 'error')


@app.route('/get_recipe_detail', methods=['GET'])
def get_recipe_detail():
    recipe_id = request.args.get('recipe_id')
    ret_dict = {}
    if recipe_id in mem_table:
        ret_dict['recipeDetail'] = []
        segs = mem_table[recipe_id]
        recipe_name = segs[1]
        recipe_pic = segs[4]
        recipe_desc = segs[-1]
        item = {}
        item['recipe_id'] = recipe_id
        item['recipe_name'] = recipe_name
        item['recipe_pic'] = recipe_pic
        item['recipe_desc'] = recipe_desc
        item['recipe_url'] = 'http://www.xiachufang.com/recipe/' + \
                             recipe_id
        ret_dict['recipeDetail'].append(item)
        return pack_json(ret_dict, 'success')
    return pack_json(ret_dict, 'error')


@app.route('/post_recipe_button', methods=['POST'])
def post_recipe_button():
    ret_dict = {'time': 1443172440, 'is_like': 1,
                'cur_page': '/recipelist.html'}
    recieve_dict = request.json.get('data')
    ret_dict = {}
    ret_dict['time'] = recieve_dict['time']
    ret_dict['is_like'] = recieve_dict['is_like']
    ret_dict['cur_page'] = recieve_dict['cur_page']
    return pack_json(ret_dict, 'success')


@app.route('/get_recipe_button', methods=['GET'])
def get_recipe_button():
    ret_dict = {'time': 1443172440, 'is_like': 1,
                'cur_page': '/recipelist.html', 'recipe_id': '100020144'}
    return pack_json(ret_dict, 'success')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: "
                        "%(asctime)s: %(filename)s: %(lineno)d * "
                        "%(thread)d %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    app.run(host='101.200.198.128', debug=True)
