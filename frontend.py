import os
import pandas as pd
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from sklearn.preprocessing import LabelEncoder
from joblib import load

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route("/", methods=['GET', 'POST'])
def main_page(name=None):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            df=pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            print(df)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


            clf = load(os.path.join(app.config['UPLOAD_FOLDER'], 'model.joblib'))
            # prediction = clf.predict(df)
            # print("Prediction:", prediction)
            return redirect(url_for('download_file', name=filename))
    return render_template('index.html', name=name)
@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)