from django.test import TestCase
from django.contrib.auth import get_user_model
from analysis.forms import TechnicalAnalysisSettingsForm
from analysis.models import TechnicalAnalysisSettings

class TechnicalAnalysisSettingsFormTest(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.analysis_settings = TechnicalAnalysisSettings.objects.create(user=self.user)

    def test_form_valid_data(self):
        data = {
            'symbol': 'ETHUSDC',
            'interval': '15m',
            'lookback': '7d',
            'general_timeperiod': 14,
            'rsi_timeperiod': 14,
            'rsi_sell': 70,
            'rsi_buy': 30,
            'cci_timeperiod': 20,
            'cci_sell': 70,
            'cci_buy': 30,
            'mfi_timeperiod': 14,
            'mfi_sell': 70,
            'mfi_buy': 30,
            'macd_timeperiod': 12,
            'macd_signalperiod': 9,
            'bollinger_timeperiod': 20,
            'bollinger_nbdev': 2,
            'stoch_k_timeperiod': 14,
            'stoch_d_timeperiod': 3,
            'stoch_rsi_timeperiod': 14,
            'stoch_rsi_k_timeperiod': 3,
            'stoch_rsi_d_timeperiod': 3,
            'ema_fast_timeperiod': 9,
            'ema_slow_timeperiod': 21,
            'psar_acceleration': 0.02,
            'psar_maximum': 0.2,
            'atr_timeperiod': 14,
            'di_timeperiod': 14,
            'adx_timeperiod': 14,
        }
        
        form = TechnicalAnalysisSettingsForm(data=data, instance=self.analysis_settings)
        self.assertTrue(form.is_valid())
        form.save()
        self.analysis_settings.refresh_from_db()

        self.assertEqual(self.analysis_settings.symbol, 'ETHUSDC')
        self.assertEqual(self.analysis_settings.interval, '15m')
        self.assertEqual(self.analysis_settings.lookback, '7d')

    def test_form_invalid_data(self):
        data = {
            'symbol': 'BTCUSDC',
            'interval': '1h',
            'lookback': '1d',
            'general_timeperiod': 'invalid',
            'rsi_timeperiod': 14,
            'rsi_sell': 70,
            'rsi_buy': 30,
            'cci_timeperiod': 20,
            'cci_sell': 70,
            'cci_buy': 30,
            'mfi_timeperiod': 14,
            'mfi_sell': 70,
            'mfi_buy': 30,
            'macd_timeperiod': 12,
            'macd_signalperiod': 9,
            'bollinger_timeperiod': 20,
            'bollinger_nbdev': 2,
            'stoch_k_timeperiod': 14,
            'stoch_d_timeperiod': 3,
            'stoch_rsi_timeperiod': 14,
            'stoch_rsi_k_timeperiod': 3,
            'stoch_rsi_d_timeperiod': 3,
            'ema_fast_timeperiod': 9,
            'ema_slow_timeperiod': 21,
            'psar_acceleration': 0.02,
            'psar_maximum': 0.2,
            'atr_timeperiod': 14,
            'di_timeperiod': 14,
            'adx_timeperiod': 14,
        }
        
        form = TechnicalAnalysisSettingsForm(data=data, instance=self.analysis_settings)
        self.assertFalse(form.is_valid())
        self.assertIn('general_timeperiod', form.errors)

    def test_form_field_widgets(self):
        form = TechnicalAnalysisSettingsForm(instance=self.analysis_settings)
        self.assertIn('class="form-control w-100"', str(form['symbol']))
        self.assertIn('class="form-control w-100"', str(form['rsi_timeperiod']))
        self.assertIn('class="form-control w-100"', str(form['lookback']))