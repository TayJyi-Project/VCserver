import os
import string
import pathlib
import youtube_dl
import subprocess
from flask import Flask, request, make_response, send_file, send_from_directory
from flask_cors import CORS, cross_origin

app = Flask(__name__)
# fix the encode of Chinese letters in json format
# app.config['JSON_AS_ASCII'] = False

@app.route("/", methods = ['GET', 'POST'])
def main():
  if request.method == 'POST':
    return ''
  else:
    return 'Bonjour'

@app.route("/upload", methods = ['POST'])
def upload():

  file = request.files['file']
  uid = request.form['uid']
  tid = request.form['tid']
  fid = request.form['fid']
  if not file:
    return 'FileNotRecievedError'
  # for Obsessive-Compulsive Disorder friend
  # if uid == '113165926150600630335':
    # uid = 'lu'

  filename = "../storage/" + uid + "/" + tid + "/src/"
  # Create the directory if not exists, do nothing while exists
  pathlib.Path(filename).mkdir(parents = True, exist_ok = True)
  filepath = os.path.join(filename)
  ftemp = 'temp.wav'
  fsave = str(fid).zfill(4) + '.wav'
  file.save(filepath + ftemp)
  subprocess.call(['ffmpeg', '-y', '-i', filepath + ftemp, filepath + fsave])
  return 'SuccessUploadFile'


@app.route("/convert", methods = ['POST'])
def convert():

  file = request.files['file']
  uid = request.form['uid']
  tid = request.form['tid']
  if not file:
    return 'FileNotRecievedError'
  # for Obsessive-Compulsive Disorder friend
  # if uid == '113165926150600630335':
    # uid = 'lu'

  filepath = "../storage/" + uid
  # sprocketPath = '../../sprocket/example/onServer.py'
  sprocketPath = '../sprocket/example/onServer.py'
  ftemp = '/tempaudio.wav'
  fconvert = '/tobeconvert.wav'
  freturn = '/afterconvert.wav'

  pathlib.Path(filepath).mkdir(parents = True, exist_ok = True)
  file.save(os.path.join(filepath) + ftemp)
  # If overwrites to 'tobeconvert.wav' will cause unknown error
  subprocess.call(['ffmpeg', '-y', '-i', filepath + ftemp, filepath + fconvert])
  cmd = ['python3', sprocketPath, uid, tid]
  subprocess.Popen(cmd).wait()
  return filepath + freturn

@app.route("/download", methods = ['GET'])
def download():

  filename = request.args.get("filename")
  # return byte data ?
  # response = make_response(file.read())
  response = make_response(send_file(filename))
  response.headers['Content-Type'] = 'audio/wav'
  # response.headers['Content-Disposition'] = "attachment"
  return response


@app.route('/<path:dummy>', methods = ['POST', 'GET'])
def fallback(dummy):
  return 'Undefined Request..., bro, stop doing this...'

if __name__ == "__main__":
  # for production environment
  app.run(host="0.0.0.0", port="5001", debug=False)
  # for local testing
  # app.run(port=5001, debug=True)
