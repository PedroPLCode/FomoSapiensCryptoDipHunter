from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth.models import User
from analysis.models import TechnicalAnalysisSettings


class TestUpdateTechnicalAnalysisSettingsView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.url = reverse("update_technical_analysis_settings")
        self.user_ta_settings = TechnicalAnalysisSettings.objects.create(user=self.user)

    def test_update_settings_valid_form(self):
        data = {
            "symbol": "BTCUSDC",
            "interval": "1h",
            "lookback": 14,
            "general_timeperiod": 14,
            "rsi_timeperiod": 14,
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse("show_technical_analysis"))
        self.user_ta_settings.refresh_from_db()
        self.assertEqual(self.user_ta_settings.symbol, "BTCUSDC")
        self.assertEqual(self.user_ta_settings.interval, "1h")

    def test_update_settings_invalid_form(self):
        data = {
            "symbol": "BTCUSDC",
            "interval": "",
            "lookback": 14,
        }
        response = self.client.post(self.url, data)
        self.assertFormError(response, "form", "interval", "This field is required.")


class TestRefreshDataView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.url = reverse("refresh_data")
        self.user_ta_settings = TechnicalAnalysisSettings.objects.create(user=self.user)

    def test_refresh_data(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("show_technical_analysis"))
        self.user_ta_settings.refresh_from_db()
        self.assertIsNotNone(self.user_ta_settings.df)


class TestShowTechnicalAnalysisView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.url = reverse("show_technical_analysis")
        self.user_ta_settings = TechnicalAnalysisSettings.objects.create(user=self.user)
        self.user_ta_settings.df = '{"close":[1,2,3]}'
        self.user_ta_settings.save()

    def test_show_technical_analysis_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "analysis/show_analysis.html")
        self.assertIn("latest_data", response.context)

    def test_show_technical_analysis_guest(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "analysis/show_analysis.html")


class TestSendEmailAnalysisReportView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.url = reverse("send_email_analysis_report")
        self.user_ta_settings = TechnicalAnalysisSettings.objects.create(user=self.user)
        self.user_ta_settings.df = '{"close":[1,2,3]}'
        self.user_ta_settings.save()

    @patch("fomo_sapiens.utils.email_utils.send_email")
    def test_send_email_analysis_report(self, mock_send_email):
        mock_send_email.return_value = None

        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("show_technical_analysis"))
        self.assertTrue(mock_send_email.called)
        self.assertEqual(mock_send_email.call_count, 1)


class TestShowTechnicalAnalysisViewWithErrors(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.url = reverse("show_technical_analysis")
        self.user_ta_settings = TechnicalAnalysisSettings.objects.create(user=self.user)
        self.user_ta_settings.df = ""
        self.user_ta_settings.save()

    def test_show_analysis_with_empty_data(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Error loading data.")
