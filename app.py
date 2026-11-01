import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pickle
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blessings.db'
db = SQLAlchemy(app)

app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-key")

class Blessing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(280),nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    blessings = Blessing.query.order_by(Blessing.date.desc()).all()
    return render_template('home.html',blessings=blessings)

@app.route('/submit',methods=['POST'])
def submit():
    text = request.form['text'].strip()
    if text:
        db.session.add(Blessing(text=text[:280]))
        db.session.commit()
    return redirect('/')

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

