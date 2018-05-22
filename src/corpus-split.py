import os
import re
import wave
import json
import random
import string
import random
import pathlib
import youtube_dl
from scipy.io import wavfile
from pydub import AudioSegment
from pydub.silence import split_on_silence
from os.path import join, dirname
# from watson_developer_cloud import SpeechToTextV1
# from watson_developer_cloud.websocket import RecognizeCallback

def nameGenerator(strlen = 20, chars = string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for char in range(strlen))

def audioDownload(url, audioFormat = 'wav', sampleRate = 44100):

    tempname = nameGenerator()
    filedir = '../storage/{0}'.format(tempname)
    filename = '{0}/{1}.{2}'.format(filedir, tempname, audioFormat)
    pathlib.Path(filedir).mkdir(parents = True, exist_ok = True)
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': audioFormat,
        }],
        'noplaylist': True,
        'writesubtitles': True,
        'subtitleslangs': ['zh-TW'],
        # this is a bug between youtube-dl and ffmpeg
        'outtmpl': filename+'%(ext)s'
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download( [url] )
    AudioSegment.from_wav(filename).set_channels(1).set_frame_rate(sampleRate).export(filename, format=audioFormat, parameters = ['-y'])
    # AudioSegment.from_file(filename).set_channels(1).set_frame_rate(sampleRate).export(filename, format=audioFormat, parameters = ['-y'])
    return tempname, filename, sampleRate, audioFormat

def splitBySubtitles(tempname, filename, sampleRate, audioFormat):
    
    chunkdir = filename.replace('{0}.{1}'.format(tempname, audioFormat), 'chunks/')
    pathlib.Path(chunkdir).mkdir(parents = True, exist_ok = True)
    with open(filename.replace('.{0}'.format(audioFormat), '.zh-TW.vtt')) as fp:
        lines = fp.readlines()
    audiosignals = AudioSegment.from_file(filename)
    x = audiosignals.get_array_of_samples()

    chunktimes = []
    chunkwords = []
    regexp1 = '\d+:\d+:\d+.\d+ --> \d+:\d+:\d+.\d+'
    regexp2 = '\d+\.?\d+'
    lazytag = False
    for line in lines:
        if re.search(regexp1, line):
            matches = re.findall(regexp2, line)
            timepts = [float(tp) for tp in matches]
            # pydub uses ms as calculate units...
            tstart = (timepts[0] * 3600 + timepts[1] * 60 + timepts[2] * 1) * 1000
            tend = (timepts[3] * 3600 + timepts[4] * 60 + timepts[5] * 1) * 1000

            chunktimes.append(audiosignals[tstart:tend])
            lazytag = True
        elif not re.search(regexp1, line) and lazytag is True:
            lazytag = False
            chunkwords.append(line)
        else:
            continue
  
    assert len(chunktimes) == len(chunkwords)
    for idx in range(len(chunktimes)):
        chunktimes[idx].export('{0}{1}.{2}'.format(chunkdir, str(idx).zfill(4), audioFormat), format = audioFormat)
    for idx in range(len(chunkwords)):
        with open('{0}{1}.txt'.format(chunkdir, str(idx).zfill(4)), 'w') as fp:
            fp.write(chunkwords[idx])


if __name__ == "__main__":

    tempname, filename, sampleRate, audioFormat = audioDownload('https://www.youtube.com/watch?v=N0zhdMwD2Z8')
    if(os.path.exists(filename.replace('.mp3', '.zh-TW.vtt'))):
        splitBySubtitles(tempname = tempname, filename = filename, sampleRate = sampleRate, audioFormat = audioFormat)
    else:
        pass