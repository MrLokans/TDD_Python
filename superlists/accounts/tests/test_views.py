from django.test import TestCase
from unittest.mock import patch


class LoginViewTest(TestCase):

    @patch('accounts.view.autheticate')
    def test_calls_authenticate_with_assertion_from_post(self, mock_authenticate):
        mock_authenticate.return_vale = None
        self.client.post('/accounts/login', {'assertion': 'assert this'})
        mock_authenticate.assert_called_once_with(assertion='assert this')