from django.test import TestCase
from django.contrib.auth.models import User
from analysis.models import TechnicalAnalysisSettings
from unittest.mock import patch


class SignalHandlersTestCase(TestCase):

    @patch("utils.email_utils.send_admin_email")
    @patch("utils.logging.logger")
    def test_create_user_profile_signal(self, mock_logger, mock_send_email):
        user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )

        mock_send_email.assert_called_once_with(
            "New user created",
            f"User testuser testuser@example.com False {user.date_joined}",
        )

        mock_logger.info.assert_called_once_with("New user created: testuser")

    def test_make_first_user_superuser(self):
        user = User.objects.create_user(username="firstuser", password="testpassword")
        self.client.login(username="firstuser", password="testpassword")

        user.refresh_from_db()
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_technical_analysis_settings_creation_on_login(self):
        user = User.objects.create_user(username="user1", password="testpassword")
        self.client.login(username="user1", password="testpassword")

        ta_settings = TechnicalAnalysisSettings.objects.filter(user=user)
        self.assertTrue(ta_settings.exists())

        with patch("analysis.utils.fetch_utils.fetch_and_save_df") as mock_fetch:
            mock_fetch.assert_called_once_with(ta_settings.first())

    @patch("django.contrib.auth.signals.user_logged_in.send")
    def test_signal_connected(self, mock_send):
        user = User.objects.create_user(username="user2", password="testpassword")
        self.client.login(username="user2", password="testpassword")

        mock_send.assert_called_once_with(
            sender=User, request=self.client.request, user=user
        )
