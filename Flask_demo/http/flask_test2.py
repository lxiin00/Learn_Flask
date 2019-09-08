'''
Http重定向
'''

from flask import Flask, url_for, redirect, request, jsonify, render_template
from urllib.parse import urljoin, urlparse
from jinja2.utils import generate_lorem_ipsum

app = Flask(__name__)

@app.route('/hello')
def hello(name='Programmer'):
    return '<h1>Hello, %s</h1>' % name

@app.route('/do_something')
def do_something():
    # return redirect(request.referrer or url_for('hello'))
    # return redirect(url_for('hello'))
    # return redirect(request.args.get('next'))
    # return redirect(request.args.get('next', url_for('hello')))
    return redirect_back()

@app.route('/foo')
def foo():
    return '<h1>Foo page</h1><a href="%s">Do something</a>' % url_for('do_something')

@app.route('/bar')
def bar():
    return '<h1>Bar page</h1><a href="%s">Do something</a>' % url_for('do_something', next=request.full_path)

def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))

# 对URL进行安全验证
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

# 返回局部数据-纯文本或局部HTML模板
@app.route('/comments/<int:post_id>')
def get_comments(post_id):
    # return render_template('comments.html')
    pass

# 返回局部数据-JSON数据
@app.route('/profile/<int:user_id>')
def get_profile(usid_id):
    # return jsonify(username=username, bio=bio)
    pass

# 返回局部数据-空值
@app.route('/post/delete/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    return '', 204

# 模拟AJAX加载更多
@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    return '''
    <h1>A very long post</h1>
    <div class='body'>%s</div>
    <button id='load'>Load More</button>
    <script src='https://code.jquery.com/jquery-3.3.1.min.js'></script>
    <script type='text/javascript'>
    $(function(){
        $('#load').click(function(){
            $.ajax({
                url: '/more',
                type: 'get',
                success: function(data){
                    $('.body').append(data);
                }
            })
        })
    })
    </script>
    ''' % post_body

@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)

if __name__ == '__main__':
    app.run(debug=True)