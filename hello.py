from flask import Flask, render_template, jsonify
from flask import request

import numpy as np
import pandas as pd

import os
from flask import flash, request, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename


# UPLOAD_FOLDER = '/Users/yangkai/work/git/flask_start/uploads'
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'csv', 'png', 'jpg', 'jpeg', 'gif', 'json'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '123456'
# app.add_url_rule(
#     "/uploads/<name>", endpoint="download_file", build_only=True
# )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
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
            # return 'No selected file'
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('download_file', name=filename))
            # return str(request.files)
            return redirect(url_for('plot_scatter', title=filename))
        else:
            return render_template('upload.html')
    else:
        return render_template('upload.html')



@app.route('/plot_scatter/<title>')
def plot_scatter(title):
    return render_template("plot_scatter.html", Title=title)

@app.route('/stu/<filename>',)
def get_stu_data(filename):
    file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(file, index_col=0)
    return_dict = {}
    return_dict['chr'] = {}
    return_dict['pos'] = {}
    for c in ['chr1', 'chr2', 'chr3', 'chr4']:
        return_dict['pos'][c] = np.array(df[df['chr']==c]['pos']).tolist()
        return_dict['chr'][c] = np.array(df[df['chr']==c]['value'].reset_index()).tolist()
    # print(df)
    # print([df['number1'].to_list(), df['number2'].to_list()])
    return jsonify(return_dict)

    '''
    stu = range(100)
    studata1 = np.random.randint(1,10,100)
    studata2 = np.random.randint(1, 10, 100)
    name = []
    number1 = []
    number2 = []
    for a, b, c in zip(stu, studata1, studata2):
        name.append(str(a))
        number1.append(int(b))
        number2.append(int(c))
    return jsonify({"name": name, "number1": number1, "number2": number2})
    # return content
    '''

