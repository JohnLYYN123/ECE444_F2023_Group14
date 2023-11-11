import unittest
from backend.models.host_event_model import HostEventModel


class TestHostEventModel(unittest.TestCase):
    def setUp(self):
        self.host_event_mock = [
            {
                'host_id': '1',
                'event_id': '2',
            },
        ]

    # Test if HostEventModel constructs correctly
    def test_model_init(self):
        for user_data in self.host_event_mock:
            mock_model = HostEventModel(
                host_id=user_data['host_id'],
                event_id=user_data['event_id'],
            )
            self.assertEqual(mock_model.host_id, user_data['host_id'])
            self.assertEqual(mock_model.event_id, user_data['event_id'])


if __name__ == '__main__':
    unittest.main()
