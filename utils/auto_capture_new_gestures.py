from app import pre_process_landmark, calc_landmark_list

import cv2 as cv
import copy
import csv
import mediapipe as mp
import itertools
from pathlib import Path

# === SETTINGS ===
gesture_id = 5   # pick the numeric ID for your new gesture (check keypoint_classifier_label.csv)
gesture_name = "PointLeft"  # for your own tracking
num_samples = 1500    # how many frames to collect

# Resolve csv_path relative to repo root (two levels up from this utils file)
# so the script works when run from any CWD.
csv_path = Path(__file__).resolve().parents[1] / "model" / "keypoint_classifier" / "keypoint.csv"

# === Mediapipe init ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
)
mp_drawing = mp.solutions.drawing_utils


# Camera preparation 
cap = cv.VideoCapture(1)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 540)

counter = 0

# Ensure parent directory exists
csv_path.parent.mkdir(parents=True, exist_ok=True)

with csv_path.open("a", newline="") as f:
    writer = csv.writer(f)

    while cap.isOpened() and counter < num_samples:

        # Camera capture #####################################################
        ret, image = cap.read()
        if not ret:
            break
        image = cv.flip(image, 1)  # Mirror display
        debug_image = copy.deepcopy(image)

        # Detection implementation #############################################################
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

         #  ####################################################################
        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                  results.multi_handedness):
     
                # Landmark calculation
                landmark_list = calc_landmark_list(debug_image, hand_landmarks)

                # Conversion to relative coordinates / normalized coordinates
                pre_processed_landmark_list = pre_process_landmark(
                    landmark_list)

                # Add gesture_id in front
                row = [gesture_id, *pre_processed_landmark_list]
                writer.writerow(row)

                counter += 1

                # Draw for feedback
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv.putText(image, f"Gesture: {gesture_name} ({counter}/{num_samples})",
                    (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv.imshow("Capture", image)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv.destroyAllWindows()
