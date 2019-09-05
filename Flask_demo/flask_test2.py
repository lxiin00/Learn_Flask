'''
重定向
'''

from flask import Flask, url_for, redirect

app = Flask(__name__)


@app.route('/hello')
def hello(name='Programmer'):
    return '<h1>Hello, %s</h1>' % name

@app.route('/do_something')
def do_something():
    # do something
    return redirect(url_for('hello'))

@app.route('/foo')
def foo():
    return '<h1>Foo page</h1><a href="%s">Do something</a>' % url_for('do_something')

@app.route('/bar')
def bar():
    return '<h1>Bar page</h1><a href="%s">Do something</a>' % url_for('do_something')


if __name__ == '__main__':
    app.run()