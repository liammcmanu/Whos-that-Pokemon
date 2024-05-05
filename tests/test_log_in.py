import unittest
from unittest.mock import patch, PropertyMock

from log_in import SignUpStrategy, SignInStrategy, log_in, select_option

class TestSignUpStrategy(unittest.TestCase):

    @patch('log_in.Prompt.ask', side_effect=['testuser', 'testpass', 'testpass', '2000-01-01'])
    @patch('log_in.db')
    def test_sign_up(self, mock_db, mock_prompt):

        mock_db.check_username_taken.return_value = False
        mock_db.push_user.return_value = True

        strategy = SignUpStrategy()

        strategy.authenticate()

        mock_db.check_username_taken.assert_called_with('testuser')
        mock_db.push_user.assert_called_with(data_dict={'username': 'testuser', 'password': 'testpass', 'age': 24})

    @patch('log_in.Prompt.ask', side_effect=['testuser', 'testpass'])
    @patch('log_in.db')
    def test_sign_in(self, mock_db, mock_prompt):

        mock_db.check_username_taken.return_value = True
        mock_db.authenticate_user.return_value = True

        strategy = SignInStrategy()

        strategy.authenticate()

        mock_db.check_username_taken.assert_called_with('testuser')
        mock_db.authenticate_user.assert_called_with('testuser', 'testpass')

    @patch('log_in.inquirer.list_input', return_value="Sign-in 🔑")
    @patch('log_in.AuthenticationContext')
    def test_log_in(self, mock_auth_context, mock_list_input):

        mock_auth_context.return_value.authenticate_user.return_value = True

        result = log_in()

        mock_list_input.assert_called_with("Please select an option", choices=["Sign-in 🔑", "Sign-up 🔐"])

        args, _ = mock_auth_context.call_args
        self.assertIsInstance(args[0], SignInStrategy)
        mock_auth_context.return_value.authenticate_user.assert_called_once()

        self.assertTrue(result)

    @patch('log_in.inquirer.list_input', return_value="Sign-up 🔐")
    @patch('log_in.AuthenticationContext')
    def test_select_option(self, mock_auth_context, mock_list_input):

        mock_auth_context.return_value.authenticate_user.return_value = True

        result = select_option()

        mock_list_input.assert_called_with("Please select an option", choices=["Sign-in 🔑", "Sign-up 🔐"])

        args, _ = mock_auth_context.call_args
        self.assertIsInstance(args[0], SignUpStrategy)
        mock_auth_context.return_value.authenticate_user.assert_called_once()

        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()