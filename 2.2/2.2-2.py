#coding:utf-8
__author__ = 'Mr. null'

from flask import Flask, request, jsonify

app = Flask(__name__)

# 定义接口door1，对参数p的参数值做int转换
@app.route('/door1',methods= ["GET"])
def door1():
    p = request.args.get("p")
    print(int(p) ,type(p))
    if int(p) == 0:
        return jsonify(code=0,msg="开门")
    elif int(p) == 1:
        return jsonify(code=1,msg="关门")
    else:
        return jsonify(code=10,msg='非法输入')

if __name__ == '__main__':
	app.run()
