from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.http import HttpRequest


class UrlsTestCase(TestCase):

    def test_home_page_url(self):
        url = reverse("home_page")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2025-02-17 12:00:00")
        self.assertContains(response, "OK")

    def test_custom_404_view(self):
        url = "/nonexistent-url/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

        request = HttpRequest()
        storage = get_messages(request)
        messages_list = list(storage)
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), "404 > home_page")

    def test_url_patterns(self):
        response = self.client.get(reverse("home_page"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/accounts/")
        self.assertEqual(response.status_code, 404)

        response = self.client.get("/captcha/")
        self.assertEqual(response.status_code, 404)

        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/analysis/")
        self.assertEqual(response.status_code, 404)

        response = self.client.get("/hunter/")
        self.assertEqual(response.status_code, 404)
