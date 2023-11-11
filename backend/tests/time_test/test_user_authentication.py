import unittest
import time
from flask import Flask, jsonify
from unittest.mock import patch
from backend.routes.user_authentication_system import login
from backend import app, db


class TestLoginFunction(unittest.TestCase):
    def setUp(self):
        # Create a Flask application for testing
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Pop the application context after the test
        self.app_context.pop()

    @patch('backend.models.user_model.UserModel.query.filter_by')
    @patch('backend.bcrypt.check_password_hash')
    @patch('backend.routes.user_authentication_system.generate_token')
    @patch('backend.routes.user_authentication_system.verify_token')
    def test_login_function_runtime(self, mock_verify_token, mock_generate_token, mock_check_password_hash, mock_filter_by):
        # Mock necessary components
        mock_filter_by.return_value.first.return_value = None  # Assume no user found
        mock_check_password_hash.return_value = True  # Assume password check succeeds
        mock_generate_token.return_value = "mocked_token"

        # Simulate a request to the login route and measure the time
        start_time = time.time()
        response = self.app.post(
            '/login', json={"username": "testuser", "password": "testpassword"})
        end_time = time.time()

        # Calculate the runtime and print or assert as needed
        runtime = end_time - start_time
        print(f"Login function runtime: {runtime} seconds")


if __name__ == '__main__':
    unittest.main()
