import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime, timedelta


cred = credentials.Certificate("your_certificate_realtimefirebase.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'url_for_your_database',
    'storageBucket': 'url_for_your_storageBucket'
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread("resources/background.png")

folderModesPath = "resources/Modes"
modePathList = os.listdir(folderModesPath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModesPath, path)))

    
with open("EncodeFile.p", "rb") as f:
    encodeListKnowwithIds = pickle.load(f)
    encodelistknow, face_idList = encodeListKnowwithIds
    
counter = 0
modetype = 0
imgPerson = []
person_infos_loaded = {}
image_person_loaded = {}
last_time_loaded = {}
while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
    
    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44+633, 808:808+414] = imgModeList[modetype]
    
    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodelistknow, encodeFace)
            faceDis = face_recognition.face_distance(encodelistknow, encodeFace)

            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = x1 + 55, y1 + 162, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

                id = face_idList[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modetype = 1

        if counter != 0:
            if counter == 1:
                #secondsElapsed = 0
                if (id not in person_infos_loaded) or ((datetime.now() - last_time_loaded[id]).total_seconds() >= 60):
                    person_info = db.reference(f"Students/{id}").get()
                    print(person_info)
                    person_infos_loaded[id] = person_info
                    last_time_loaded[id] = datetime.strptime(person_info["last_attendance_time"], "%Y-%m-%d %H:%M:%S")
                                                             
                    blob = bucket.get_blob(f"images/{id}.jpg")
                    if blob is not None:
                        array = np.frombuffer(blob.download_as_string(), dtype=np.uint8)
                        imgPerson = cv2.imdecode(array, cv2.COLOR_BGRA2RGB)
                        image_person_loaded[id] = imgPerson
                    
                else:
                    person_info = person_infos_loaded[id]
                    imgPerson = image_person_loaded[id]
                    

                # datetimeObject = datetime.strptime(person_info["last_attendance_time"], "%Y-%m-%d %H:%M:%S")
                datetimeObject = last_time_loaded[id]
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                    
                if secondsElapsed >= 60:
                    ref = db.reference(f"Students/{id}")
                    person_info["total_attendance"] += 1
                    ref.child("total_attendance").set(person_info["total_attendance"])
                    ref.child("last_attendance_time").set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    tmp_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    last_time_loaded[id] = datetime.strptime(tmp_time, "%Y-%m-%d %H:%M:%S")
                else:
                    modetype = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modetype]

            if modetype !=3:
                if 10 < counter < 20:
                    modetype = 2
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modetype]

                if counter <= 10:
                    cv2.putText(imgBackground, str(person_info['total_attendance']), (861, 125),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(person_info['major']), (1006, 550),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(person_info['standing']), (910, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(person_info['year']), (1025, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(person_info['starting_year']), (1125, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(person_info['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(person_info['name']), (808 + offset, 445),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imgPerson_resized = cv2.resize(imgPerson, (216, 216))
                    imgBackground[175:175 + 216, 909:909 + 216] = imgPerson_resized

                counter +=1
                
                if counter >= 20:
                    counter = 0
                    modetype = 0
                    person_info = []
                    imgPerson = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modetype]
    else:
        modetype = 0
        counter = 0

    cv2.imshow("Face Attendance", imgBackground)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
        