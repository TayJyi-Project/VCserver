import os
import string
import pathlib
import youtube_dl
from flask import Flask, request, make_response, send_file, send_from_directory
from flask_cors import CORS, cross_origin

app = Flask(__name__)
# fix the encode of Chinese letters in json format
# app.config['JSON_AS_ASCII'] = False

@app.route("/", methods = ['GET', 'POST'])
def hello():
  if request.method == 'POST':
    return "Bro, don't do this...!"
  else:
    return "Hello World!"

@app.route("/upload", methods = ['POST'])
def upload():
  file = request.files['file']
  uid = request.form['uid'] # user_token
  tid = request.form['tid'] # target_token
  fid = request.form['fid'] # file_id
  if file:
    filename = "../storage/" + uid + "/" + tid + "/"
    # Create the directory if not exists, do nothing while exists
    pathlib.Path(filename).mkdir(parents=True, exist_ok=True)
    file.save(os.path.join(filename) + str(fid).zfill(4) + ".wav")
    return "1"
  return "0"

@app.route("/convert", methods = ['POST'])
def convert():
  file = request.files['file']
  uid = request.form['uid'] # user_token
  tid = request.form['tid'] # target_token
  fid = 'tobeconvert.wav'
  if file:
    filename = "../storage/" + uid + "/"
    # Create the directory if not exists, do nothing while exists
    pathlib.Path(filename).mkdir(parents=True, exist_ok=True)
    file.save(os.path.join(filename) + fid)
    return filename + fid
  return "0"

"""
# Directly return byte data, put it into memory
def convert():
  file = request.files['file']
  response = make_response(file.read())
  response.headers['Content-Type'] = 'audio/wav'
  return response
"""

@app.route("/download", methods = ['GET'])
def download():
  filename = request.args.get("filename")
  response = make_response(send_file(filename))
  response.headers['Content-Type'] = 'audio/wav'
  #response.headers['Content-Disposition'] = "attachment"
  return response

@app.route('/<path:dummy>', methods = ['POST', 'GET'])
def fallback(dummy):
  return "Bro, don't do this...!"

if __name__ == "__main__":
  app.run(host="0.0.0.0", port="5001", debug=False)
  # run the above for local testing, and the below for production environment
  # app.run(port=5001, debug=True)
