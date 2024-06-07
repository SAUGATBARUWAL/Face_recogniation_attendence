import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
import face_recognition

def take_attendance():
    # Load the trained model and label data
    with open('data/names.pkl', 'rb') as w:
        LABELS = pickle.load(w)
    with open('data/face_encodings.pkl', 'rb') as f:
        ENCODINGS = pickle.load(f)

    print('Number of Face Encodings Loaded:', len(ENCODINGS))

    video = cv2.VideoCapture(0)

    COL_NAMES = ['NAME', 'TIME', 'STATUS']  # Add 'STATUS' to the column names

    # Check file existence before entering the loop
    ts = time.time()
    date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
    exist = os.path.isfile(f"Attendance/Attendance_{date}.csv")

    while True:
        ret, frame = video.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Find all face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Initialize attendance list
        attendance = []

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            output = "Unknown"

            # Compare face encoding with stored encodings
            matches = face_recognition.compare_faces(ENCODINGS, face_encoding)
            if True in matches:
                first_match_index = matches.index(True)
                output = LABELS[first_match_index]

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1)
            cv2.rectangle(frame, (left, top), (right, top + 20), (50, 50, 255), -1)
            cv2.putText(frame, output, (left, top + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Append to attendance list
            attendance.append([output, datetime.fromtimestamp(time.time()).strftime("%H:%M:%S"), 'Present'])  # Add 'Present' to the attendance record

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)

        if key == ord('o'):
            if exist:
                with open(f"Attendance/Attendance_{date}.csv", "a") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(attendance)  # Write all attendance records at once
            else:
                with open(f"Attendance/Attendance_{date}.csv", "a") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(COL_NAMES)
                    writer.writerows(attendance)

        if key == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    take_attendance()
