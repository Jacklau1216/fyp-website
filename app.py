from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = '123'
db = SQLAlchemy(app)



class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
class Text(db.Model):
    input_id = db.Column(db.Integer, primary_key=True)
    input_text = db.Column(db.String,nullable=False)
    detection_result = db.Column(db.Boolean,nullable=True)
    watermark_result = db.Column(db.String,nullable=True)
    
    # def __init__(self, input_text, detection_result, watermark_result):
    #     self.input_text = input_text
    #     self.detection_result = detection_result
    #     self.watermark_result = watermark_result
        

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

    flash("Register successfully", 'success')
    return redirect(url_for('llm_detection'))

@app.route('/detect', methods=['POST'])
def detect():
    text = request.form['text']
    detection_result = bool(random.getrandbits(1))
    detection_text = Text(input_text=text,detection_result=detection_result)
    db.session.add(detection_text)
    db.session.commit()
    # Perform LLM detection logic
    def detect():
        return str(detection_result).capitalize()
    result = detect()
    
    return result


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    