from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            session['username'] = username
            return redirect(url_for('llm_detection'))

        return render_template('login.html', message='Invalid username or password')

    return render_template('login.html', message='')


@app.route('/llm_detection')
def llm_detection():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('llm_detection.html')


@app.route('/register', methods=['POST'])
def register():
    new_username = request.form['new_username']
    new_password = request.form['new_password']

    existing_user = User.query.filter_by(username=new_username).first()
    if existing_user:
        return "Username already exists", 409

    new_user = User(username=new_username, password=new_password)
    db.session.add(new_user)
    db.session.commit()

    return "Registration successful", 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)