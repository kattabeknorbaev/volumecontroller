import cv2
import mediapipe as mp
import numpy as np
import pyautogui

# ----------------------------
# MEDIAPIPE SETUP
# ----------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# ----------------------------
# FIST DETECTION HELPER
# ----------------------------
def is_fist(hand_lms):
    # Tips: 8, 12, 16, 20 | Knuckles: 6, 10, 14, 18
    tips = [8, 12, 16, 20]
    knuckles = [6, 10, 14, 18]
    closed_fingers = 0
    for t, k in zip(tips, knuckles):
        # In MediaPipe, Y increases downward. Tip Y > Knuckle Y means finger is folded.
        if hand_lms.landmark[t].y > hand_lms.landmark[k].y:
            closed_fingers += 1
    return closed_fingers == 4

# ----------------------------
# WEBCAM SETUP
# ----------------------------
cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
prev_y = None  # Track movement instead of absolute position

print("🚀 VolumeKnuckle ACTIVE: Make a FIST and move it UP/DOWN.")

# ----------------------------
# MAIN LOOP
# ----------------------------
while True:
    success, img = cap.read()
    if not success: break

    img = cv2.flip(img, 1)
    h, w, c = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    status = "Waiting for Fist..."
    color = (200, 200, 200)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            
            # 1. CHECK IF IT'S A FIST
            if is_fist(handLms):
                status = "FIST DETECTED: Control Active"
                color = (0, 255, 0)
                
                # 2. TRACK MOVEMENT (Landmark 0 is the wrist)
                current_y = handLms.landmark[0].y
                
                if prev_y is not None:
                    diff = prev_y - current_y # Moving UP means Y decreases, so diff is positive
                    
                    # 3. APPLY VOLUME (Sensitivity Threshold)
                    if diff > 0.03: # Moved Up
                        pyautogui.press("volumeup")
                        prev_y = current_y # Update anchor
                    elif diff < -0.03: # Moved Down
                        pyautogui.press("volumedown")
                        prev_y = current_y
                else:
                    prev_y = current_y
            else:
                # Reset tracking when hand is open so volume doesn't jump
                prev_y = None

    # ----------------------------
    # UI OVERLAY
    # ----------------------------
    cv2.putText(img, status, (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    cv2.putText(img, 'Q to Quit', (w-120, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

    cv2.imshow("VolumeKnuckle - DAY 3", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()