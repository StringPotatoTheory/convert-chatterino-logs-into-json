import os
import unittest
from unittest.mock import patch

from main import convert_csv_into_array, get_usernames_and_colors


class TestCodeFile(unittest.TestCase):
    def setUp(self):
        self.file_content = "badge1, badge2, badge3"
        self.file_name = 'test_file.csv'

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    @patch('builtins.print')
    def test_convert_csv_into_array_read_file_not_found(self, mock_print):
        word_array = convert_csv_into_array("invalid_file_name.csv")
        self.assertEqual(word_array, [])
        mock_print.assert_called_with(
            "invalid_file_name.csv is not found, none of these badges will be added to any messages")

    @patch('builtins.print')
    def test_convert_csv_into_array_read_file_empty(self, mock_print):
        with open(self.file_name, 'w') as f:
            f.write('')
        word_array = convert_csv_into_array(self.file_name)
        self.assertEqual(word_array, [])
        mock_print.assert_called_with(f"{self.file_name} is empty, none of these badges will be added to any messages")

    def test_convert_csv_into_array_success(self):
        with open(self.file_name, 'w') as f:
            f.write(self.file_content)
        word_array = convert_csv_into_array(self.file_name)
        self.assertEqual(word_array, ['badge1', 'badge2', 'badge3'])

    @patch('builtins.print')
    def test_get_usernames_and_colors_read_file_not_found(self, mock_print):
        usernames, colors = get_usernames_and_colors("invalid_file_name.csv")
        self.assertEqual(usernames, [])
        self.assertEqual(colors, [])
        mock_print.assert_called_with("invalid_file_name.csv is not found, no colors will be set for any usernames")

    @patch('builtins.print')
    def test_get_usernames_and_colors_read_file_empty(self, mock_print):
        with open(self.file_name, 'w') as f:
            f.write('')
        usernames, colors = get_usernames_and_colors(self.file_name)
        self.assertEqual(usernames, [])
        self.assertEqual(colors, [])
        mock_print.assert_called_with(f"{self.file_name} is empty, no colors will be set for any usernames")

    def test_get_usernames_and_colors_success(self):
        usernames, colors = get_usernames_and_colors('config/example-colors.csv')
        self.assertEqual(usernames, ['username1', 'username2'])
        self.assertEqual(colors, ['#ff00ff', '#00cc00'])
