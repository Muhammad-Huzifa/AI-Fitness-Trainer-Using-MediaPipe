class SquatValidator:
    def __init__(self, landmarks, pose_analyzer):
        self.landmarks = landmarks
        self.pose_analyzer = pose_analyzer
        
    def check_form(self):
        issues = []
        angles = self.pose_analyzer.get_joint_angles(self.landmarks)
        avg_knee = (angles['left_knee'] + angles['right_knee']) / 2
        
        if 110 < avg_knee < 160:
            issues.append("Go deeper! Thighs should be parallel to ground")
        
        if self.landmarks[25].x < self.landmarks[27].x - 0.05:
            issues.append("Knees too far forward!")
        
        back_angle = self.pose_analyzer.calculate_angle(
            self.landmarks[11], self.landmarks[23], self.landmarks[25])
        if back_angle < 150 and avg_knee < 100:
            issues.append("Keep your chest up and back straight!")
        
        return issues
    
    def get_key_angle(self):
        angles = self.pose_analyzer.get_joint_angles(self.landmarks)
        return (angles['left_knee'] + angles['right_knee']) / 2
