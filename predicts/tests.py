from django.test import TestCase
from django.utils import timezone
from .models import MatchPrediction

class MatchPredictionTest(TestCase):
    def setUp(self):
        # Create a sample MatchPrediction object for testing
        self.prediction = MatchPrediction.objects.create(
            matchApiId=123,
            homeTeamScore=2,
            homeTeamName="Home Team",
            awayTeamScore=1,
            awayTeamName="Away Team",
            user_id=2,
            goalScorerId=456,
            goalScorerName="Goal Scorer",
            checked=False,
            league="Sample League",
            match_date=timezone.now(),
        )

    def test_is_correct_score(self):
        self.assertTrue(self.prediction.is_correct_score())

    def test_is_correct_result(self):
        self.assertTrue(self.prediction.is_correct_result())

    def test_is_correct_first_goal_scorer(self):
        self.assertTrue(self.prediction.is_correct_first_goal_scorer())

    def test_does_first_goal_scorer_score_anytime(self):
        self.assertTrue(self.prediction.does_first_goal_scorer_score_anytime())

    def test_calculate_points(self):
        expected_points = 10  # Adjust based on the expected points for the prediction
        self.assertEqual(self.prediction.calculate_points(), expected_points)

    def test_update_points(self):
        expected_points = 10  # Adjust based on the expected points for the prediction
        self.prediction.update_points()
        self.assertEqual(self.prediction.points, expected_points)
