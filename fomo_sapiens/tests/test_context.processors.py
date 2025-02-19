import unittest
from unittest.mock import patch, MagicMock
from utils.context_processors import (
    inject_date_and_time,
    inject_user_agent,
    inject_system_info,
    inject_system_uptime,
    inject_python_version,
    inject_django_version,
    inject_numpy_version,
    inject_pandas_version,
    inject_db_info,
)


class TestInjectFunctions(unittest.TestCase):

    @patch("django.utils.timezone.now")
    def test_inject_date_and_time_success(self, mock_now):
        mock_now.return_value = "2025-02-17T12:00:00Z"
        request = MagicMock()
        result = inject_date_and_time(request)
        self.assertEqual(result, {"date_and_time": "2025-02-17T12:00:00Z"})

    def test_inject_user_agent_success(self):
        request = MagicMock()
        request.META.get.return_value = "Mozilla/5.0"
        result = inject_user_agent(request)
        self.assertEqual(result, {"user_agent": "Mozilla/5.0"})

    @patch("platform.system")
    @patch("platform.version")
    @patch("platform.release")
    def test_inject_system_info_success(self, mock_release, mock_version, mock_system):
        mock_system.return_value = "Linux"
        mock_version.return_value = "5.10.0"
        mock_release.return_value = "Ubuntu"
        request = MagicMock()
        result = inject_system_info(request)
        self.assertEqual(result, {"system_info": "Linux Ubuntu 5.10.0"})

    @patch("subprocess.check_output")
    def test_inject_system_uptime_success(self, mock_uptime):
        mock_uptime.return_value = "up 1 day, 3 hours, 45 minutes"
        request = MagicMock()
        result = inject_system_uptime(request)
        self.assertEqual(result, {"system_uptime": "up 1 day, 3 hours, 45 minutes"})

    def test_inject_python_version_success(self):
        request = MagicMock()
        result = inject_python_version(request)
        self.assertIn("python_version", result)

    @patch("builtins.__import__")
    def test_inject_django_version_success(self, mock_import):
        mock_import.return_value.__version__ = "4.1.0"
        request = MagicMock()
        result = inject_django_version(request)
        self.assertEqual(result, {"django_version": "4.1.0"})

    @patch("numpy.__version__")
    def test_inject_numpy_version_success(self, mock_numpy_version):
        mock_numpy_version = "1.24.0"
        request = MagicMock()
        result = inject_numpy_version(request)
        self.assertEqual(result, {"numpy_version": "1.24.0"})

    @patch("pandas.__version__")
    def test_inject_pandas_version_success(self, mock_pandas_version):
        mock_pandas_version = "1.5.0"
        request = MagicMock()
        result = inject_pandas_version(request)
        self.assertEqual(result, {"pandas_version": "1.5.0"})

    @patch("django.db.connection.vendor")
    def test_inject_db_info_success(self, mock_vendor):
        mock_vendor.return_value = "PostgreSQL"
        request = MagicMock()
        result = inject_db_info(request)
        self.assertEqual(result, {"db_engine": "PostgreSQL"})


if __name__ == "__main__":
    unittest.main()
