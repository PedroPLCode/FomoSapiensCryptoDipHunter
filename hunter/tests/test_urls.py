from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from hunter.models import TechnicalAnalysisHunter

class HunterViewsTest(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_show_hunters_list(self):
        url = reverse('hunter:show_hunters_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hunter/hunters_list.html')

    def test_hunter_create_or_edit_create(self):
        url = reverse('hunter:hunter_create_or_edit', kwargs={'pk': None})
        data = {
            'name': 'Hunter 1',
            'df': '{"price": [1, 2, 3]}'
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('hunter:show_hunters_list'))
        self.assertEqual(TechnicalAnalysisHunter.objects.count(), 1)

    def test_hunter_create_or_edit_edit(self):
        hunter = TechnicalAnalysisHunter.objects.create(user=self.user, name='Hunter 1', df='{"price": [1, 2, 3]}')
        url = reverse('hunter:hunter_create_or_edit', kwargs={'pk': hunter.pk})
        data = {
            'name': 'Updated Hunter',
            'df': '{"price": [4, 5, 6]}'
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('hunter:show_hunters_list'))
        hunter.refresh_from_db()
        self.assertEqual(hunter.name, 'Updated Hunter')

    def test_hunter_delete(self):
        hunter = TechnicalAnalysisHunter.objects.create(user=self.user, name='Hunter to delete', df='{"price": [1, 2, 3]}')
        url = reverse('hunter:hunter_delete', kwargs={'pk': hunter.pk})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('hunter:show_hunters_list'))
        self.assertEqual(TechnicalAnalysisHunter.objects.count(), 0)

    def test_remove_all_hunters(self):
        TechnicalAnalysisHunter.objects.create(user=self.user, name='Hunter 1', df='{"price": [1, 2, 3]}')
        TechnicalAnalysisHunter.objects.create(user=self.user, name='Hunter 2', df='{"price": [4, 5, 6]}')
        url = reverse('hunter:remove_all_hunters')
        response = self.client.post(url)
        self.assertRedirects(response, reverse('hunter:show_hunters_list'))
        self.assertEqual(TechnicalAnalysisHunter.objects.count(), 0)

    def test_start_all_hunters(self):
        hunter1 = TechnicalAnalysisHunter.objects.create(user=self.user, name='Hunter 1', df='{"price": [1, 2, 3]}')
        hunter2 = TechnicalAnalysisHunter.objects.create(user=self.user, name='Hunter 2', df='{"price": [4, 5, 6]}')
        url = reverse('hunter:start_all_hunters')
        response = self.client.post(url)
        self.assertRedirects(response, reverse('hunter:show_hunters_list'))
        hunter1.refresh_from_db()
        hunter2.refresh_from_db()
        self.assertTrue(hunter1.running)
        self.assertTrue(hunter2.running)

    def test_start_hunter(self):
        hunter = TechnicalAnalysisHunter.objects.create(user=self.user, name='Hunter 1', df='{"price": [1, 2, 3]}')
        url = reverse('hunter:start_hunter', kwargs={'pk': hunter.pk})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('hunter:show_hunters_list'))
        hunter.refresh_from_db()
        self.assertTrue(hunter.running)

    def test_stop_hunter(self):
        hunter = TechnicalAnalysisHunter.objects.create(user=self.user, name='Hunter 1', df='{"price": [1, 2, 3]}', running=True)
        url = reverse('hunter:stop_hunter', kwargs={'pk': hunter.pk})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('hunter:show_hunters_list'))
        hunter.refresh_from_db()
        self.assertFalse(hunter.running)

    def test_stop_all_hunters(self):
        hunter1 = TechnicalAnalysisHunter.objects.create(user=self.user, name='Hunter 1', df='{"price": [1, 2, 3]}', running=True)
        hunter2 = TechnicalAnalysisHunter.objects.create(user=self.user, name='Hunter 2', df='{"price": [4, 5, 6]}', running=True)
        url = reverse('hunter:stop_all_hunters')
        response = self.client.post(url)
        self.assertRedirects(response, reverse('hunter:show_hunters_list'))
        hunter1.refresh_from_db()
        hunter2.refresh_from_db()
        self.assertFalse(hunter1.running)
        self.assertFalse(hunter2.running)