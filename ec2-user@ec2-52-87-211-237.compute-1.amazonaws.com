from model import get_model
from tools import allowed_file, img2tensor

import torch
import numpy as np
from flask import Flask, request, flash, redirect
import os, json

model, class2name = get_model(), json.load(open("configs/class2name.json"))
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/upload_images/'



def load_model():
    # global model
    # model variable refers to the global variable
    PATH = 'weights/weights_dense.wght'
    model.load_state_dict(torch.load(PATH, map_location='cpu'))
    model.eval()


@app.route('/')
def home_endpoint():
    return 'fruits classification' + str(model)


@app.route('/predict', methods=['POST'])
def get_prediction():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        # filename = file.filename
        # with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'w+') as f:
        #     file.save(f)
        file_tr = img2tensor(file)
        outp = model(file_tr[None, :])
        _, pred = torch.max(outp, 1)
        return class2name[str(pred.item())]

if __name__ == '__main__':
    load_model()  # load model at the beginning once only
    app.run(host='0.0.0.0', port=80)