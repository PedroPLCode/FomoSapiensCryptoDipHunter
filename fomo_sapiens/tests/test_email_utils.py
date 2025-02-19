import unittest
from unittest.mock import patch, MagicMock
from utils.email_utils import send_email, send_admin_email


class TestEmailFunctions(unittest.TestCase):

    @patch("utils.send_mail")
    @patch("utils.logger")
    def test_send_email_success(self, mock_logger, mock_send_mail):
        mock_send_mail.return_value = 1

        result = send_email("test@example.com", "Test Subject", "Test Body")

        self.assertTrue(result)
        mock_send_mail.assert_called_once_with(
            "Test Subject", "Test Body", "your-email@example.com", ["test@example.com"]
        )
        mock_logger.info.assert_called_once_with(
            'Email "Test Subject" to test@example.com sent successfully.'
        )

    @patch("utils.send_mail")
    @patch("utils.logger")
    def test_send_email_failure(self, mock_logger, mock_send_mail):
        mock_send_mail.side_effect = Exception("Send mail error")

        result = send_email("test@example.com", "Test Subject", "Test Body")

        self.assertFalse(result)
        mock_logger.error.assert_called_once_with(
            "Error sending email to test@example.com. Error: Send mail error"
        )

    @patch("utils.send_mail")
    @patch("utils.logger")
    @patch("utils.User.objects.filter")
    def test_send_admin_email_success(
        self, mock_user_filter, mock_logger, mock_send_mail
    ):
        mock_send_mail.return_value = 1
        mock_user_filter.return_value = [MagicMock(email="admin@example.com")]

        send_admin_email("Admin Subject", "Admin Body")

        mock_send_mail.assert_called_once_with(
            "Admin Subject",
            "Admin Body",
            "your-email@example.com",
            ["admin@example.com"],
        )
        mock_logger.info.assert_called_once_with(
            'Email "Admin Subject" to admin@example.com sent successfully.'
        )

    @patch("utils.send_mail")
    @patch("utils.logger")
    @patch("utils.User.objects.filter")
    def test_send_admin_email_failure(
        self, mock_user_filter, mock_logger, mock_send_mail
    ):
        mock_send_mail.side_effect = Exception("Send mail error")
        mock_user_filter.return_value = [MagicMock(email="admin@example.com")]

        send_admin_email("Admin Subject", "Admin Body")

        mock_logger.error.assert_called_once_with(
            "Error sending email to admin@example.com. Error: Send mail error"
        )

    @patch("utils.send_mail")
    @patch("utils.logger")
    @patch("utils.User.objects.filter")
    def test_send_admin_email_no_superusers(
        self, mock_user_filter, mock_logger, mock_send_mail
    ):
        mock_user_filter.return_value = []

        send_admin_email("Admin Subject", "Admin Body")

        mock_send_mail.assert_not_called()
        mock_logger.info.assert_called_once_with(
            "No superuser found to send admin email."
        )


if __name__ == "__main__":
    unittest.main()
