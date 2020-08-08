#coding:utf-8
__author__ = 'Mr. null'
'''
实现认证功能
'''
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/door',methods= ["GET"])
def door():
    """定义door接口，先验证username和password的正确性，如验证通过，则参数p值为"open"时返回开门，为"close"时返回关门"""
    p = request.args.get("p")
    username = request.args.get("username")
    password = request.args.get("password")
    if username == 'Mr.null' and password == 'dc483e80a7a0bd9ef71d8cf973673924':
        if p == 'open':
            return jsonify(code=0,msg="开门")
        elif p == 'close':
            return jsonify(code=1,msg="关门")
    else:
        return jsonify(code=2,msg="非法用户")
if __name__ == '__main__':
	app.run(debug= 'True')
