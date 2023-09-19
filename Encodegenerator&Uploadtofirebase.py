import cv2
import os
import face_recognition
import pickle

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("your_certificate_realtimefirebase.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'url_for_your_database',
    'storageBucket': 'url_for_your_storageBucket'
})

ref = db.reference('Students')


facePath = "images"
facePathList = os.listdir(facePath)
faceList = []
face_idList = []
for path in facePathList:
    faceList.append(cv2.imread(os.path.join(facePath, path)))
    face_idList.append(os.path.splitext(path)[0])
    
    fileName = f'{facePath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    
    
def findEncodings(faceList):
    encodeList = []
    for img in faceList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodelistknow = findEncodings(faceList)

encodelistknowwithId = [encodelistknow, face_idList]

with open('EncodeFile.p', 'wb') as f:
    pickle.dump(encodelistknowwithId, f)