from flask import Flask, redirect, url_for, abort

app = Flask(__name__)

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

@app.route('/404')
def not_found():
    abort(404)

if __name__ == '__main__':
    app.run()