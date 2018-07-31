#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

STOCKS = {
    601858: {'name': '中国科传'},
    603607: {'name': '京华激光'},
}


def abort_if_stock_doesnt_exist(code):
    if int(code) not in STOCKS:
        abort(404, message="Code {} doesn't exist".format(code))


parser = reqparse.RequestParser()
parser.add_argument('name')


# # 操作（put / get / delete）单一资源Stock

class Stock(Resource):
    def get(self, code):
        abort_if_stock_doesnt_exist(code)
        return STOCKS[int(code)]

    def delete(self, code):
        abort_if_stock_doesnt_exist(code)
        del STOCKS[int(code)]
        return '', 204

    def put(self, code):
        args = parser.parse_args()
        name = {'name': args['name']}
        STOCKS[int(code)] = name
        return name, 201


# # 操作（post / get）资源列表StockList

class StockList(Resource):
    def get(self):
        return STOCKS

    def post(self):
        args = parser.parse_args()
        print("args", args)
        code = int(max(STOCKS.keys())) + 1
        STOCKS[int(code)] = {'name': args['name']}
        return STOCKS[int(code)], 201


# 设置路由
api.add_resource(StockList, '/stocks')
api.add_resource(Stock, '/stocks/<code>')

if __name__ == '__main__':
    app.run(debug=True)
