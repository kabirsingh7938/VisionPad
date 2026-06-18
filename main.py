import cv2
import mediapipe as mp
import pyautogui
import time

pyautogui.PAUSE = 0

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)

current_action = "NONE"

# Gesture stability
last_detected_gesture = "NONE"
gesture_frames = 0
REQUIRED_FRAMES = 2

# Controller state
controller_enabled = True

# FPS
prev_time = time.time()

while True:
    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    raw_gesture = "NONE"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            landmarks = hand_landmarks.landmark

            fingers_up = 0

            # Index
            if landmarks[8].y < landmarks[6].y:
                fingers_up += 1

            # Middle
            if landmarks[12].y < landmarks[10].y:
                fingers_up += 1

            # Ring
            if landmarks[16].y < landmarks[14].y:
                fingers_up += 1

            # Pinky
            if landmarks[20].y < landmarks[18].y:
                fingers_up += 1

            # Thumb
            if landmarks[4].x < landmarks[3].x:
                fingers_up += 1

            if fingers_up >= 4:
                raw_gesture = "PALM"

            elif fingers_up <= 1:
                raw_gesture = "FIST"

            else:
                raw_gesture = "NEUTRAL"

    # Gesture Stabilization

    if raw_gesture == last_detected_gesture:
        gesture_frames += 1
    else:
        last_detected_gesture = raw_gesture
        gesture_frames = 1

    stable_gesture = "WAITING"

    if gesture_frames >= REQUIRED_FRAMES:
        stable_gesture = raw_gesture

    # Action Mapping

    action = "NONE"

    if controller_enabled:

        if stable_gesture == "PALM":
            action = "BRAKE"

        elif stable_gesture == "FIST":
            action = "ACCELERATE"

    # Keyboard Control

    if action != current_action:

        pyautogui.keyUp('left')
        pyautogui.keyUp('right')

        if action == "BRAKE":
            pyautogui.keyDown('left')

        elif action == "ACCELERATE":
            pyautogui.keyDown('right')

        current_action = action

    # FPS

    current_time = time.time()
    fps = int(1 / (current_time - prev_time))
    prev_time = current_time

    # UI

    status = "ON" if controller_enabled else "OFF"

    cv2.putText(
        frame,
        f"Controller: {status}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0) if controller_enabled else (0, 0, 255),
        2
    )

    cv2.putText(
        frame,
        f"Gesture: {stable_gesture}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Action: {action}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"FPS: {fps}",
        (20, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 0, 255),
        2
    )

    cv2.putText(
        frame,
        "T = Toggle Controller",
        (20, 200),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (200, 200, 200),
        2
    )

    cv2.putText(
        frame,
        "Q = Quit",
        (20, 235),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (200, 200, 200),
        2
    )

    cv2.imshow("VisionPad Lite", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('t'):
        controller_enabled = not controller_enabled

        pyautogui.keyUp('left')
        pyautogui.keyUp('right')
        current_action = "NONE"

    if key == ord('q'):
        break

    if cv2.getWindowProperty("VisionPad Lite", cv2.WND_PROP_VISIBLE) < 1:
        break

# Safety release
pyautogui.keyUp('left')
pyautogui.keyUp('right')

cap.release()
cv2.destroyAllWindows()