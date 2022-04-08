from model import DetectionClassificationModel
from tools import allowed_file, preprocess_img

import torch
from flask import Flask, request, flash, redirect, render_template
import os, json

app = Flask(__name__)

app.config['WORK_DIR'] = os.getcwd()
app.config['UPLOAD_FOLDER'] = app.config['WORK_DIR'] + '/data/upload_impages/'
model = DetectionClassificationModel(w_cl_path=app.config['WORK_DIR'] + '/app/weights/weights_dense.wght')
class2name =  json.load(open(app.config['WORK_DIR'] + "/configs/class2name.json"))

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
def home_endpoint():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def get_prediction():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        file_tr = preprocess_img(file)
        outp = model(file_tr[None, :])
        _, pred = torch.max(outp, 1)
        pred_cl = class2name[str(pred.item())]
        flash(pred_cl)
        return redirect('/')

if __name__ == '__main__':
    app.run(
        host='0.0.0.0', 
        port=int(os.getenv('PORT', 4444)),
        debug=False
        )