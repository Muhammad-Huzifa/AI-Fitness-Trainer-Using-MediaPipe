# 🏋️ AI Fitness Trainer using MediaPipe

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Pose-orange)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)

An AI-powered personal trainer that uses **Computer Vision** to analyze exercise form, count repetitions, and provide real-time feedback. Built with **Python**, **OpenCV**, and **MediaPipe**.

## 🚀 Features
* **Real-time Pose Estimation:** Tracks body landmarks with high accuracy.
* **Automatic Rep Counting:** Counts reps for Squats, Pushups, and Lunges.
* **Form Analysis:** Calculates joint angles to ensure correct posture.
* **Visual Feedback:** Overlays skeleton and rep counter on the video feed.

## 📂 Project Structure
```bash
├── exercises/          # Logic for specific exercises
│   ├── lunges.py
│   ├── pushups.py
│   └── squats.py
├── modules/            # Core modules for pose detection
│   ├── pose_analyzer.py
│   └── rep_counter.py
├── utils/              # Helper functions
├── app.py              # Main application entry point
├── requirements.txt    # Dependencies
└── README.md
