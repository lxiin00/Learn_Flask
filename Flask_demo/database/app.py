from flask import Flask, flash, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
import os
import click

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:////' + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret string'  # app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')


db = SQLAlchemy(app)

@app.cli.command()
def initdb():
    db.create_all()
    click.echo('已初始化的数据库')


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)

    def __repr__(self):
        return '<Note %r>' % self.body

class NewNoteForm(FlaskForm):
    body = TextAreaField('内容', validators=[DataRequired()])
    submit = SubmitField('提交')

class DeleteNoteForm(FlaskForm):
    submit = SubmitField('删除')

@app.route('/new', methods=['GET', 'POST'])
def new_note():
    form = NewNoteForm()
    if form.validate_on_submit():
        body = form.body.data
        note = Note(body=body)
        db.session.add(note)
        db.session.commit()
        flash('Note已经保存成功！')
        return redirect(url_for('index'))
    return render_template('new_note.html', form=form)

@app.route('/index')
def index():
    form = DeleteNoteForm()
    notes = Note.query.all()
    return render_template('index.html', notes=notes, form=form)


if __name__ == '__main__':
    app.run(debug=True)
