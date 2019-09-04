from flask import Flask

app = Flask(__name__)

# @app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet')
@app.route('/greet/<name>')
def hello(name='Programmer'):
    return '<h1>Hello %s!</h1>' % name

if __name__ == '__main__':
    app.run()