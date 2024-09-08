import cv2
import numpy as np
import mediapipe as mp
from google.protobuf.json_format import MessageToDict
import pygame
import threading
import time
import asyncio

pygame.mixer.init()

IMPORTANT_LANDMARK_INDICES = [4, 8, 12, 16, 20]
COOLDOWN_DURATION = 0.3
SOUND_PATHS = {
    'Left': {
        8: './sounds/left/c.mp3',
        12: './sounds/left/d.mp3',
        16: './sounds/left/e.mp3',
        20: './sounds/left/f.mp3'
    },
    'Right': {
        8: './sounds/right/a.mp3',
        12: './sounds/right/b.mp3',
        16: './sounds/right/c.mp3',
        20: './sounds/right/g.mp3'
    }
}

mp_hands = mp.solutions.hands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75,
    max_num_hands=2
)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

last_played_times = {}

def euclidean_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def play_sound(path):
    sound = pygame.mixer.Sound(path)
    sound.play()

def play_sound_in_thread(path):
    threading.Thread(target=play_sound, args=(path,)).start()

async def process_hand_landmarks(hand_landmarks, hand_label, last_played_times, img):
    landmarks = [(int(point.x * img.shape[1]), int(point.y * img.shape[0])) for point in hand_landmarks.landmark]
    cv2.putText(img, f'{hand_label} Hand', (20 if hand_label == 'Left' else 460, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)

    for i in IMPORTANT_LANDMARK_INDICES:
        point = landmarks[i]
        cv2.circle(img, point, 10, (0, 255, 0), -1)
        cv2.putText(img, f"ID {i}", (point[0], point[1] + 15), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 255, 0), 1)
        
        if i == 4:
            for target_index in IMPORTANT_LANDMARK_INDICES[1:]:
                distance = euclidean_distance(landmarks[4], landmarks[target_index])
                if distance < 30:
                    cv2.putText(img, "Close", (landmarks[4][0], landmarks[4][1] + 15), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 255, 0), 1)
                    
                    current_time = time.time()
                    last_played_time = last_played_times.get(f"{hand_label}_{target_index}", 0)
                    
                    if current_time - last_played_time >= COOLDOWN_DURATION:
                        last_played_times[f"{hand_label}_{target_index}"] = current_time
                        sound_path = SOUND_PATHS[hand_label].get(target_index)
                        if sound_path:
                            print(f"Playing sound: {sound_path}")
                            play_sound_in_thread(sound_path)
    return last_played_times

async def main():
    global last_played_times
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
        
        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = mp_hands.process(img_rgb)

        if results.multi_hand_landmarks:
            tasks = []
            for idx, hand_handedness in enumerate(results.multi_handedness):
                label = MessageToDict(hand_handedness)['classification'][0]['label']
                hand_landmarks = results.multi_hand_landmarks[idx]

                tasks.append(process_hand_landmarks(hand_landmarks, label, last_played_times, img))
            
            if tasks:
                await asyncio.gather(*tasks)

        cv2.imshow('Hand Tracking', img)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
