import os
import math
import struct
import string
import pathlib
import youtube_dl
import subprocess
from pydub import AudioSegment
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
  response = make_response(send_file(filename, 'audio/wav'))
  # response.headers['Content-Type'] = 'audio/wav'
  # response.headers['Content-Disposition'] = "attachment"
  return response




@app.route("/m4dl", methods = ['GET'])
def testM4Download():

  retSize = 1024# return bytes
  if request.args.get("pid"):
    pageid = int(request.args.get("pid"))
  else:
    pageid = -1
  fpath = '../storage/cortex-m4/afterconvert.wav'
  if pageid == -1:

    with open(fpath, 'rb') as fp:
      temp = fp.read()
    print('pid is {}'.format(pageid))
    return 'loopCount:' + str(math.ceil(len(temp) / retSize))

  with open(fpath, 'rb') as fp:
    fp.seek(int(pageid) * retSize, 1)
    ret = fp.read(retSize)

  #print(type(ret))
  print(len(ret))
  print(ret)

  return bytes('byteData:', encoding="utf8") + (ret)

'''
@app.route("/m4ul", methods = ['POST'])
def testM4Post():

  if request.form:
    if request.form['msg']:
      msg = request.form['msg']
    else:
      msg = "your post is fucking empty no msg"
  else:
    msg = "your post is fucking empty"
  print(msg)
  return msg
  # pass
  # make sure post is workable first
'''


@app.route("/m4ul", methods = ['POST'])
def testM4Upload():

  batch_size = 1500 - 1 # according to m4
  tempPath = '../storage/cortex-m4/tempConvert.wav'
  realPath = '../storage/cortex-m4/tobeconvert.wav'
  convPath = '../storage/cortex-m4/afterconvert.wav'
  sprocketPath = '../sprocket/example/onServer.py'
  '''
  pid = int(request.form['pid']) if request.form.get('pid') else 0

  fpath = '../storage/cortex-m4/tobeconvert.wav'
  if pid == -1:
    with open(fpath, 'wb') as fp:
      pass
    return 'remove!'
  # json doesn't accept byte data
  '''

  bytedata = request.get_data()
  if bytedata == b'':
    return 'empty!'


  with open(tempPath, 'ab+') as fp:
    fp.write(bytedata)

  if len(bytedata) != batch_size:
    os.rename(tempPath, realPath)

    AudioSegment.from_wav(realPath).set_channels(1).export(realPath, format='wav', parameters = ['-y'])
    cmd = ['python3', sprocketPath, "cortex-m4", "kp3-16k"]
    subprocess.Popen(cmd).wait()
    AudioSegment.from_wav(convPath).set_channels(2).export(convPath, format='wav', parameters = ['-y'])

  return 'success'



@app.route('/<path:dummy>', methods = ['POST', 'GET'])
def fallback(dummy):
  return 'Undefined Request..., bro, stop doing this...'

if __name__ == "__main__":
  # for production environment
  app.run(host="0.0.0.0", port="5001", debug=False)
  # for local testing
  # app.run(port=5001, debug=True)
