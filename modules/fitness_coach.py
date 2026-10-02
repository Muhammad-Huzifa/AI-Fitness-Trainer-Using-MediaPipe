"""Workout state and exercise analysis, independent of the user interface."""

from exercises.lunges import LungeValidator
from exercises.pushups import PushupValidator
from exercises.squats import SquatValidator
from modules.pose_analyzer import PoseAnalyzer
from modules.rep_counter import RepCounter


class FitnessCoach:
    """Analyze landmarks and keep statistics for one workout run."""

    CALORIES_PER_REP = 0.5
    VALIDATORS = {
        "Squats": SquatValidator,
        "Push-ups": PushupValidator,
        "Lunges": LungeValidator,
    }

    def __init__(self):
        self.pose_analyzer = PoseAnalyzer()
        self.rep_counter = RepCounter()
        self.total_reps = 0
        self.calories = 0.0

    def analyze_landmarks(self, landmarks, exercise_type):
        """Return workout metrics and form feedback, or no metrics without a pose."""
        if landmarks is None:
            return None, []

        validator_class = self.VALIDATORS.get(exercise_type)
        if validator_class is None:
            return None, []

        validator = validator_class(landmarks, self.pose_analyzer)
        issues = validator.check_form()
        angle = validator.get_key_angle()

        if self.rep_counter.count(angle, exercise_type):
            self.total_reps += 1
            self.calories += self.CALORIES_PER_REP

        metrics = {
            "count": self.total_reps,
            "angle": angle,
            "calories": self.calories,
        }
        return metrics, issues
