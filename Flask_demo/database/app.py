from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import click

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:////' + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.cli.command()
def initdb():
    db.create_all()
    click.echo('已初始化的数据库')


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)


if __name__ == '__main__':
    app.run(debug=True)
