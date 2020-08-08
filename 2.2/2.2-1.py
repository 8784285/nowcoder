#coding:utf-8
__author__ = 'Mr. null'

from flask import Flask, request, jsonify
app = Flask(__name__)

# 定义check_type接口，返回p参数值及类型
@app.route('/check_type',methods= ["GET"])
def check_type():
    p = request.args.get("p")
    return jsonify(code = 0, msg = "请求成功", p = p, type_p = str(type(p)))
if __name__ == '__main__':
	app.run()
