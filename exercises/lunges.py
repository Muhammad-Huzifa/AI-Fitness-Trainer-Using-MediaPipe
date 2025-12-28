class LungeValidator:
    def __init__(self, landmarks, pose_analyzer):
        self.landmarks = landmarks
        self.pose_analyzer = pose_analyzer
        
    def check_form(self):
        issues = []
        angles = self.pose_analyzer.get_joint_angles(self.landmarks)
        
        if angles['left_knee'] < 70:
            issues.append("Don't bend knee too much - aim for 90°")
        
        if self.landmarks[25].x < self.landmarks[27].x:
            issues.append("Front knee shouldn't go past toes")
        
        if angles['right_knee'] > 110:
            issues.append("Lower your back knee more")
        
        return issues
    
    def get_key_angle(self):
        return self.pose_analyzer.get_joint_angles(self.landmarks)['left_knee']
