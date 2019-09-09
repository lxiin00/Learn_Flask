from flask import Flask, render_template, request, url_for, flash, redirect
from forms import LoginForm, UploadForm
from flask_wtf import FlaskForm

app = Flask(__name__)

app.secret_key = 'secret string'

app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 # 设置上传文件的最大值（单位为字节byte）

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm()
    if form.validate_on_submit():# 等价于：if request.method == 'POST' and form.validate():
        username = form.username.data
        flash('Welcome home, %s!' % username)
        return redirect(url_for('index'))
    return render_template('basic.html', form=form)

@app.route('/bootstrap')
def bootstrap():
    form = LoginForm()
    return render_template('bootstrap.html', form=form)

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    return render_template('upload_file.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)