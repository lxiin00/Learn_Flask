from flask import Flask, render_template, request, url_for, flash, redirect, session, send_from_directory
from forms import LoginForm, UploadForm, MultiUploadForm
from flask_wtf import FlaskForm
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError
import os
import uuid

app = Flask(__name__)

app.secret_key = 'secret string'

app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024# 设置上传文件的最大值（单位为字节byte）
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
app.config['ALLOWED_EXTENSIONS'] = ['png', 'jpg', 'jpeg', 'gif']

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

# 统一处理对所有上传的文件重新命名
def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename

@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/uploaded-images')
def show_images():
    return render_template('uploaded.html')

@app.errorhandler(413)
def too_large(e):
    return render_template('errors/413.html'), 413

# 上传单份文件
@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = random_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('上传成功！')
        session['filenames'] = [filename]
        return redirect(url_for('show_images'))
    return render_template('upload_file.html', form=form)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# 上传多份文件
@app.route('/multi-upload', methods=['GET', 'POST'])
def multi_upload():
    form = MultiUploadForm()
    if request.method == 'POST':
        filenames = []
        try:
            validate_csrf(form.csrf_token.data)
        except ValidationError:
            flash('CSRF token 错误！')
            return redirect(url_for('multi_upload'))

        if 'photo' not in request.files:
            flash('文件不存在！')
            return redirect(url_for('multi_upload'))

        for f in request.files.getlist('photo'):
            if f and allowed_file(f.filename):
                filename = random_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                filenames.append(filename)
            else:
                flash('文件无效！')
                return redirect(url_for('multi_upload'))
        flash('上传成功！')
        session['filenames'] = filenames
        return redirect(url_for('show_images'))
    return render_template('upload_file.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)