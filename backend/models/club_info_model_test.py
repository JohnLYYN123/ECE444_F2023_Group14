import unittest
from club_info_model import ClubInfoModel, club_info_model_print
from club_info_model_mock_data import club_info_mock_data

class TestClubInfoModel(unittest.TestCase):
    # test if ClubInfoModel construct correctly
    def test_model_init(self):
        mock_model = ClubInfoModel(club_info_mock_data[0])
        mock_model2 = ClubInfoModel(club_info_mock_data[1])
        mock_model3 = ClubInfoModel(club_info_mock_data[2])
        self.assertEqual(mock_model.club_id, 1)
        self.assertEqual(mock_model2.club_id, 2)
        self.assertEqual(mock_model3.club_id, 3)

if __name__ == '__main__':
    unittest.main()

