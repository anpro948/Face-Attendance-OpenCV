# Simple Face Attendance System with OpenCV Library and Firebase

This project is a Simple Face Attendance System that leverages the power of OpenCV for face recognition and Firebase for real-time database storage of personal information.

This project is guided by Murtaza Hassan. You can watch the tutorial [here](https://www.youtube.com/watch?v=iBomaK2ARyI). If you're interested, you can visit his [website](https://www.computervision.zone/), which includes various interesting courses and projects related to computer vision.

## Features

- **Face Recognition:** Uses OpenCV Library to accurately identify individuals' faces.

- **Real-time Database:** Stores, updates, and modifies personal information and attendance records in Firebase.

- **Automatic Attendance Tracking:** Automatically records attendance when recognized faces are detected, simplifying the attendance process.

- **Secure and Scalable:** Firebase's security features protect sensitive data, and the system can be scaled to accommodate various attendance management needs.

- **Code Optimization**: If you take a look at my `main.py` file, you'll notice that I've used variables like `person_infos_loaded` and `last_time_loaded` to optimize the number of requests to Firebase (this is a small improvement over the code in this tutorial).

## Face Attendance System Diagram
![Face Attendance Diagram](https://github.com/anpro948/Face-Attendance-OpenCV/assets/39051090/6358a670-25a4-44ba-a09b-70964b72b4ba)
