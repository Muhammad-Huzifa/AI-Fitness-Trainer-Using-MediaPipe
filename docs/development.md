# Development and troubleshooting

Start with the environment setup in the [README](../README.md). Run commands from the repository root with the virtual environment active.

## Check a change

```bash
python -m unittest discover -s tests -v
python -m compileall -q app.py modules exercises tests
python -m pip check
```

The tests cover joint geometry, complete repetition cycles, repeated frames, and frames without a pose. Camera tests mock OpenCV, MediaPipe, and Streamlit to check resource cleanup and tracking messages. They do not validate live camera capture, MediaPipe tracking accuracy, or exercise-form accuracy.

After changing the camera or interface code, run the app locally and check:

1. Starting and stopping a workout releases the camera so another run can use it.
2. Moving out of view displays **No pose detected**, and the repetition total stops changing.
3. Squats, push-ups, and lunges each complete a repetition cycle without counting stationary frames twice.
4. Disconnecting or selecting an unavailable camera produces a clear message.

## Git commands for documentation changes

```bash
git switch main
git pull --ff-only
git switch -c docs/improve-readme
```

Edit the files, then review and commit them:

```bash
git status
git diff
git add README.md docs
git commit -m "Improve project documentation"
git push -u origin docs/improve-readme
```

Open a pull request from that branch to `main` on GitHub. Keep exercise-rule changes separate from documentation changes so their effect on counts and feedback is clear.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| MediaPipe cannot be installed | Use 64-bit Python 3.11 and create a fresh virtual environment. The pinned release has no Python 3.12 wheel. |
| A module cannot be imported | Activate the virtual environment, then run `python -m pip install -r requirements.txt`. Launch the app from the repository root. |
| The camera cannot be opened | Close other applications using it, allow camera access in the operating system, and try another camera index. |
| A remote app cannot see your webcam | This implementation captures a camera attached to the Python host. Run it locally. |
| The pose is not detected | Use clear lighting and keep the body landmarks needed for the exercise in view. |
| Counts or feedback vary by camera angle | The rules use two-dimensional geometry. Keep the view consistent; see the [architecture notes](architecture.md). |
| OpenCV imports fail after installing several variants | Recreate the environment and install only the requirements in this repository. OpenCV variants share the `cv2` namespace. |

`requirements.txt` uses `opencv-contrib-python` because MediaPipe depends on that distribution. Installing a separate `opencv-python` package alongside it can overwrite the same `cv2` files.
