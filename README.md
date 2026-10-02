# AI Fitness Trainer using MediaPipe

A local webcam application that uses MediaPipe Pose landmarks to count exercise repetitions and display form feedback. OpenCV handles camera frames, and Streamlit provides the interface.

The app supports **squats, push-ups, and lunges**. Repetition counting and form feedback use joint angles and fixed rules; no custom model training is required.

## Features

- Live webcam view with a pose skeleton, repetition count, and joint angle.
- Separate exercise validators for squats, push-ups, and lunges.
- Feedback when a pose is missing or an exercise rule is triggered.
- Workout totals and a simple calorie estimate of 0.5 kcal per repetition.
- Camera selection for computers with more than one video device.

## Setup and run

Use **64-bit Python 3.11** and a webcam connected to the computer running the application. The pinned MediaPipe release provides Python 3.11 wheels; a newer Python version may not install these dependencies.

Clone the repository:

```bash
git clone https://github.com/Muhammad-Huzifa/ai-fitness-trainer.git
cd ai-fitness-trainer
```

### Windows Command Prompt

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

### Git Bash on Windows

```bash
py -3.11 -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

### Linux or macOS

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) if the browser does not open automatically.

## Use the app

1. Select an exercise.
2. Leave **Camera index** at `0` for the default webcam, or try `1` for another camera.
3. Keep your full body visible with clear lighting, then check **Start workout**.
4. Complete the bending and extension phases to count a repetition.
5. Uncheck **Start workout** to stop. A new run starts the workout totals at zero.

The camera belongs to the computer running Python. Hosting the app on a remote server does not give it access to a visitor's browser camera.

## Project organization

| Path | Purpose |
| --- | --- |
| `app.py` | Streamlit interface, webcam capture, and pose rendering |
| `modules/fitness_coach.py` | Workout state and exercise analysis |
| `modules/pose_analyzer.py` | Two-dimensional joint-angle calculations |
| `modules/rep_counter.py` | Repetition counting across bending and extension phases |
| `exercises/squats.py` | Squat rules and key-angle selection |
| `exercises/pushups.py` | Push-up rules and key-angle selection |
| `exercises/lunges.py` | Lunge rules and key-angle selection |
| `tests/` | Geometry, workout logic, and camera cleanup checks with mocked I/O |
| `docs/` | Architecture, development commands, and troubleshooting |
| `requirements.txt` | Pinned application dependencies |
| `.python-version` | Python version for tools that support this file |

## Useful commands

Run these commands from the repository root with the virtual environment active.

| Task | Command |
| --- | --- |
| Start the application | `python -m streamlit run app.py` |
| Use another port | `python -m streamlit run app.py --server.port 8502` |
| Run the logic checks | `python -m unittest discover -s tests -v` |
| Check installed dependencies | `python -m pip check` |
| View local changes | `git status` |

## Documentation

- [Architecture and counting rules](docs/architecture.md)
- [Development and troubleshooting](docs/development.md)

## Current limitations

Joint angles are measured in the image plane, so camera placement and occlusion affect the results. Form rules use fixed thresholds and some horizontal landmark comparisons that depend on viewing direction. A frame with no triggered rule does not establish that an exercise was performed correctly. The calorie total is a fixed estimate, not a measurement of energy expenditure.

## Author

[Muhammad Huzifa](https://github.com/Muhammad-Huzifa)

## References

- [MediaPipe 0.10.8 release and supported wheels](https://pypi.org/project/mediapipe/0.10.8/)
- [OpenCV package installation guidance](https://pypi.org/project/opencv-contrib-python/4.8.1.78/)
- [Running a Streamlit application](https://docs.streamlit.io/develop/concepts/architecture/run-your-app)
