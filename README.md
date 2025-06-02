🔍 Overview:
The Virtual AI Painter is a computer vision-based interactive drawing application that allows users to draw on screen in real-time using only hand gestures, without touching the mouse or screen. It uses a webcam, OpenCV, and a custom hand-tracking module built on MediaPipe, enabling natural, contactless interaction.

🛠️ Key Features:
Hand Gesture Recognition:
Detects and tracks hand landmarks (fingertips and joints) to determine which fingers are raised.

Drawing with Index Finger:
When the user raises only the index finger, the system enters "Drawing Mode". The fingertip acts like a virtual pen.

Color & Tool Selection:
When both the index and middle fingers are raised, the system enters "Selection Mode". Users can hover over colored buttons (in the top header bar) to change the drawing color (e.g., Yellow, Dark Blue, Green) or activate the eraser.

Eraser Functionality:
When the "Eraser" is selected, the user can erase previous drawings by moving the index finger, like a digital whiteboard.

Canvas and Overlay Blending:
The drawing is done on a separate canvas image which is blended with the live webcam feed, allowing the drawing to persist even when the hand is not moving.

🧠 Technologies Used:
Python

OpenCV – for video capture and image processing

MediaPipe (via custom HTModule) – for real-time hand tracking

NumPy – for canvas manipulation

CV2 GUI – for display and interaction

🎯 Applications:
Contactless digital whiteboards

Virtual classrooms or live presentations

Fun drawing games for kids

Human-computer interaction (HCI) experiments

Assistive tech for touch-free input
