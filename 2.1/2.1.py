#coding:utf-8
__author__ = 'Mr. null'

from flask import Flask, request, jsonify

app = Flask(__name__)

# 定义door接口，参数p值为"open"时返回开门，为"close"时返回关门
@app.route('/door',methods= ["GET"])
def door():
    p = request.args.get("p")
    if p == 'open':
        return jsonify(code=0,msg="开门")
    elif p == 'close':
        return jsonify(code=1,msg="关门")

if __name__ == '__main__':
	app.run()
