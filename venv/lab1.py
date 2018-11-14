from flask import Flask
from flask import request
from flask import Response
from flask import safe_join
from flask import send_from_directory
from flask import render_template
from werkzeug.utils import secure_filename
from flask import redirect, url_for
import json
import os

app = Flask(__name__)

DIR = os.path.dirname(os.path.realpath(__file__))
STORAGE= safe_join(DIR, 'storage')

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = safe_join(DIR,'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#UPLOAD_FOLDER = '/uploads'


@app.errorhandler(404)
def not_found_error(error):
   return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')




@app.route('/download', methods=['GET'])
def download_file():
    path = request.files['file']
    filePpath = safe_join(STORAGE, path)

    return send_from_directory('storage', path, as_attachment=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
@app.route('/uploads', methods=['GET'])
def uploaded_file():
    path = request.args['file']
    return send_from_directory('uploads',path,as_attachment=True)

@app.route('/up', methods=['GET', 'POST'])
def uploadd_file():
    if request.method == 'POST':
        f = request.args['the_file']
        f.save('uploads/uploaded_file.txt')



if __name__== '__main__':
    app.run()
