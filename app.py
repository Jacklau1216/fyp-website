import random

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from numpy import arange
import re
import os
from docx import Document
from PyPDF2 import PdfReader

UPLOAD_FOLDER = 'upload_file'
ALLOWED_EXTENSIONS = {'txt'}
from watermarking import demo_watermark as watermarking
from argparse import Namespace
args = Namespace()
from detector.ensemble_detector import EnsembleDectector
detector = EnsembleDectector()

arg_dict = {
    'run_gradio': False, 
    'demo_public': False, 
    'model_name_or_path': 'facebook/opt-125m', 
    # 'model_name_or_path': 'facebook/opt-1.3b', 
    # 'model_name_or_path': 'facebook/opt-2.7b', 
    # 'model_name_or_path': 'facebook/opt-6.7b',
    # 'model_name_or_path': 'facebook/opt-13b',
    # 'load_fp16' : True,
    'load_fp16' : False,
    'prompt_max_length': None, 
    'max_new_tokens': 200, 
    'generation_seed': 123, 
    'use_sampling': True, 
    'n_beams': 1, 
    'sampling_temp': 0.7, 
    'use_gpu': True, 
    'seeding_scheme': 'simple_1', 
    'gamma': 0.25, 
    'delta': 2.0, 
    'normalizers': '', 
    'ignore_repeated_bigrams': False, 
    'detection_z_threshold': 4.0, 
    'select_green_tokens': True,
    'skip_model_load': False,
    'seed_separately': True,
}

args.__dict__.update(arg_dict)
args.normalizers = (args.normalizers.split(",") if args.normalizers else [])
model, tokenizer, device = watermarking.load_model(args)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = '123'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
db = SQLAlchemy(app)



class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    useremail = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.Boolean) # 1: staff; 0: student
    course = db.Column(db.String(100),nullable=True)
    
    
    def __init__(self, useremail, password):
        self.useremail = useremail
        self.password = password
        self.role = 1 if 'staff' in useremail else 0
   
    
class Text(db.Model):
    input_id = db.Column(db.Integer, primary_key=True)
    input_text = db.Column(db.String,nullable=False)
    detection_result = db.Column(db.Boolean,nullable=True)
    watermark_result = db.Column(db.String,nullable=True)

class File(db.Model):
    file_id = db.Column(db.Integer, primary_key=True)
    input_file = db.Column(db.String,nullable=False)
    detection_result = db.Column(db.Boolean,nullable=True)
    watermark_result = db.Column(db.String,nullable=True)
    
        

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login_check():
    if not request.form:
        return render_template('login.html')

    useremail = request.form['useremail']
    password = request.form['password']

    user = User.query.filter_by(useremail=useremail).first()
    if user and user.password == password:
        session['user_login'] = True
        flash("Login successfully", 'info')
        return redirect(url_for('llm_detection'))
    else:
        flash('Incorrect email or password. Please try again.', 'error')
        return render_template('login.html')


@app.route('/llm_detection', methods=['GET', 'POST'])
def llm_detection():
    if not session.get('user_login', False):
        return redirect(url_for('login_check'))

    return render_template('llm_detection.html')

@app.route('/logout', methods=['GET'])
def logout():
    session['user_login'] = False
    return render_template('index.html')

email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
@app.route('/watermark', methods=['GET'])
def watermark():
    if not session.get('user_login', False):
        return redirect(url_for('login_check'))
    return render_template('watermark.html')

@app.route('/generate', methods=['POST'])
def generate():
    if not request.form:
        return "Error: not receive any text!"
    text = request.form['text']
    _, _, decoded_output_without_watermark, decoded_output_with_watermark, _ = watermarking.generate(text, args, model=model, device=device, tokenizer=tokenizer)
    return decoded_output_with_watermark

@app.route('/register', methods=['GET', 'POST'])
def register():
    useremail = None

    if not request.form:
        return render_template('register.html')

    useremail = request.form['useremail']
    password = request.form['password']
    password2 = request.form['password2']

    existing_user = User.query.filter_by(useremail=useremail).first()
    if existing_user:
        flash('User name have already exist. Please try again.', 'error')
        return render_template('register.html')

    if password != password2:
        flash("Two password don't match. Please try again", 'error')
        return render_template('register.html')

    if not re.match(email_regex, useremail):
        flash("Invalid email format. Please try again.", 'error')
        return render_template('register.html')

    new_user = User(useremail=useremail, password=password)
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
    overall_result, chunks_predict_result, text_is_AI_percentage, chunk_is_AI_probability = detector.detect_text(text)

    existing_text = Text.query.filter_by(input_text=text).first()
    if existing_text:
        existing_text.detection_result = overall_result
    else:
        detection_text = Text(input_text=text, detection_result=overall_result)
        db.session.add(detection_text)

    db.session.commit()

    return [str(overall_result).capitalize(), text_is_AI_percentage, chunks_predict_result, chunk_is_AI_probability]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route('/detect_file', methods=['POST'])
def detect_file():
    if request.method == 'POST':
        detection_result = bool(random.getrandbits(1))
        file = request.files['file']
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        file_content = ""
        if filename.endswith('.txt'):
            # Read the content of the TXT file
            with open(file_path, 'r') as f:
                file_content = f.read()
        elif filename.endswith('.doc') or filename.endswith('.docx'):
            # Read the content of the DOC/DOCX file
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                file_content += paragraph.text + "\n"
        elif filename.endswith('.pdf'):
            # Read the content of the PDF file
            reader = PdfReader(file_path)
            number_of_pages = len(reader.pages)
            page = reader.pages[0]
            file_content = page.extract_text()
        else:
            flash('Invalid file type! Only TXT, DOC, DOCX, and PDF files are allowed.', 'error')
        # Print the file content
        print(file_content,str(detection_result))
        
        existing_file = File.query.filter_by(input_file=filename).first()
        if existing_file:
            existing_file.detection_result = detection_result
        else:
            detection_file = File(input_file=filename, detection_result=detection_result)
            db.session.add(detection_file)
        db.session.commit()
        return jsonify({'message': 'File uploaded successfully'})


   

@app.route('/course', methods=['GET'])
def course():
    if not session.get('user_login', False):
            return redirect(url_for('login_check'))
    return render_template('course.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
