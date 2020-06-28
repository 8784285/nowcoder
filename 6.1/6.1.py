#coding:utf-8
__author__ = 'Mr. null'

'''
将登录获取token逻辑与开关门逻辑分开
'''
from flask import Flask, request, jsonify
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import json
import  MySQLdb

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config['SECRET_KEY']='nowcoder'
auth = HTTPTokenAuth()

_db = MySQLdb.connect(host="localhost",user="root",passwd="root123",db="apitest",charset="utf8")
_cursor = None

def create_token(username,password):
    """创建token"""
    s = Serializer(app.config["SECRET_KEY"],expires_in = 24 * 3600)
    token = s.dumps({"username":username,"password":password})
    return token

@auth.verify_token
def verify_token(token):
    """校验token"""
    s = Serializer(app.config["SECRET_KEY"])
    try:
        data = s.loads(token)
    # except SignatureExpired:
    #     raise SignatureExpired('令牌已过期')
    # except BadSignature:
    #     raise BadSignature('令牌不合法')
    except Exception:
        return None
    user = data['username']
    return user

@app.route('/login',methods= ["POST"])
def login():
    """登录验证用户名密码正确性，如正确返回token"""
    j_data = json.loads(request.get_data())
    try:
        inp_name = j_data['username']
        inp_password = j_data['password']
    except:
        return jsonify(code=1001,msg="参数缺失")

    #sql = "SELECT * FROM users WHERE name = '%s' AND password = '%s'"%(inp_name, inp_password)
    sql = "SELECT * FROM users WHERE name = '%s' AND password = '%s'"%(inp_name, inp_password)
    print(sql)
    cursor = _db.cursor()
    rows = cursor.execute(sql)

    if rows:
        token = create_token(inp_name,inp_password)
        return jsonify(code=4,msg="登录成功",token=token.decode())
    else:
        return jsonify(code=2,msg="非法用户")
    _cursor.close()

@app.route('/door',methods= ["GET"])
@auth.login_required
def door():
    """请求需要验证用户是否已登录，若已登录，参数p值为"open"时返回开门，为"close"时返回关门"""
    if 'p' not in request.args.keys():
        return jsonify(code=1001,msg="p参数缺失")
    p = request.args.get("p")
    if p == 'open':
        return jsonify(code=0,msg="开门")
    elif p == 'close':
        return jsonify(code=1,msg="关门")
    else:
        return jsonify(code=1002,msg="p参数非法，取值[close,open]")

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)

