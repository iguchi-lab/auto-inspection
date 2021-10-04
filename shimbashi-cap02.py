import cv2
import datetime
import boto3
import time
import os
import json
import urllib.request

bucket_name = "shimbashi-meter-in"
s3 = boto3.resource('s3')

DEVICE_ID = [0, 2]

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

print('now start')
filepath = '/home/pi/meter-reader/shimbashi/' 
datetime_str= datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

for i, id in enumerate(DEVICE_ID):
    
    try:
        print('Capture ID = ' + str(id))
        cap = cv2.VideoCapture(id)
        ret, frame = cap.read()
        filename = datetime_str + '-' + str(i) + '.jpg'
    
        cv2.imwrite(filepath + filename, frame)
        time.sleep(5)
    
        print(filepath + filename)
        cap.release()

        s3.Bucket(bucket_name).upload_file(filepath + filename, str(i + 3) + '/' + filename)
        time.sleep(5)
        
        print('transported')
        os.remove(filepath + filename)
    
    except Exception as e:
        post_slack(e)
