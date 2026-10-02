"""Streamlit interface for local webcam exercise analysis."""

import cv2
import mediapipe as mp
import streamlit as st

from modules.fitness_coach import FitnessCoach


def run_workout(exercise, camera_index, frame_window, rep_display,
                angle_display, calories_display, form_display):
    """Process webcam frames and release resources when the run ends."""
    cap = cv2.VideoCapture(camera_index)
    try:
        if not cap.isOpened():
            st.error("Cannot access the camera. Check its index and permissions.")
            return

        coach = FitnessCoach()
        mp_pose = mp.solutions.pose
        mp_drawing = mp.solutions.drawing_utils

        with mp_pose.Pose(min_detection_confidence=0.7,
                          min_tracking_confidence=0.7) as pose:
            while True:
                success, frame = cap.read()
                if not success:
                    st.error("Cannot read a camera frame. Check the connection.")
                    break

                frame = cv2.flip(frame, 1)
                results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                landmarks = (
                    results.pose_landmarks.landmark
                    if results.pose_landmarks else None
                )
                rep_data, issues = coach.analyze_landmarks(landmarks, exercise)

                if rep_data is not None:
                    rep_display.metric("Reps completed", rep_data["count"])
                    angle_display.metric("Current angle", f'{int(rep_data["angle"])}°')
                    calories_display.metric("Estimated calories", f'{rep_data["calories"]:.1f}')

                    cv2.putText(frame, f'Reps: {rep_data["count"]}', (20, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
                    cv2.putText(frame, f'Angle: {int(rep_data["angle"])}', (20, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    mp_drawing.draw_landmarks(
                        frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                        mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2),
                    )

                if landmarks is None:
                    angle_display.metric("Current angle", "Not detected")
                    form_display.info("No pose detected. Keep your full body in view.")
                elif issues:
                    form_display.warning("Form feedback:\n" + "\n".join(f"- {issue}" for issue in issues))
                else:
                    form_display.success("No form issues detected.")

                frame_window.image(frame, channels="BGR")
    finally:
        cap.release()


def main():
    st.set_page_config(page_title="AI Fitness Coach", page_icon="💪", layout="wide")
    st.title("AI Fitness Coach")
    st.caption("Local webcam pose analysis for squats, push-ups, and lunges.")
    video_column, stats_column = st.columns([3, 1])

    with stats_column:
        exercise = st.selectbox("Select exercise", ["Squats", "Push-ups", "Lunges"])
        camera_index = int(st.number_input("Camera index", min_value=0, value=0, step=1))
        st.subheader("Workout stats")
        rep_display = st.empty()
        angle_display = st.empty()
        calories_display = st.empty()
        rep_display.metric("Reps completed", 0)
        angle_display.metric("Current angle", "Not detected")
        calories_display.metric("Estimated calories", "0.0")
        st.caption("Calorie estimate: a fixed 0.5 kcal per counted repetition.")
        form_display = st.empty()

    with video_column:
        run = st.checkbox("Start workout", value=False)
        frame_window = st.empty()

    if run:
        run_workout(exercise, camera_index, frame_window, rep_display,
                    angle_display, calories_display, form_display)
    else:
        st.info("Select an exercise, then check Start workout to begin.")


if __name__ == "__main__":
    main()
