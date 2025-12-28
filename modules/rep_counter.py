class RepCounter:
    def __init__(self):
        self.stage = "up"
        
    def count(self, angle, exercise_type):
        thresholds = {
            "Squats": (90, 160),
            "Push-ups": (90, 160),
            "Lunges": (90, 150)
        }
        down, up = thresholds.get(exercise_type, (90, 160))
        
        if angle < down and self.stage == "up":
            self.stage = "down"
        if angle > up and self.stage == "down":
            self.stage = "up"
            return True
        return False
