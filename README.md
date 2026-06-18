# VisionPad 🎮

Control games using only your hand and a webcam.

VisionPad is a computer vision-based virtual game controller that uses real-time hand gesture recognition to convert hand movements into keyboard inputs.

Built with:

* Python
* OpenCV
* MediaPipe
* PyAutoGUI

## Features

* Real-time hand tracking
* Palm and fist gesture recognition
* Controller-free gameplay
* FPS monitoring
* Toggle controller ON/OFF
* Standalone Windows executable

## Controls // IMPORTANT

| Gesture | Action          |
|         |                 |
| ✊ Fist  | Accelerate      |
| ✋ Palm  | Brake / Reverse |

| Key | Function                 
|     |  
| T   | Toggle Controller ON/OFF 
| Q   | Quit                     

## Requirements

* Windows 10/11
* Webcam

## Tech Stack

* Python
* OpenCV
* MediaPipe
* PyAutoGUI
* PyInstaller

## How It Works

1. Webcam captures hand movements.
2. MediaPipe detects hand landmarks.
3. VisionPad classifies gestures.
4. Gestures are converted into keyboard inputs.
5. Games respond as if a physical controller is being used.

## Future Plans

* Air steering
* Floating HUD
* Custom gesture mapping
* Multi-game support
* Calibration mode

## Author

Kabir Singh 
