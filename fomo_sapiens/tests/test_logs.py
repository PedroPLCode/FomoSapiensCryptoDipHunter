import unittest
from unittest.mock import patch, mock_open
import os
from utils.logs_utils import send_daily_logs, clear_logs

class TestLoggingFunctions(unittest.TestCase):

    @patch('utils.logs_utils.send_admin_email')
    @patch('utils.logs_utils.logger')
    @patch('utils.logs_utils.os.path.exists')
    @patch('utils.logs_utils.open', new_callable=mock_open)
    @patch('utils.logs_utils.clear_logs')
    def test_send_daily_logs_success(self, mock_clear_logs, mock_open, mock_exists, mock_logger, mock_send_email):
        mock_exists.return_value = True
        mock_open.return_value.read.return_value = "Log content here"

        send_daily_logs()

        mock_send_email.assert_called_once()
        self.assertIn("Successfully sent email with log:", [call[0][0] for call in mock_logger.info.call_args_list])

        mock_clear_logs.assert_called_once()

    @patch('utils.logs_utils.logger')
    @patch('utils.logs_utils.os.path.exists')
    def test_send_daily_logs_file_not_found(self, mock_exists, mock_logger):
        mock_exists.return_value = False

        send_daily_logs()

        mock_logger.warning.assert_called_once_with('Log file does not exist:')

    @patch('utils.logs_utils.send_admin_email')
    @patch('utils.logs_utils.logger')
    @patch('utils.logs_utils.os.path.exists')
    @patch('utils.logs_utils.open', new_callable=mock_open)
    def test_send_daily_logs_error_handling(self, mock_open, mock_exists, mock_logger, mock_send_email):
        mock_exists.return_value = True
        mock_open.return_value.read.return_value = "Log content here"
        mock_send_email.side_effect = Exception("Failed to send email")

        with self.assertRaises(Exception):
            send_daily_logs()

        mock_send_email.assert_called_once()
        self.assertIn("Failed to send email", [call[0][1] for call in mock_logger.warning.call_args_list])

    @patch('utils.logs_utils.logger')
    @patch('utils.logs_utils.os.path.exists')
    @patch('utils.logs_utils.open', new_callable=mock_open)
    def test_clear_logs_success(self, mock_open, mock_exists, mock_logger):
        mock_exists.return_value = True

        clear_logs()

        mock_open.assert_called_once_with(os.path.join(os.getcwd(), 'logfile.log'), 'w')

        mock_logger.info.assert_called_once_with('Successfully cleared log file:')

    @patch('utils.logs_utils.logger')
    @patch('utils.logs_utils.os.path.exists')
    def test_clear_logs_file_not_found(self, mock_exists, mock_logger):
        mock_exists.return_value = False

        clear_logs()

        mock_logger.warning.assert_called_once_with('Log file does not exist:')

    @patch('utils.logs_utils.send_admin_email')
    @patch('utils.logs_utils.logger')
    @patch('utils.logs_utils.os.path.exists')
    @patch('utils.logs_utils.open', new_callable=mock_open)
    def test_clear_logs_error_handling(self, mock_open, mock_exists, mock_logger, mock_send_email):
        mock_exists.return_value = True
        mock_send_email.side_effect = Exception("Failed to send email")

        with self.assertRaises(Exception):
            clear_logs()

        mock_send_email.assert_called_once()
        self.assertIn("Failed to send email", [call[0][1] for call in mock_logger.warning.call_args_list])

if __name__ == "__main__":
    unittest.main()