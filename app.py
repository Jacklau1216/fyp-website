import random

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from numpy import arange
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
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login_check():
    if not request.form:
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        session['user_login'] = True
        flash("Login successfully", 'info')
        return redirect(url_for('llm_detection'))
    else:
        flash('Incorrect username or password. Please try again.', 'error')
        return render_template('login.html')


@app.route('/llm_detection')
def llm_detection():
    if not session.get('user_login', False):
        return redirect(url_for('login_check'))

    return render_template('llm_detection.html')

@app.route('/logout', methods=['GET'])
def logout():
    session['user_login'] = False
    return render_template('index.html')

@app.route('/watermark', methods=['GET'])
def watermark():
    if not session.get('user_login', False):
        return redirect(url_for('login_check'))
    return render_template('watermark.html')

@app.route('/generate', methods=['POST'])
def generate():
    if not request.form:
        return "Error"
    return "Hi what's up (%s)" % random.randint(0,100)

@app.route('/register', methods=['GET', 'POST'])
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
    session['user_login'] = True
    flash("Register successfully", 'info')
    return redirect(url_for('llm_detection'))


@app.route("/GLTR_detect", methods=['POST'])
def GLTR_detect():
    text = request.form['text']
    import myGLTR
    gpt2 = myGLTR.GPT2()
    data = gpt2.analyze(text, 40)
    import math
    m = dict()
    m["topk"] = gpt2.model.lm.getTopKCount(data["real_topk"], [10, 100, 1000, math.inf])
    m["fracp"] = gpt2.model.lm.getFracpCount(data["real_topk"], data["pred_topk"], arange(0,1,0.1))
    m["top10Entropy"] = gpt2.model.lm.getTopEntropy(data["pred_topk"], arange(0,2.4,0.2))
    m["real_topk"] = data["real_topk"]
    m["pred_topk"] = data["pred_topk"]
    m["bpe_strings"] = [i+'&nbsp;' for i in data["bpe_strings"]]
    # m["bpe_strings"]  = [str(filter(gpt2.model.lm.postprocess,i)) for i in data["bpe_strings"]]
    m["topk_display"] = list(zip(m["bpe_strings"][1:],[ i[0] for i in data["real_topk"]]))
    m["pop_up_display"] = [(topk, prob, fp) for ((topk, prob), fp) in zip(data["real_topk"], gpt2.model.lm.getFracp(data["real_topk"],data["pred_topk"]))]

    m["countArray"] = [10,100,1000,10000000]
    return jsonify(m)


@app.route('/detect', methods=['POST'])
def detect():
    text = request.form['text']
    detection_result = bool(random.getrandbits(1))

    existing_text = Text.query.filter_by(input_text=text).first()
    if existing_text:
        existing_text.detection_result = detection_result
    else:
        detection_text = Text(input_text=text, detection_result=detection_result)
        db.session.add(detection_text)

    db.session.commit()

    return str(detection_result).capitalize()

@app.route('/upload', methods=['POST'])
def upload():
    content = request.form['content']

    existing_text = Text.query.filter_by(input_text=content).first()
    if existing_text:
        existing_text.watermark_result = "Generating"
    else:
        text_entry = Text(input_text=content, watermark_result="Generating")
        db.session.add(text_entry)

    db.session.commit()

    return "File uploaded successfully!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
