import cv2
from deepface import DeepFace
import numpy as np
import os

# ------------------ Initialization ------------------

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Camera
cap = cv2.VideoCapture(0)

CAP_WIDTH = 1280
CAP_HEIGHT = 720

cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAP_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAP_HEIGHT)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

print("Press 'c' to capture image")
print("Press 'q' to quit")

# ------------------ Image Save Folder ------------------

save_folder = r"E:\Facial-Emotion-Recognition\Facial-Emotion-Recognition-main\Facial-Emotion-Recognition-main\Images"

os.makedirs(save_folder, exist_ok=True)

image_count = 0

# ------------------ Analysis Text ------------------

analysis_text = {
    "Emotion": "Detecting...",
    "Gender": "Detecting...",
    "Age": "Detecting...",
    "Race": "Detecting..."
}

# ------------------ Main Loop ------------------

while True:

    ret, frame = cap.read()

    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

    faces = face_cascade.detectMultiScale(
        gray_frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    face_crop = None

    for i, (x, y, w, h) in enumerate(faces):

        # Save face crop
        face_crop = frame[y:y+h, x:x+w]

        if i == 0:

            face_roi = rgb_frame[y:y+h, x:x+w]

            if face_roi.size > 0:

                try:

                    result = DeepFace.analyze(
                        face_roi,
                        actions=['emotion', 'age', 'gender', 'race'],
                        enforce_detection=False
                    )

                    analysis = result[0]

                    analysis_text["Emotion"] = analysis["dominant_emotion"].capitalize()
                    analysis_text["Gender"] = analysis["dominant_gender"].capitalize()
                    analysis_text["Age"] = str(analysis["age"])
                    analysis_text["Race"] = analysis["dominant_race"].capitalize()

                except:
                    pass

        # Draw Rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

    # ------------------ Display Analysis ------------------

    font = cv2.FONT_HERSHEY_SIMPLEX

    y = 30

    for key_name in analysis_text:

        text = f"{key_name}: {analysis_text[key_name]}"

        cv2.putText(frame,
                    text,
                    (10, y),
                    font,
                    0.8,
                    (255,255,255),
                    2)

        y += 30

    # Resize window
    display_frame = cv2.resize(frame, (600, 600))

    cv2.imshow("Real-Time DeepFace Analysis", display_frame)

    key = cv2.waitKey(1) & 0xFF

    # ------------------ Save Image ------------------

    if key == ord('c'):

        filename = os.path.join(save_folder, f"image_{image_count}.jpg")

        # Save the full frame
        cv2.imwrite(filename, frame)

        # Uncomment the following lines if you want to save ONLY the face
        #
        # if face_crop is not None:
        #     cv2.imwrite(filename, face_crop)

        print(f"Saved: {filename}")

        image_count += 1

    # ------------------ Quit ------------------

    elif key == ord('q'):
        break

# ------------------ Cleanup ------------------

cap.release()
cv2.destroyAllWindows()