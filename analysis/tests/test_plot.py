import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from datetime import timedelta
from analysis.utils.plot_utils import (
    plot_selected_ta_indicators,
    parse_lookback,
    validate_indicators,
    add_price_traces,
    add_ta_traces
)

class TestPlottingFunctions(unittest.TestCase):

    @patch('fomo_sapiens.utils.exception_handlers.exception_handler')
    @patch('analysis.utils.calc_utils.is_df_valid')
    @patch('plotly.graph_objects.Figure')
    @patch('plotly.io.write_image')
    def test_plot_selected_ta_indicators(self, mock_write_image, mock_figure, mock_is_df_valid, mock_exception_handler):
        settings = MagicMock()
        settings.selected_plot_indicators = ['rsi', 'macd']
        settings.lookback = '10d'
        df = pd.DataFrame({'open_time': pd.date_range(start='2022-01-01', periods=100, freq='D'),
                           'close': [1]*100,
                           'rsi': [50]*100,
                           'macd': [0]*100,
                           'macd_signal': [0]*100})

        mock_is_df_valid.return_value = True
        mock_write_image.return_value = None
        mock_figure.return_value = MagicMock()

        result = plot_selected_ta_indicators(df, settings)

        self.assertIsInstance(result, str)
        mock_write_image.assert_called_once()

    def test_invalid_df(self):
        df = pd.DataFrame()
        settings = MagicMock()
        
        result = plot_selected_ta_indicators(df, settings)
        
        self.assertIsNone(result)

    @patch('plotly.graph_objects.Figure')
    def test_add_price_traces(self, mock_figure):
        df = pd.DataFrame({
            'open_time': pd.date_range(start='2022-01-01', periods=100, freq='D'),
            'close': [1]*100,
            'ema_fast': [1]*100,
            'ema_slow': [1]*100,
            'ma_50': [1]*100,
            'ma_200': [1]*100
        })
        indicators = ['close', 'ema', 'ma50', 'ma200']
        
        fig = MagicMock()
        add_price_traces(fig, df, indicators)
        
        self.assertEqual(fig.add_trace.call_count, 4)

    @patch('plotly.graph_objects.Figure')
    def test_add_ta_traces(self, mock_figure):
        df = pd.DataFrame({
            'open_time': pd.date_range(start='2022-01-01', periods=100, freq='D'),
            'rsi': [50]*100,
            'macd': [0]*100,
            'macd_signal': [0]*100,
            'macd_histogram': [0]*100
        })
        indicators = ['rsi', 'macd']
        settings = MagicMock(rsi_sell=70, rsi_buy=30, cci_sell=100, cci_buy=-100, mfi_sell=80, mfi_buy=20)
        
        fig = MagicMock()
        add_ta_traces(fig, df, indicators, settings)
        
        self.assertTrue(fig.add_trace.called)

    def test_parse_lookback(self):
        self.assertEqual(parse_lookback('10d'), timedelta(days=10))
        self.assertEqual(parse_lookback('3h'), timedelta(hours=3))
        self.assertEqual(parse_lookback('5m'), timedelta(minutes=5))

        with self.assertRaises(ValueError):
            parse_lookback('10y')

    def test_validate_indicators(self):
        df = pd.DataFrame({'close': [1]*100, 'rsi': [50]*100})
        indicators = ['close', 'rsi', 'macd']
        
        with self.assertRaises(ValueError):
            validate_indicators(df, indicators)