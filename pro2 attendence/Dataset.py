import cv2
import os
import pickle
import numpy as np
import face_recognition
import sys

# Create data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    print("No name provided.")
    sys.exit(1)

print("Collecting data. Please ensure your face is well-lit and centered.")

video = cv2.VideoCapture(0)
face_encodings = []

while True:
    ret, frame = video.read()  # Reading the images
    if not ret:
        break

    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    if face_locations:
        new_encodings = face_recognition.face_encodings(frame, face_locations)
        for new_encoding in new_encodings:
            if len(face_encodings) < 60:  # Collect up to 60 face encodings
                face_encodings.append(new_encoding)
                cv2.putText(frame, f"Collected: {len(face_encodings)}/60", org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 0), thickness=1)
            else:
                cv2.putText(frame, "Collection Complete!", org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 0), thickness=2)

    cv2.imshow("Register", frame)
    k = cv2.waitKey(1)
    if len(face_encodings) == 60:  # Stop when 60 face encodings are collected
        break

video.release()
cv2.destroyAllWindows()

# Saving the face encodings to a file
face_encodings = np.array(face_encodings)

if 'names.pkl' not in os.listdir('data/'):
    names = [name] * len(face_encodings)  # Save name only
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)
else:
    with open('data/names.pkl', 'rb') as f:
        names = pickle.load(f)
    names.extend([name] * len(face_encodings))  # Save name only
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)

if 'face_encodings.pkl' not in os.listdir('data/'):
    with open('data/face_encodings.pkl', 'wb') as f:
        pickle.dump(face_encodings, f)
else:
    with open('data/face_encodings.pkl', 'rb') as f:
        saved_face_encodings = pickle.load(f)

    # Ensure the dimensions match before concatenating
    if saved_face_encodings.shape[1] == face_encodings.shape[1]:
        face_encodings = np.append(saved_face_encodings, face_encodings, axis=0)
        with open('data/face_encodings.pkl', 'wb') as f:
            pickle.dump(face_encodings, f)
    else:
        print("Error: Dimension mismatch between saved_face_encodings and face_encodings. Cannot concatenate.")
