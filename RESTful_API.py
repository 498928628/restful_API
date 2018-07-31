#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, abort, request, jsonify

app = Flask(__name__)

# 测试数据暂时存放
stocks = []


@app.route('/add_stock/', methods=['POST'])
def add_stock():
    if not request.json or 'code' not in request.json or 'name' not in request.json:
        print('request.json', request.json)
        print('request.json[code]', request.json['code'])
        abort(400)
    stock = {
        'code': request.json['code'],
        'name': request.json['name']
    }
    stocks.append(stock)
    return jsonify({'result': 'success'})


@app.route('/get_stock/', methods=['GET'])
def get_stock():
    print('request.args', request.args)
    if not request.args or 'code' not in request.args:
        # 没有指定code则返回全部

        return jsonify(stocks)
    else:
        code = request.args['code']
        print(filter(lambda t: t['code'] == int(code), stocks))
        stock = list(filter(lambda t: t['code'] == int(code), stocks))
        return jsonify(stock) if stock else jsonify({'result': 'not found'})


if __name__ == "__main__":
    # 将host设置为0.0.0.0，则外网用户也可以访问到这个服务
    app.run(host="0.0.0.0", port=3838, debug=True)
