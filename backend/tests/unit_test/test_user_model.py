import unittest
from backend.models.user_info_mock_data import user_info_mock_data
from backend.models.user_model import UserModel


class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.user_info_mock_data = [
            {
                'username': 'guitar hero',
                'uoft_email': 'guitar.hero@mail.utoronto.ca',
                'uoft_student_id': '1004140140',
                'first_name': 'guitar',
                'last_name': 'hero',
                'department': 'Music',
                'enrolled_time': '2023',
                'password_hash': 'fahjkfhjkahfjkahjfakfhqk',
                'organizational_role': True
            },
        ]

    # Test if UserModel constructs correctly
    def test_model_init(self):
        for user_data in self.user_info_mock_data:
            mock_model = UserModel(
                username=user_data['username'],
                uoft_email=user_data['uoft_email'],
                uoft_student_id=user_data['uoft_student_id'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                department=user_data['department'],
                enrolled_time=user_data['enrolled_time'],
                password_hash=user_data['password_hash'],
                organizational_role=user_data['organizational_role']
            )

            self.assertEqual(mock_model.username, user_data['username'])


if __name__ == '__main__':
    unittest.main()
