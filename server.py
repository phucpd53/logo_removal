import os
import sys
import threading
import flask
from flask import Flask, request, jsonify, Response, render_template
# from flask_cors import CORS
from werkzeug import secure_filename
import config
import logo_removal


# initialize flask server
app = Flask(__name__, static_folder='static', static_url_path='')
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# app.config["DEBUG"] = False
# app.config['JSON_AS_ASCII'] = False

# index page here, just return some html
@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/run', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['image']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'input', secure_filename(f.filename))
        f.save(file_path)
        logo_removal.run(file_path)
        return "OK"
        
    return None

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
