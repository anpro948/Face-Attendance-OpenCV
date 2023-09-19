import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("your_certificate_realtimefirebase.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'url_for_your_database',
    'storageBucket': 'url_for_your_storageBucket'
})

ref = db.reference('Students')

data = {
    "2":
    {
        "name": "Son Tung MTP",
        "major": "Singer",
        "starting_year": "Not Defined",
        "total_attendance": 3,
        "standing": "F",
        "year": "Not Defined",
        "last_attendance_time": "2022-9-11 00:43:33"
    },
    "3":
    {
        "name": "Teacher Three",
        "major": "Streamer",
        "starting_year": "Not Defined",
        "total_attendance": 4,
        "standing": "A",
        "year": "Not Defined",
        "last_attendance_time": "2022-10-11 00:43:33"
    }

}

for key, value in data.items():
    ref.child(key).set(value)