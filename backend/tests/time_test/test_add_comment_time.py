import unittest
import time
from flask import Flask, jsonify
from unittest.mock import patch
from backend.routes.detailed_system import insert_new_comment
from backend import app, db


class TestAddCommentFunction(unittest.TestCase):
    def setUp(self):
        # Create a Flask application for testing
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Pop the application context after the test
        self.app_context.pop()

    def test_add_comment_function_runtime(self):
        mock_event_id = 1
        mock_user_id = 10
        mock_comment = "mock"
        mock_rating = 5

        # Simulate a request to the login route and measure the time
        start_time = time.time()
        insert_new_comment(mock_event_id, mock_user_id, mock_comment, mock_rating)
        end_time = time.time()

        # Calculate the runtime and print or assert as needed
        runtime = end_time - start_time
        print(f"Add Comment function runtime: {runtime} seconds")


if __name__ == '__main__':
    unittest.main()
