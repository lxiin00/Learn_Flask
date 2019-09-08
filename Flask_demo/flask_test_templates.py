from flask import Flask, render_template, Markup

app = Flask(__name__)

# 去掉渲染html显示的空行，效果和定界符内侧添加减号效果一样（这样并不影响实际效果，可有可无的操作）
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

user = {
    'username': 'Grey Li',
    'bio': 'A boy who loves movies and music.'
}

movies = [
    {'name': 'My Neighbor Totoro', 'year': '1988'},
    {'name': 'Three Colours trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'Perfect Blue', 'year': '1997'},
    {'name': 'The Matrix', 'year': '1999'},
    {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket list', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'},
    {'name': 'Gone Girl', 'year': '2014'},
    {'name': 'CoCo', 'year': '2017'},
]


@app.route('/')
def index():
    return '<h1>Hello, %s</h1>' % user['username']

@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies)

#注册模板上下文的处理函数
@app.context_processor
def inject_foo():
    foo = 'I am foo.'
    return dict(foo=foo) # 等同于 return '{'foo': foo}
# app.context_processor(lambda: dict(foo='I am foo.')) 等同于@app.context_processor

# 自定义过滤器--> {{ name|musical }}
@app.template_filter()
def musical(s):
    return s + Markup(' &#9835;')

# 将函数注册为模板全局函数
@app.template_global()
def bar():
    return 'I am bar.'

# 这样定义，可以在模板里面直接使用{{ text }}
@app.route('/hello')
def hello():
    text = Markup('<h1>Hello, Flask!</h1>')
    return render_template('index.html', text=text)

# 自定义测试器，函数名需要对应上
@app.template_test()
def baz(n):
    if n == 'baz':
        return True
    return False
# app.jinja_env.tests['baz'] = baz

if __name__ == '__main__':
    app.run(debug=True)