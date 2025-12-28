import numpy as np

class PoseAnalyzer:
    def calculate_angle(self, p1, p2, p3):
        a = np.array([p1.x, p1.y])
        b = np.array([p2.x, p2.y])
        c = np.array([p3.x, p3.y])
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        return 360-angle if angle > 180.0 else angle
    
    def get_joint_angles(self, landmarks):
        return {
            'left_knee': self.calculate_angle(landmarks[23], landmarks[25], landmarks[27]),
            'right_knee': self.calculate_angle(landmarks[24], landmarks[26], landmarks[28]),
            'left_hip': self.calculate_angle(landmarks[11], landmarks[23], landmarks[25]),
            'right_hip': self.calculate_angle(landmarks[12], landmarks[24], landmarks[26]),
            'left_elbow': self.calculate_angle(landmarks[11], landmarks[13], landmarks[15]),
            'right_elbow': self.calculate_angle(landmarks[12], landmarks[14], landmarks[16]),
        }
