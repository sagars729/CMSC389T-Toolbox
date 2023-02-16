import unittest
from gradescope_utils.autograder_utils.decorators import weight, number
from utils import read_submission, request_github, response_to_str
 

class TestHelloWorld(unittest.TestCase):
    def setUp(self):
        self.username, self.repo = read_submission()

    @weight(5)
    @number("2.1")
    def test_file_contains_hello_world(self):
        """Check if test.txt is correct"""
        slug = f"{self.username}/{self.repo}"
        response = request_github(f"repos/{slug}/contents/test.txt")

        # test.txt file exists
        self.assertEqual(response.status_code, 200,
                         "test.txt File Does Not Exist")

        # test.txt file has the phrase "Hello World"
        text = response_to_str(response)
        self.assertIn("hello world", text.lower(), "test.txt does not contain Hello World")
