class PushupValidator:
    def __init__(self, landmarks, pose_analyzer):
        self.landmarks = landmarks
        self.pose_analyzer = pose_analyzer
        
    def check_form(self):
        issues = []
        angles = self.pose_analyzer.get_joint_angles(self.landmarks)
        avg_elbow = (angles['left_elbow'] + angles['right_elbow']) / 2
        
        if 120 < avg_elbow < 160:
            issues.append("Lower your body more - elbows at 90°")
        
        body_angle = self.pose_analyzer.calculate_angle(
            self.landmarks[11], self.landmarks[23], self.landmarks[27])
        if body_angle < 160:
            issues.append("Keep your body straight! Don't sag hips")
        
        return issues
    
    def get_key_angle(self):
        angles = self.pose_analyzer.get_joint_angles(self.landmarks)
        return (angles['left_elbow'] + angles['right_elbow']) / 2
