# Architecture and counting rules

The application has three responsibilities: capturing and displaying frames, analyzing landmarks, and applying exercise rules.

## Frame analysis

1. `app.py` reads a frame from the selected local camera and mirrors it for display.
2. MediaPipe Pose receives an RGB frame and returns body landmarks when a pose is detected.
3. `FitnessCoach` passes the landmarks to the selected exercise validator.
4. `PoseAnalyzer` calculates knee, hip, and elbow angles from the landmarks' `x` and `y` coordinates. Each angle is measured at the middle point of a three-point joint.
5. `RepCounter` tracks bending and extension. The coach updates totals, and the app displays the results on the camera frame and in the sidebar.

`FitnessCoach` contains no camera or Streamlit code. Its `analyze_landmarks()` method can be checked with synthetic landmarks without opening a webcam. When no pose is detected, it returns no metrics; the interface shows a tracking message instead of reporting good form.

The camera is released in a `finally` block. The MediaPipe Pose context closes when capture ends or the Streamlit run is interrupted.

## Repetition thresholds

| Exercise | Key angle | Enter the bent phase | Count after extension |
| --- | --- | --- | --- |
| Squats | Mean of left and right knee angles | Below 90° | Above 160° |
| Push-ups | Mean of left and right elbow angles | Below 90° | Above 160° |
| Lunges | Left knee angle | Below 90° | Above 150° |

These comparisons are strict: reaching exactly 90°, 150°, or 160° does not cross the corresponding threshold. A repetition is counted only after the bent phase is followed by extension. Remaining extended does not add repetitions.

The current lunge validator follows the left knee. Changing the front leg does not automatically change the counting rule.

## Form feedback and workout state

The files in `exercises/` contain the existing angle thresholds and landmark-position checks. They return messages when a rule is triggered. The repository does not include an evaluation of these rules on a labeled exercise-form dataset.

Each new workout run creates a fresh coach with zero repetitions and zero calories. Every counted repetition adds 0.5 to the calorie estimate. No frames or workout records are written to disk by the application.

Camera position, mirrored coordinates, incomplete landmarks, and the absence of visibility filtering can affect feedback. Improving those checks should be evaluated separately from changes to the interface or project layout.
