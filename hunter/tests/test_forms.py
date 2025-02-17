from django import forms
from django.test import TestCase
from hunter.forms import TechnicalAnalysisHunterForm

class TechnicalAnalysisHunterFormTest(TestCase):
    def test_form_valid_data(self):
        form_data = {
            'symbol': 'BTCUSDT',
            'interval': '1m',
            'lookback': 30,
            'comment': 'Test comment',
            'running': True,
            'general_timeperiod': 14,
            'price_signals': True,
            'avg_close_period': 14,
        }

        form = TechnicalAnalysisHunterForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form_data = {
            'symbol': '',
            'interval': '1m',
            'lookback': 30,
            'comment': 'Test comment',
            'running': True,
        }

        form = TechnicalAnalysisHunterForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('symbol', form.errors)

    def test_form_field_widgets(self):
        form = TechnicalAnalysisHunterForm()
        self.assertIsInstance(form.fields['symbol'].widget, forms.TextInput)
        self.assertIsInstance(form.fields['comment'].widget, forms.Textarea)
        self.assertIsInstance(form.fields['lookback'].widget, forms.NumberInput)
        self.assertIsInstance(form.fields['running'].widget, forms.CheckboxInput)