from flask import Flask, render_template, request, redirect, send_file, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from encode import encrypt
from decode import decrypt
from sqlalchemy.sql import func
import os
import re

basedir = os.path.abspath(os.path.dirname(__file__))
save_path = os.path.join(basedir, 'bytecode.txt')
UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads') 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'register.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ALLOWED_EXTENSIONS = {'txt'}
app.config['UPLOAD_FOLDER '] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'gfahjsgfkag'


db = SQLAlchemy(app)

class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)   
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    
    def __repr__(self):
        return f'<Register {self.username}, {self.email}, {self.password}>'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/register/', methods = ['GET', 'POST'])
def register():
    msg = ""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        con_password = request.form['con_password']
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        elif password != con_password:
            msg = 'Password and confirm password does not match'
        else:            
            user = Register(username = username, email = email, password = password)
            #msg = 'User registered successfully'
            print('Hit here post')
            db.session.add(user)
            db.session.commit()
            return render_template('login.html')
    else:
        print('hit here get')
        return render_template('register.html', msg=msg)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        users = Register.query.all()
        print(users)
        names = []
        passwords = []
        for i in users:
            print('email:', i.email)
            print('password:', i.password)
            names.append(i.email)
            passwords.append(i.password)
        if email in names and password in passwords:
            return redirect('home_encodedecode')
        else:
            msg = "Incorrect email/password!"            
    return render_template('login.html', msg=msg)
    
@app.route('/login/home_encodedecode/', methods = ['GET', 'POST'])
def home_encodedecode():
    msg_encode = ''
    if request.method == 'POST' and 'encode_text' in request.form and 'encode_password' in request.form:
        encode_text = request.form['encode_text']
        secret_key = request.form['encode_password']    
        print(encode_text)    
        print(secret_key)
        result = encrypt(info = encode_text , secret_key = secret_key)
        msg_encode = result
        print(result)
        f = open(save_path, 'wb')
        f.write(msg_encode)
        f.close()
        return render_template('home_encodedecode.html', msg_encode = msg_encode)
    else:
        return render_template('home_encodedecode.html')
    
@app.route('/login/home_encodedecode/decode.html', methods = ['GET', 'POST'])
def decode():
    msg_decode = ''
    if request.method == 'POST' and 'decode_password' in request.form:
        file = request.files['file']
        secret_key = request.form['decode_password']
        filename = secure_filename(file.filename)

        file.save(os.path.join(app.config['UPLOAD_FOLDER '], filename))
        decode_file = os.path.join(app.config['UPLOAD_FOLDER '], filename)
        print('decode file is: ', decode_file)
        with open(decode_file, 'rb') as file:
            file_content = file.read()
        print('File content to decrypt : ', file_content)
        print('Secret key to decrypt: ', secret_key)
        result = decrypt(info=file_content, secret_key=secret_key)

        print('The decoded result is : ', result)
        
        return render_template('decode.html', msg_decode = result) 
    return render_template('decode.html')
    
@app.route('/download', methods = ['GET', 'POST'])
def download_file():
    p = 'bytecode.txt'
    return send_file(p, as_attachment=True)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)