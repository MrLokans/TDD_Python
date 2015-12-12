from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.authentication import (
    PERSONA_VERIFY_URL, DOMAIN, PersonaAuthenticationBackend
)

User = get_user_model()


@patch('accounts.authentication.requests.post')
class AuthenticationTest(TestCase):

    def setUp(self):
        self.backend = PersonaAuthenticationBackend()
        user = User(email='always@exists.com')
        user.username = 'sampleuser'
        user.save()

    def test_sends_assertion_to_mozilla_with_domain(self, mock_post):
        self.backend.authenticate('an assertion')
        # we assure, that patched method is called with following args
        mock_post.assert_called_once_with(
            PERSONA_VERIFY_URL,
            data={'assertion': 'an assertion', 'audience': DOMAIN}
        )

    def test_returns_none_if_errors_in_response(self, mock_post):
        mock_post.return_value.ok = False
        mock_post.return_value.json.return_value = {}
        user = self.backend.authenticate('an assertion')
        self.assertIsNone(user)

    def test_returns_none_if_status_not_okay(self, mock_post):
        mock_post.return_value.json.return_value = {'status': 'not okay!'}
        user = self.backend.authenticate('an assertion')
        self.assertIsNone(user)

    def test_finds_existing_user_with_email(self, mock_post):
        mock_post.return_value.json.return_value = {'status': 'okay', 'email': 'a@a.a'}
        actual_user = User.objects.create(email='a@a.a')
        found_user = self.backend.authenticate('an assertion')
        self.assertEqual(found_user, actual_user)

    def test_creates_new_user_if_necessary_for_valid_assertion(self, mock_post):
        mock_post.return_value.json.return_value = {'status': 'okay', 'email': 'a@a.a'}
        found_user = self.backend.authenticate('an assertion')
        new_user = User.objects.get(email='a@a.a')
        self.assertEqual(found_user, new_user)
