#coding:utf-8
__author__ = 'Mr. null'

from flask import Flask, request, jsonify
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import json
import pymysql.connections as db_connection

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config['SECRET_KEY']='nowcoder'
auth = HTTPTokenAuth()

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
    _db = db_connection.Connection(host="localhost",user="root",passwd="root123",db="apitest",charset="utf8")
    j_data = json.loads(request.get_data())
    print(j_data)
    try:
        username = j_data['username']
        password = j_data['password']
    except:
        return jsonify(code=1001,msg="参数缺失")

    sql = "SELECT * FROM users WHERE name = '%s' AND password = '%s'"%(username, password)
    print(sql)
    cursor = _db.cursor()
    rows = cursor.execute(sql)

    if rows:
        token = create_token(username,password)
        return jsonify(code=4,msg="登录成功，欢迎您！",token=token.decode(),sql=sql)
    else:
        return jsonify(code=2,msg="非法用户")
    cursor.close()

@app.route('/news',methods= ["GET"])
#@auth.login_required
def news():
    _db = db_connection.Connection(host="localhost",user="root",passwd="root123",db="apitest",charset="utf8")
    #j_data = json.loads(request.get_data())
    newsid = request.args.get("newsid")
    sql = "SELECT * FROM news WHERE id = %s"%(newsid)
    cursor = _db.cursor()
    rows = cursor.execute(sql)
    data = cursor.fetchall()
    print(rows)
    if rows:
        return jsonify(code = 5, msg = "查询成功",sql = sql, count = rows, data = data)
    else:
        return jsonify(code = 6, msg = "未查询到数据", sql = sql)
    _cursor.close()

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)

