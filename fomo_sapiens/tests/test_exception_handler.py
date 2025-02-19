import unittest
from unittest.mock import patch
from utils.exception_handlers import exception_handler


class TestExceptionHandler(unittest.TestCase):

    @patch("utils.logging_functions.logger")
    @patch("utils.email_utils.send_admin_email")
    def test_function_success(self, mock_send_email, mock_logger):
        @exception_handler(default_return="Fallback value")
        def successful_function():
            return "Success"

        result = successful_function()

        self.assertEqual(result, "Success")
        mock_send_email.assert_not_called()
        mock_logger.error.assert_not_called()

    @patch("utils.logging_functions.logger")
    @patch("utils.email_utils.send_admin_email")
    def test_function_with_index_error(self, mock_send_email, mock_logger):
        @exception_handler(default_return="Fallback value")
        def function_with_index_error():
            raise IndexError("Test IndexError")

        result = function_with_index_error()

        self.assertEqual(result, "Fallback value")
        mock_send_email.assert_called_once()
        self.assertIn(
            "IndexError in function_with_index_error",
            [call[0][0] for call in mock_send_email.call_args_list],
        )
        mock_logger.error.assert_called_once()

    @patch("utils.logging_functions.logger")
    @patch("utils.email_utils.send_admin_email")
    def test_function_with_unhandled_exception(self, mock_send_email, mock_logger):
        @exception_handler(default_return="Fallback value")
        def function_with_unhandled_exception():
            raise ValueError("Test ValueError")

        result = function_with_unhandled_exception()

        self.assertEqual(result, "Fallback value")
        mock_send_email.assert_called_once()
        self.assertIn(
            "Exception in function_with_unhandled_exception",
            [call[0][0] for call in mock_send_email.call_args_list],
        )
        mock_logger.error.assert_called_once()

    @patch("utils.logging_functions.logger")
    @patch("utils.email_utils.send_admin_email")
    @patch("sys.exit")
    def test_function_with_exit(self, mock_exit, mock_send_email, mock_logger):
        @exception_handler(default_return="exit")
        def function_with_exit():
            raise IndexError("Test IndexError")

        with self.assertRaises(SystemExit):
            function_with_exit()

        mock_exit.assert_called_once_with(1)
        mock_send_email.assert_called_once()
        self.assertIn(
            "IndexError in function_with_exit",
            [call[0][0] for call in mock_send_email.call_args_list],
        )

    @patch("utils.logging_functions.logger")
    @patch("utils.email_utils.send_admin_email")
    def test_function_with_callable_default_return(self, mock_send_email, mock_logger):
        def custom_return_value():
            return "Callable Result"

        @exception_handler(default_return=custom_return_value)
        def function_with_callable():
            raise IndexError("Test IndexError")

        result = function_with_callable()

        self.assertEqual(result, "Callable Result")
        mock_send_email.assert_called_once()
        self.assertIn(
            "IndexError in function_with_callable",
            [call[0][0] for call in mock_send_email.call_args_list],
        )


if __name__ == "__main__":
    unittest.main()
