from flask import Flask, redirect, url_for, abort, request, session
from flask import make_response, json, jsonify
import os


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string') # 用session设置cookie值，这里定义一个加密密钥

# @app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/hello')
@app.route('/greet/<name>', methods=['GET'])
def hello(name='Programmer'):
    return '<h1>Hello %s!</h1>' % name

# <转换器:变量名>
@app.route('/goback/<int:year>')
def go_back(year):
    return '<p>Welcome to %d!</p>' % (2019 - year)

colors = ['blue', 'white', 'red']
@app.route('/colors/<any(%s):color>' % str(colors)[:-1])
def three_color(color):
    # return '<p>My favorite color is %s' % color
    # 响应状态码重定向的2种写法
    # return '', 302, {'Location': 'https://www.baidu.com'}
    # return redirect('https://www.baidu.com')
    return redirect(url_for('hello')) # 必须保证视图函数和路径名一致

# abort()函数用于传入状态码，即可返回对应的错误响应
@app.route('/404')
def not_found():
    abort(404)

@app.route('/500')
def not_found1():
    abort(500)

# make_response可以设置响应格式
@app.route('/foo')
def foo():
    response = make_response('Hello World!')
    response.mimetype ='text/html'
    return response
# 设置json格式响应的2种方法（json和jsonify）
@app.route('/json_test')
def json_test():
    # data = {
    #     'name': 'Grey',
    #     'gender': 'male'
    # }
    # response = make_response(json.dumps(data))
    # response.mimetype = 'application/json'
    # return response
    return jsonify(name='Grey', gender='male')

@app.route('/')
@app.route('/hello2')
def hello2():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'Human')
    return '<h1>Hello %s</h1>' % name

# 通过set_cookie可以设置cookie
@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello2')))
    response.set_cookie('name', name)
    return response

@app.route('/hello3')
def hello3():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'Human')
        response = '<h1>Hello, %s</h1>' % name
        if 'logged_in' in session:
            response += '[Authenticated]'
        else:
            response += '[Not Authenticated]'
        return response

# 通过Flask的session设置一个加密的cookies
@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello3'))

# 模拟管理后台，只有session里面有登录信息，才能访问后台
@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    else:
        return 'Welcome to admin page!'

# 模拟退出登录
@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))

if __name__ == '__main__':
    app.run()