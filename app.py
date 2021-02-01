from flask import Flask, render_template, request
from check_validation import check_validation
import sys
import os

app = Flask(__name__)


UPLOAD_FOLDER = '/static/uploads/'


@app.route('/', methods=['POST', 'GET'])
def home_page(name=None):
    if request.method == 'POST':
        if 'file' not in request.files:
            msg = "file not found in request files"
            return render_template('index.html', msg='No file selected')
        file = request.files['file']
        text = request.form['text']
        if file.filename == '':
            msg = "file no file"
            return render_template('index.html', msg='No file selected')
        if file:
            msg = check_validation(text, file)
            msg2 = ""
            if "Success" in msg:
                msg2 = ("Value: $" + text)
            else:
                msg2 = ("Value: " + "NaN")

            return render_template('index.html',
                                   msg=msg,
                                   msg2=msg2,
                                   img_src=UPLOAD_FOLDER + file.filename)
    elif request.method == 'GET':
        return render_template('index.html')
    return render_template('index.html', name=name)


if __name__ == '__main__':
    app.run()
