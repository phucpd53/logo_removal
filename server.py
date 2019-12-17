import os
import sys
import threading
import flask
from flask import Flask, request, jsonify, Response, render_template
# from flask_cors import CORS
from werkzeug import secure_filename
from gevent.pywsgi import WSGIServer
import config
import logo_removal
import fake_run


# initialize flask server
app = Flask(__name__)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# app.config["DEBUG"] = False
# app.config['JSON_AS_ASCII'] = False

def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    return rv

# index page here, just return some html
@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['image']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'input', secure_filename(f.filename))
        f.save(file_path)
        # output_path = logo_removal.run(file_path)
        # return render_template('index.html', reconstructed=output_path)
        
        # return render_template("image.html", data=fake_run.run())
        return Response(stream_template('image.html', data=fake_run.run()))
        
    # return None

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()