
# Hand Tracking and Sound Playback Project

This project tracks hand movements using the MediaPipe library and plays corresponding sounds based on specific hand gestures. It integrates OpenCV for video capture, MediaPipe for hand landmark detection, and Pygame for sound playback.

## Features
- **Hand Tracking:** Detects both left and right hands in real-time using a webcam.
- **Gesture Recognition:** Plays different sounds based on the proximity of certain hand landmarks.
- **Async Processing:** Uses asyncio to handle hand tracking and sound playback efficiently.
- **Custom Sounds:** Each hand gesture is mapped to specific sounds for both left and right hands.

## Requirements
Make sure you have the following libraries installed:

```bash
pip install mediapipe opencv-python pygame numpy
```

## How it Works
1. **Landmark Detection:**
   - Tracks hand landmarks using MediaPipe.
   - Key landmarks are indexed as 4, 8, 12, 16, and 20.
   
2. **Gesture Recognition:**
   - Measures the distance between thumb (ID 4)=>thumb and other fingers landmarks.
   - If the thumb is close to a key landmark (e.g., ID 8, 12, 16, or 20), it plays a corresponding sound.
   
3. **Sound Playback:**
   - Plays custom sounds for each hand (left/right) when the gesture is recognized.
   - Implements a cooldown mechanism to avoid playing sounds too frequently.

## File Structure

- `main.py`: The main script containing the hand tracking logic.
- `./sounds/left/`: Directory for sounds triggered by the left hand.
- `./sounds/right/`: Directory for sounds triggered by the right hand.

## Running the Project
1. Clone or download the repository.
2. Ensure you have a working webcam.
3. Place your custom sound files in the respective `./sounds/left/` and `./sounds/right/` directories.
4. Run the script:

