"""Check camera cleanup and missing-pose feedback with mocked I/O."""

from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch

import app


class WorkoutCaptureTests(unittest.TestCase):
    def setUp(self):
        self.frame_window = MagicMock()
        self.rep_display = MagicMock()
        self.angle_display = MagicMock()
        self.calories_display = MagicMock()
        self.form_display = MagicMock()

    def run_workout(self):
        app.run_workout("Squats", 0, self.frame_window, self.rep_display,
                        self.angle_display, self.calories_display, self.form_display)

    def test_unavailable_camera_is_released_without_starting_pose_tracking(self):
        with patch("app.cv2") as cv2, patch("app.mp") as mp, patch("app.st") as st:
            camera = cv2.VideoCapture.return_value
            camera.isOpened.return_value = False
            self.run_workout()
            camera.release.assert_called_once()
            mp.solutions.pose.Pose.assert_not_called()
            st.error.assert_called_once()

    def test_failed_frame_read_closes_pose_and_releases_camera(self):
        with patch("app.cv2") as cv2, patch("app.mp") as mp, patch("app.st") as st:
            camera = cv2.VideoCapture.return_value
            camera.isOpened.return_value = True
            camera.read.return_value = (False, None)
            self.run_workout()
            camera.release.assert_called_once()
            mp.solutions.pose.Pose.return_value.__exit__.assert_called_once()
            st.error.assert_called_once()

    def test_missing_pose_displays_tracking_feedback_without_reporting_good_form(self):
        with patch("app.cv2") as cv2, patch("app.mp") as mp, patch("app.st"):
            camera = cv2.VideoCapture.return_value
            camera.isOpened.return_value = True
            camera.read.side_effect = [(True, object()), (False, None)]
            pose = mp.solutions.pose.Pose.return_value.__enter__.return_value
            pose.process.return_value = SimpleNamespace(pose_landmarks=None)
            self.run_workout()
            self.form_display.info.assert_called_once()
            self.form_display.success.assert_not_called()
            self.rep_display.metric.assert_not_called()
            self.angle_display.metric.assert_called_once_with("Current angle", "Not detected")
            camera.release.assert_called_once()

    def test_rendering_failure_still_closes_pose_and_releases_camera(self):
        with patch("app.cv2") as cv2, patch("app.mp") as mp, patch("app.st"):
            camera = cv2.VideoCapture.return_value
            camera.isOpened.return_value = True
            camera.read.return_value = (True, object())
            pose = mp.solutions.pose.Pose.return_value.__enter__.return_value
            pose.process.return_value = SimpleNamespace(pose_landmarks=None)
            self.frame_window.image.side_effect = RuntimeError("Rendering failed")
            with self.assertRaisesRegex(RuntimeError, "Rendering failed"):
                self.run_workout()
            camera.release.assert_called_once()
            mp.solutions.pose.Pose.return_value.__exit__.assert_called_once()


if __name__ == "__main__":
    unittest.main()
