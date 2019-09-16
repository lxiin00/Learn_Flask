from flask import Flask, flash, redirect, render_template, url_for, request
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from threading import Thread
import os

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.config.update(
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string'),
    # MAIL_SERVER = os.getenv('MAIL_SERVER'),
    MAIL_SERVER = 'smtp.qq.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    # MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
    MAIL_USERNAME = 'xxx',
    # MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
    MAIL_PASSWORD = 'xxxx',
    # MAIL_DEFAULT_SENDER = ('Lxiin00', os.getenv('MAIL_USERNAME'))
    MAIL_DEFAULT_SENDER = ('Lxiin00', 'xxx')
)

mail = Mail(app)

def send_smtp_mail(subject, to, body):
    message = Message(subject, recipients=[to], body=body)
    mail.send(message)

def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)

def send_async_email(subject, to, body):
    message = Message(subject, recipients=[to], body=body)
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr

def send_subscribe_mail(subject, to, **kwargs):
    message = Message(subject, recipients=[to], sender='XXX')
    message.body = render_template('emails/subscribe.txt', **kwargs)
    message.html = render_template('emails/subscribe.html', **kwargs)
    mail.send(message)

class SubscribeForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired()])
    submit = SubmitField('订阅')

class EmailForm(FlaskForm):
    to = StringField('发送给', validators=[DataRequired(), Email()])
    subject = StringField('主题', validators=[DataRequired()])
    body = TextAreaField('内容', validators=[DataRequired()])
    submit_smtp = SubmitField('普通发送')
    submit_async = SubmitField('异步发送')


@app.route('/index', methods=['GET', 'POST'])
def index():
    form = EmailForm()
    if form.validate_on_submit():
        to = form.to.data
        subject = form.subject.data
        body = form.subject.data
        if form.submit_smtp.data:
            send_smtp_mail(subject, to, body)
            method = request.form.get('submit_smtp')
        else:
            send_async_email(subject, to, body)
            method = request.form.get('submit_async')
        flash('邮件已经发送至 %s！请检查！' % form.to.data)
        return redirect(url_for('index'))
    form.subject.data = 'Hello World!'
    form.body.data = '您好～'
    return render_template('index.html', form=form)

@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    form = SubscribeForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        flash('发送成功！')
        # send_smtp_mail('订阅成功！', email, '您好，感谢您的订阅!')
        send_subscribe_mail('订阅成功！', email, name=name)
        return redirect(url_for('index'))
    return render_template('subscribe.html', form=form)

@app.route('/unsubscribe')
def unsubscribe():
    flash('想取消订阅？！没门！')
    return redirect(url_for('subscribe'))

if __name__ == '__main__':
    app.run(debug=True)