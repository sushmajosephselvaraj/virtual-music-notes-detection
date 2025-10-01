import cv2
import mediapipe as mp
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load notes
notes = {
    1: "notes/C.wav",
    2: "notes/D.wav",
    3: "notes/E.wav",
    4: "notes/F.wav",
    5: "notes/G.wav",
    6: "notes/A.wav",
    7: "notes/B.wav"
}

sounds = {k: pygame.mixer.Sound(v) for k, v in notes.items()}

# Map count -> Note name
note_names = {
    1: "C",
    2: "D",
    3: "E",
    4: "F",
    5: "G",
    6: "A",
    7: "B"
}

# Mediapipe Hands setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)
print("Press 'q' to quit")

# ✅ Track last note played
last_note = None

def count_fingers(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    fingers = []
    landmarks = hand_landmarks.landmark

    # Thumb
    if landmarks[tips[0]].x < landmarks[tips[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for id in range(1, 5):
        if landmarks[tips[id]].y < landmarks[tips[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            count = count_fingers(hand_landmarks)

            if count in sounds:
                # ✅ Only play when finger count changes
                if last_note != count:
                    sounds[count].play()
                    last_note = count

                note_text = note_names[count]
            else:
                note_text = "None"
                last_note = None  # reset if no valid note

            cv2.putText(img, f"Note: {note_text}", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    cv2.imshow("Virtual Musical Note Detection", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
