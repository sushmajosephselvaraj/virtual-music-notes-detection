# Virtual Musical Note Detection 🎵

This project turns your hand gestures into musical notes using your webcam.

## Features
- Detects hand gestures with **cvzone** (MediaPipe backend).
- Plays notes (C, D, E, F, G, A, B) depending on number of fingers raised.
- Simple, fun, and works in real-time.

## Setup
```bash
pip install -r requirements.txt
```

## Run
```bash
python main.py
```

Raise:
- 1 finger → C
- 2 fingers → D
- 3 fingers → E
- 4 fingers → F
- 5 fingers → G
(All 6–7 fingers mapped if detected)
