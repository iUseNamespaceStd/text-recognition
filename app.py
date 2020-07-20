import os
from flask import Flask, render_template, request
from ocr import ocr

UPLOADS = '/static/'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

def allowed_file(filename):
        return  '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/')
# def index():
#         return render_template('upload.html')

@app.route('/', methods=['GET', 'POST'])
def upload():
      return render_template('upload.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
        if request.method == 'POST':
                if 'file' not in request.files:
                        return render_template('upload.html', msg='No file selected')
                file = request.files['file']

                if file.filename == '':
                        return render_template('upload.html', msg='No file selected')

                if file and allowed_file(file.filename):
                        extracted_text = ocr(file)

                        return render_template('submit.html', msg='Success', 
                                                extracted_text=extracted_text,
                                                img_src = UPLOADS + file.filename)
        
        elif request.method == 'GET':
                return render_template('submit.html')      

if __name__ == '__main__':
    app.run(debug=True)