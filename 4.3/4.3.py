#coding:utf-8
__author__ = 'Mr. null'

from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/testapi',methods= ["GET"])
def testapi():
    print(request.headers)
    if 'Authorization' not in request.headers.keys():
        return jsonify(code=403, msg="header必填带上auth", status=False, data="")

    keys = request.args.keys()
    print(type(keys), keys)
    if "p1" not in request.args.keys():
        return jsonify(code=400, msg="p1参数必填", status=False, data="")
    if "p2" not in request.args.keys():
        return jsonify(code=400, msg="p2参数必填", status=False, data="")

    p1 = request.args.get("p1")
    if p1 not in ["1", "2", "3"]:
        return jsonify(code=400, msg="p1只能取值1,2,3", status=False, data="")

    return jsonify(code=0,msg=p1, status=True, data="")

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
	app.run()
