import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from modules.pose_analyzer import PoseAnalyzer
from modules.rep_counter import RepCounter
from exercises.squats import SquatValidator
from exercises.pushups import PushupValidator
from exercises.lunges import LungeValidator

st.set_page_config(page_title="AI Fitness Coach", page_icon="💪", layout="wide")

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

class FitnessCoach:
    def __init__(self):
        self.pose_analyzer = PoseAnalyzer()
        self.rep_counter = RepCounter()
        self.total_reps = 0
        self.calories = 0
        
    def analyze_frame(self, frame, exercise_type):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)
        form_issues = []
        rep_data = None
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            
            validator = {
                "Squats": SquatValidator,
                "Push-ups": PushupValidator,
                "Lunges": LungeValidator
            }.get(exercise_type)
            
            if validator:
                v = validator(landmarks, self.pose_analyzer)
                form_issues = v.check_form()
                key_angle = v.get_key_angle()
                
                if self.rep_counter.count(key_angle, exercise_type):
                    self.total_reps += 1
                    self.calories += 0.5
                
                rep_data = {'count': self.total_reps, 'angle': key_angle, 'calories': self.calories}
                
                cv2.putText(frame, f"Reps: {self.total_reps}", (20, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
                cv2.putText(frame, f"Angle: {int(key_angle)}", (20, 100),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                     mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2),
                                     mp_drawing.DrawingSpec(color=(0,0,255), thickness=2))
        
        return frame, rep_data, form_issues

def main():
    st.title("💪 AI Fitness Coach - Real-Time Form Analysis")
    col1, col2 = st.columns([3, 1])
    
    with col2:
        exercise = st.selectbox("Select Exercise", ["Squats", "Push-ups", "Lunges"])
        st.markdown("---\n### 📊 Workout Stats")
        rep_display = st.empty()
        angle_display = st.empty()
        calories_display = st.empty()
        st.markdown("---")
        form_display = st.empty()
        
    with col1:
        run = st.checkbox("🎥 Start Workout", value=False)
        frame_window = st.image([])
    
    if run:
        coach = FitnessCoach()
        cap = cv2.VideoCapture(0)
        
        while run:
            ret, frame = cap.read()
            if not ret:
                st.error("❌ Cannot access camera")
                break
            
            frame = cv2.flip(frame, 1)
            analyzed_frame, rep_data, issues = coach.analyze_frame(frame, exercise)
            
            if rep_data:
                rep_display.metric("Reps Completed", rep_data['count'])
                angle_display.metric("Current Angle", f"{int(rep_data['angle'])}°")
                calories_display.metric("Calories Burned", f"{rep_data['calories']:.1f}")
            
            if issues:
                form_display.error("⚠️ Form Issues:\n" + "\n".join(f"- {i}" for i in issues))
            else:
                form_display.success("✅ Perfect Form!")
            
            frame_window.image(analyzed_frame, channels="BGR")
        
        cap.release()
    else:
        st.info("👆 Check 'Start Workout' to begin")

if __name__ == "__main__":
    main()
