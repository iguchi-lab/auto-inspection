import pyaudio
import wave
import datetime
import boto3
import time
import os
import json
import urllib.request

bucket_name = "shimbashi-sound-in"
s3 = boto3.resource('s3')

DEVICE_ID = [0, 1, 2]

def post_slack(message):
    send_data ={
        "username": "meter-reader",
        "text": message
    }
        
    send_text = "payload=" + json.dumps(send_data)
    request = urllib.request.Request(
        "https://hooks.slack.com/services/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",
        data=send_text.encode("utf-8"),
        method="POST"
    )
    with urllib.request.urlopen(request) as response:
        response_boday = response.read().decode("utf-8")

def record_snd(id, filename):

    RECORD_SECONDS = 5

    p = pyaudio.PyAudio()

    stream = p.open(
        format = pyaudio.paInt16,
        channels = 1,
        rate = 44100,
        input = True,
        input_device_index = id,
        frames_per_buffer = 1024 * 4
    )

    snd_frame = []

    print('recording')
    for i in range(0, int(44100 / (1024 * 4) * RECORD_SECONDS)):
        data = stream.read(1024 * 4)
        snd_frame.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(snd_frame))
    wf.close()

    return

print('now start')
filepath = '/home/pi/meter-reader/shimbashi/'
datetime_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

for i, id in enumerate(DEVICE_ID):

    try:

        print('Capture ID = ' + str(id))
        filename = datetime_str + '-' + str(i) + '.wav'
        record_snd(id, filepath + filename)
        time.sleep(5)
    
        print(filepath + filename)
        s3.Bucket(bucket_name).upload_file(filepath + filename, str(i) + '/' + filename)
        time.sleep(5)
        
        print('transported')
        os.remove(filepath + filename)
    
    except Exception as e:
        post_slack(e)
