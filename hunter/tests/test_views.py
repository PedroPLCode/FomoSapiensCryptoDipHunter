from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from hunter.models import TechnicalAnalysisHunter

class HunterViewsTestCase(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_show_hunters_list(self):
        hunter = TechnicalAnalysisHunter.objects.create(user=self.user, df='{"data":[1,2,3]}')
        
        response = self.client.get(reverse('show_hunters_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'hunters_list.html')
        self.assertContains(response, hunter.df)

    def test_hunter_create_or_edit_create(self):
        response = self.client.get(reverse('hunter_create_or_edit'))
        self.assertEqual(response.status_code, 200)
        
        data = {
            'name': 'Test Hunter',
            'df': '{"data":[1,2,3]}'
        }
        
        response = self.client.post(reverse('hunter_create_or_edit'), data)
        self.assertRedirects(response, reverse('show_hunters_list'))
        self.assertTrue(TechnicalAnalysisHunter.objects.filter(name='Test Hunter').exists())

    def test_hunter_delete(self):
        hunter = TechnicalAnalysisHunter.objects.create(user=self.user, df='{"data":[1,2,3]}')
        response = self.client.post(reverse('hunter_delete', kwargs={'pk': hunter.pk}))
        self.assertRedirects(response, reverse('show_hunters_list'))
        self.assertFalse(TechnicalAnalysisHunter.objects.filter(pk=hunter.pk).exists())

    def test_start_all_hunters(self):
        hunter = TechnicalAnalysisHunter.objects.create(user=self.user, df='{"data":[1,2,3]}')
        response = self.client.post(reverse('start_all_hunters'))
        self.assertRedirects(response, reverse('show_hunters_list'))
        hunter.refresh_from_db()
        self.assertTrue(hunter.running)
        
    def test_stop_all_hunters(self):
        hunter = TechnicalAnalysisHunter.objects.create(user=self.user, df='{"data":[1,2,3]}')
        response = self.client.post(reverse('stop_all_hunters'))
        self.assertRedirects(response, reverse('show_hunters_list'))
        hunter.refresh_from_db()
        self.assertTrue(hunter.running)
        
    def test_start_hunter(self):
        hunter = TechnicalAnalysisHunter.objects.create(user=self.user, df='{"data":[1,2,3]}')
        response = self.client.post(reverse('start_hunter'))
        self.assertRedirects(response, reverse('show_hunters_list'))
        hunter.refresh_from_db()
        self.assertTrue(hunter.running)
        
    def test_stophunter(self):
        hunter = TechnicalAnalysisHunter.objects.create(user=self.user, df='{"data":[1,2,3]}')
        response = self.client.post(reverse('stop_hunter'))
        self.assertRedirects(response, reverse('show_hunters_list'))
        hunter.refresh_from_db()
        self.assertTrue(hunter.running)