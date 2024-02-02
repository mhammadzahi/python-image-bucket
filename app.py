from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_session import Session
from datetime import date, timedelta
import os

app = Flask(__name__)
app.secret_key = "zs9qllEyijgsjoOoLrA7u"
app.config['UPLOAD_FOLDER'] = 'static/uploads'

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'
app.config['SESSION_PERMANENT'] = False 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
Session(app)

@app.before_request
def redirect_https():
    if os.environ.get('DYNO'):
        if request.headers.get('X-Forwarded-Proto') == 'http':
            url = request.url.replace('http://', 'https://', 1)
            return redirect(url, code=301)
        


@app.route('/')
def home():
    if 'user_id' in session:
        image_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
        return render_template('home.html', image_files=image_files)
    else:
        return(render_template('login.html'))



@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email.strip() == 'test@test.com' and password.strip() == '123':
        session['user_id'] = 1
        result = {"success": "yes"}
    else:
        result = {"success": "no"}

    return jsonify(result)



@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST' and 'user_id' in session:
        files = request.files.getlist('image')  # Use getlist for multiple files
        for file in files:
            if file:
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)
        
        return redirect(url_for('home'))
    else:
        return redirect(url_for('page_not_found'))



@app.route('/logout')
def clear_session():
    session.clear()
    return redirect(url_for('home')) 



@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

if __name__ == '__main__':
    #app.run(port=8181, host="0.0.0.0")
    app.run(debug=True)
    #app.run()

