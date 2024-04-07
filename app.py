from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = '123'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __repr__(self):
        return "<User %r>" % self.username


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login', methods=['GET','POST'])
def login_check():
    if not request.form:
        return render_template('login.html')
                
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        session['username'] = username
        flash("Login successfully", 'info')
        return redirect(url_for('llm_detection'))
    else:
        flash('Incorrect username or password. Please try again.', 'error')
        return render_template('login.html')


@app.route('/llm_detection')
def llm_detection():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('llm_detection.html')


@app.route('/register', methods=['GET','POST'])
def register():
    username = None
    
    if not request.form:
        return render_template('register.html')
                
    username = request.form['username']
    password = request.form['password']
    password2 = request.form['password2']
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash('User name have already exist. Please try again.', 'error')
        return render_template('register.html')
    
    if password != password2:
        flash("Two password don't match. Please try again", 'error')
        return render_template('register.html')
        
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    flash("Register successfully", 'info')
    return redirect(url_for('llm_detection'))

@app.route('/detect', methods=['POST'])
def detect():
    text = request.form['text']
    # Perform LLM detection logic
    def detect():
        return [random.randint(0,100)]
    result = detect()
    
    return result


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Check if the dummy user already exists
        dummy_user = User.query.filter_by(username='dummy').first()
        if not dummy_user:
            dummy_user = User(username='dummy', password='123')
            db.session.add(dummy_user)
            db.session.commit()
            print('user created')
    app.run(debug=True)
    