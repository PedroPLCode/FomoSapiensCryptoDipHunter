from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.http import HttpRequest
from unittest.mock import patch
from views import custom_404_view

class ViewsTestCase(TestCase):
    
    def test_custom_404_view(self):
        request = HttpRequest()
        exception = Exception("Not found")
        
        response = custom_404_view(request, exception)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        
        storage = get_messages(request)
        messages_list = list(storage)
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), '404 > home_page')

    @patch('analysis.utils.fetch_utils.fetch_server_time')
    @patch('analysis.utils.fetch_utils.fetch_system_status')
    def test_home_page(self, mock_fetch_system_status, mock_fetch_server_time):
        mock_fetch_system_status.return_value = "OK"
        mock_fetch_server_time.return_value = "2025-02-17 12:00:00"
        
        response = self.client.get(reverse('home_page'))
        
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "2025-02-17 12:00:00")
        self.assertContains(response, "OK")