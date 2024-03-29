from flask import Flask, render_template, request, url_for, flash, redirect, session, send_from_directory
from forms import LoginForm, UploadForm, MultiUploadForm, RichTextForm, NewPostForm, SigninForm, RegisterForm, SigninForm2, RegisterForm2
from flask_wtf import FlaskForm
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError
from flask_ckeditor import CKEditor
import os
import uuid

app = Flask(__name__)
ckeditor = CKEditor(app)

app.secret_key = 'secret string'

app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024# 设置上传文件的最大值（单位为字节byte）
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
app.config['ALLOWED_EXTENSIONS'] = ['png', 'jpg', 'jpeg', 'gif']

app.config['CKEDITOR_SERVER_LOCAL'] = True

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

# 富文本编辑器
@app.route('/ckeditor')
def ckeditor():
    form = RichTextForm()
    return render_template('ckeditor.html', form=form)

# 多提交按钮的富文本编辑器
@app.route('/two-submits', methods=['GET', 'POST'])
def two_submits_button():
    form = NewPostForm()
    if form.validate_on_submit():
        if form.save.data:
            flash('保存成功！')
        elif form.publish.data:
            flash('发布成功！')
        return redirect(url_for('index'))
    return render_template('two_submits.html', form=form)

# 单视图处理多个表单
@app.route('/multi-form', methods=['GET', 'POST'])
def multi_form():
    signin_form = SigninForm()
    register_form = RegisterForm()

    if signin_form.submit1.data and signin_form.validate():
        username = signin_form.username.data
        flash('%s, 你点击了登录按钮' % username)
        return redirect(url_for('index'))

    if register_form.submit2.data and register_form.validate():
        username = register_form.username.data
        flash('%s, 你点击了注册按钮' % username)
        return redirect(url_for('index'))

    return render_template('2form.html', signin_form=signin_form, register_form=register_form)

# 多视图处理多个表单
@app.route('/multi-form-multi-view')
def multi_form_multi_view():
    signin_form = SigninForm2()
    register_form = RegisterForm2()
    return render_template('2form2view.html', signin_form=signin_form, register_form=register_form)

@app.route('/handle-signin', methods=['POST'])
def handle_signin():
    signin_form = SigninForm2()
    register_form = RegisterForm2()

    if signin_form.validate_on_submit():
        username = signin_form.username.data
        flash('%s, 你点击了登录按钮' % username)
        return redirect(url_for('index'))
    return render_template('2form2view.html', signin_form=signin_form, register_form=register_form)

@app.route('/handle-register', methods=['POST'])
def handle_register():
    signin_form = SigninForm2()
    register_form = RegisterForm2()

    if register_form.validate_on_submit():
        username = register_form.username.data
        flash('%s, 你点击了登录按钮' % username)
        return redirect(url_for('index'))
    return render_template('2form2view.html', signin_form=signin_form, register_form=register_form)

if __name__ == '__main__':
    app.run(debug=True)