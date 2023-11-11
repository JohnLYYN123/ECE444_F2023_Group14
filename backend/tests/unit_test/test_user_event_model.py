import unittest
from backend.models.user_enroll_event_model import UserEnrollEventModel


class TestHostEventModel(unittest.TestCase):
    def setUp(self):
        self.user_event_mock = [
            {
                'user_id': '1',
                'event_id': '2',
            },
        ]

    # Test if HostEventModel constructs correctly
    def test_model_init(self):
        for user_data in self.user_event_mock:
            mock_model = UserEnrollEventModel(
                user_id=user_data['user_id'],
                event_id=user_data['event_id'],
            )
            self.assertEqual(mock_model.user_id, user_data['user_id'])
            self.assertEqual(mock_model.event_id, user_data['event_id'])


if __name__ == '__main__':
    unittest.main()
