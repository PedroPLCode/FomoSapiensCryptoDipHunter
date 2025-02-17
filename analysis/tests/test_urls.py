from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class TechnicalAnalysisURLsTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='password'
        )
        self.client.login(username='testuser', password='password')

    def test_show_technical_analysis_url(self):
        url = reverse('show_technical_analysis')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_technical_analysis_settings_url(self):
        url = reverse('update_technical_analysis_settings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_refresh_data_url(self):
        url = reverse('refresh_data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_send_email_analysis_report_url(self):
        url = reverse('send_email_analysis_report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_redirect(self):
        self.client.logout()
        url = reverse('update_technical_analysis_settings')
        response = self.client.get(url)
        self.assertRedirects(response, '/login/?next=/settings/')