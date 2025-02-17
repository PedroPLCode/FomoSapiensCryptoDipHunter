from django.test import TestCase
from django.contrib.auth import get_user_model
from analysis.models import (
    TechnicalAnalysisSettings, 
    default_plot_indicators, 
    default_df
)

class TechnicalAnalysisSettingsModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='password'
        )

    def test_technical_analysis_settings_creation(self):
        settings = TechnicalAnalysisSettings.objects.create(user=self.user)

        self.assertEqual(settings.user, self.user)
        self.assertEqual(settings.symbol, 'BTCUSDC')
        self.assertEqual(settings.interval, '1h')
        self.assertEqual(settings.lookback, '1d')
        self.assertEqual(settings.general_timeperiod, 14)

    def test_default_selected_plot_indicators(self):
        settings = TechnicalAnalysisSettings.objects.create(user=self.user)
        self.assertEqual(settings.selected_plot_indicators, ['rsi', 'macd'])

    def test_default_df(self):
        settings = TechnicalAnalysisSettings.objects.create(user=self.user)
        self.assertIn('BTCUSDC', settings.df)
        self.assertIsInstance(settings.df, list)

    def test_str_method(self):
        settings = TechnicalAnalysisSettings.objects.create(user=self.user)
        self.assertEqual(str(settings), "Technical Analysis settings for testuser")


class UserSignalsTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='password'
        )

    def test_create_user_analysis_settings(self):
        settings = TechnicalAnalysisSettings.objects.get(user=self.user)
        self.assertEqual(settings.user, self.user)
        self.assertEqual(settings.symbol, 'BTCUSDC')
        self.assertEqual(settings.interval, '1h')

    def test_save_user_analysis_settings(self):
        self.user.username = 'newusername'
        self.user.save()
        settings = TechnicalAnalysisSettings.objects.get(user=self.user)
        self.assertEqual(settings.user.username, 'newusername')


class SaveUserAnalysisSettingsSignalTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='password'
        )
        self.settings = TechnicalAnalysisSettings.objects.create(user=self.user)

    def test_save_user_analysis_settings(self):
        self.user.username = 'updatedusername'
        self.user.save()
        
        settings = TechnicalAnalysisSettings.objects.get(user=self.user)
        self.assertEqual(settings.user.username, 'updatedusername')


class FunctionsTest(TestCase):

    def test_default_plot_indicators(self):
        expected_indicators = ['rsi', 'macd']
        self.assertEqual(default_plot_indicators(), expected_indicators)

    def test_default_df(self):
        df = default_df()
        self.assertIsInstance(df, dict)
        self.assertIn('BTCUSDC', df)