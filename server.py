import os
import sys
import threading
import flask
from flask import Flask, request, jsonify, Response, render_template
from flask_cors import CORS
from werkzeug import secure_filename
import config
import logo_removal


# initialize flask server
app = Flask(__name__, static_folder='output', static_url_path='')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config["DEBUG"] = False
app.config['JSON_AS_ASCII'] = False

# index page here, just return some html
@app.route('/', methods=['GET'])
def index():
    return render_template(config.index_path)

@app.route('/api/file', methods=['POST'])
def cv_run():
    f = request.files['file']
    input_path = os.path.join(config.IMAGE_UPLOAD_PATH, secure_filename(f.filename))
    f.save(input_path)
    logo_removal.run(input_path)
#     return jsonify(status=200, file=out_file)

@app.route('/<path:filename>')  
def send_file(filename):  
    return send_from_directory(app.static_folder, filename)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
