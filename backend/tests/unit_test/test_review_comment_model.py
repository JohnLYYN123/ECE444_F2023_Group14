import unittest
from models.review_rating_model import ReviewRatingModel

class TestReviewRatingModel(unittest.TestCase):
    def setUp(self):
        self.host_event_mock = [
            {
                "event_id": 1,
                "review_user": 5,
                "rating": 4,
                "review_comment": "I really enjoyed it!",
            },
        ]

    # Test if ReviewRatingModel constructs correctly
    def test_model_init(self):
        for comment_data in self.host_event_mock:
            mock_model = ReviewRatingModel(comment_data)
            self.assertEqual(mock_model.review_comment, comment_data['review_comment'])
            self.assertEqual(mock_model.rating, comment_data['rating'])


if __name__ == '__main__':
    unittest.main()