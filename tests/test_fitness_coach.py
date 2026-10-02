"""Regression checks using synthetic landmarks, without a camera."""

import math
from types import SimpleNamespace
import unittest

from modules.fitness_coach import FitnessCoach
from modules.pose_analyzer import PoseAnalyzer


def point(x, y):
    return SimpleNamespace(x=x, y=y)


def body_landmarks(knee_angle=170, elbow_angle=170):
    """Create two legs and arms with known angles in the image plane."""
    landmarks = [point(0, 0) for _ in range(33)]
    knee_radians = math.radians(knee_angle)
    elbow_radians = math.radians(elbow_angle)
    for offset, shoulder, elbow, wrist, hip, knee, ankle in [
        (0, 11, 13, 15, 23, 25, 27),
        (2, 12, 14, 16, 24, 26, 28),
    ]:
        landmarks[shoulder] = point(offset, 0)
        landmarks[elbow] = point(offset, 1)
        landmarks[wrist] = point(offset + math.sin(elbow_radians),
                                 1 - math.cos(elbow_radians))
        landmarks[hip] = point(offset, 2)
        landmarks[knee] = point(offset, 3)
        landmarks[ankle] = point(offset + math.sin(knee_radians),
                                 3 - math.cos(knee_radians))
    return landmarks


class PoseGeometryTests(unittest.TestCase):
    def test_right_and_straight_joint_angles(self):
        analyzer = PoseAnalyzer()
        self.assertAlmostEqual(analyzer.calculate_angle(point(1, 0), point(0, 0),
                                                       point(0, 1)), 90)
        self.assertAlmostEqual(analyzer.calculate_angle(point(-1, 0), point(0, 0),
                                                       point(1, 0)), 180)

    def test_angle_is_preserved_by_translation_and_uniform_scale(self):
        analyzer = PoseAnalyzer()
        original = analyzer.calculate_angle(point(1, 0), point(0, 0), point(1, 1))
        transformed = analyzer.calculate_angle(point(12, 8), point(10, 8), point(12, 10))
        self.assertAlmostEqual(original, transformed)


class FitnessCoachTests(unittest.TestCase):
    def test_each_exercise_counts_one_complete_cycle(self):
        for exercise in ["Squats", "Push-ups", "Lunges"]:
            with self.subTest(exercise=exercise):
                coach = FitnessCoach()
                for angle in [170, 120, 80, 80, 120, 170, 170]:
                    metrics, _ = coach.analyze_landmarks(
                        body_landmarks(knee_angle=angle, elbow_angle=angle), exercise
                    )
                self.assertEqual(metrics["count"], 1)
                self.assertEqual(metrics["calories"], 0.5)

    def test_partial_motion_does_not_count(self):
        coach = FitnessCoach()
        for angle in [170, 120, 100, 120, 170]:
            metrics, _ = coach.analyze_landmarks(body_landmarks(knee_angle=angle), "Squats")
        self.assertEqual(metrics["count"], 0)
        self.assertEqual(metrics["calories"], 0.0)

    def test_missing_pose_does_not_produce_metrics_or_change_totals(self):
        coach = FitnessCoach()
        coach.analyze_landmarks(body_landmarks(knee_angle=80), "Squats")
        coach.analyze_landmarks(body_landmarks(knee_angle=170), "Squats")
        metrics, issues = coach.analyze_landmarks(None, "Squats")
        self.assertIsNone(metrics)
        self.assertEqual(issues, [])
        self.assertEqual(coach.total_reps, 1)
        self.assertEqual(coach.calories, 0.5)

    def test_new_workout_starts_with_zero_totals(self):
        first = FitnessCoach()
        first.analyze_landmarks(body_landmarks(knee_angle=80), "Squats")
        first.analyze_landmarks(body_landmarks(knee_angle=170), "Squats")
        second = FitnessCoach()
        self.assertEqual(second.total_reps, 0)
        self.assertEqual(second.calories, 0.0)

    def test_joint_mapping_uses_knees_for_squats_and_elbows_for_pushups(self):
        landmarks = body_landmarks(knee_angle=80, elbow_angle=170)
        squat_metrics, _ = FitnessCoach().analyze_landmarks(landmarks, "Squats")
        pushup_metrics, _ = FitnessCoach().analyze_landmarks(landmarks, "Push-ups")
        self.assertAlmostEqual(squat_metrics["angle"], 80)
        self.assertAlmostEqual(pushup_metrics["angle"], 170)


if __name__ == "__main__":
    unittest.main()
