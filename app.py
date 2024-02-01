from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from datetime import date, timedelta
import os

app = Flask(__name__)
app.secret_key = "zx5qsEyijgsjOhLrA7u"
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
def index():
    image_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    return render_template('index.html', image_files=image_files)


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        print(request.url)

        if 'image' not in request.files:
            return redirect(request.url)#GET

        file = request.files['image']

        if file.filename == '':
            return redirect(request.url)

        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            return redirect(url_for('index'))
    else:#get
        return redirect(url_for('page_not_found'))



@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

#if __name__ == '__main__':
    #app.run(port=8181, host="0.0.0.0")
    #app.run(debug=True)
    #app.run()