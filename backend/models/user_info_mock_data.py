from backend import bcrypt  # noqa

user_info_mock_data = [
    {
        "username": "guitar hero",
        "uoft_email": "guitar.hero@mail.utoronto.ca",
        "uoft_student_id": "1004140140",
        "first_name": "guitar",
        "last_name": "hero",
        "department": "Music",
        "enrolled_time": "2023",
        "password_hash": bcrypt.generate_password_hash("asdf").decode('utf-8'),
        "organizational_role": True
    },
    {
        "username": "crawarmac",
        "uoft_email": "sam.mas@mail.utoronto.ca",
        "uoft_student_id": "1006141000",
        "first_name": "sam",
        "last_name": "mas",
        "department": "ECE",
        "enrolled_time": "2023",
        "password_hash": bcrypt.generate_password_hash("success").decode('utf-8'),
        "organizational_role": False
    },
    {
        "username": "happy123",
        "uoft_email": "good.morning@mail.utoronto.ca",
        "uoft_student_id": "123455151515",
        "first_name": "Fran",
        "last_name": "Perez",
        "department": "CS",
        "enrolled_time": "2023",
        "password_hash": bcrypt.generate_password_hash("1234").decode('utf-8'),
        "organizational_role": False
    }
]
