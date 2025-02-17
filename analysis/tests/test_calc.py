import unittest
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from analysis.models import TechnicalAnalysisSettings
from analysis.utils.calc_utils import (
    is_df_valid, 
    handle_ta_df_initial_praparation, 
    calculate_ta_rsi, 
    calculate_ta_cci, 
    calculate_ta_mfi, 
    calculate_ta_adx, 
    calculate_ta_atr,
    calculate_ta_averages,
    calculate_ta_indicators,
    check_ta_trend
)

@pytest.fixture
def mock_settings():
    settings = MagicMock(TechnicalAnalysisSettings)
    settings.avg_volume_period = 14
    settings.avg_rsi_period = 14
    settings.avg_cci_period = 14
    settings.avg_mfi_period = 14
    settings.avg_atr_period = 14
    settings.avg_stoch_rsi_period = 14
    settings.avg_macd_period = 14
    settings.avg_stoch_period = 14
    settings.avg_ema_period = 14
    settings.avg_di_period = 14
    settings.avg_psar_period = 14
    settings.avg_vwap_period = 14
    settings.avg_close_period = 14
    settings.rsi_sell = 70
    settings.rsi_buy = 30
    settings.adx_strong_trend = 25
    settings.adx_weak_trend = 20
    settings.adx_no_trend = 10
    return settings

def test_calculate_ta_indicators(mock_settings):
    df = pd.DataFrame({
        'volume': [1000, 1500, 1200],
        'rsi': [50, 55, 60],
        'cci': [100, 120, 130],
        'mfi': [50, 60, 70],
        'stoch_rsi_k': [0.5, 0.6, 0.7],
        'macd': [0.1, 0.2, 0.3],
        'adx': [20, 25, 30],
        'plus_di': [25, 30, 35],
        'minus_di': [10, 15, 20],
        'atr': [0.5, 0.6, 0.7],
        'psar': [0.3, 0.4, 0.5],
        'vwap': [200, 210, 220],
        'ema_fast': [180, 190, 200],
        'ema_slow': [170, 180, 190],
        'close': [2500, 2550, 2600],
    })
    
    result = calculate_ta_indicators(df, mock_settings)
    assert isinstance(result, pd.DataFrame)
    assert 'rsi' in result.columns
    assert 'cci' in result.columns

def test_calculate_ta_averages(mock_settings):
    df = pd.DataFrame({
        'volume': [1000, 1500, 1200],
        'rsi': [50, 55, 60],
        'cci': [100, 120, 130],
        'mfi': [50, 60, 70],
        'atr': [0.5, 0.6, 0.7],
        'stoch_rsi_k': [0.5, 0.6, 0.7],
        'macd': [0.1, 0.2, 0.3],
        'stoch_k': [0.4, 0.5, 0.6],
        'stoch_d': [0.6, 0.7, 0.8],
        'ema_fast': [180, 190, 200],
        'ema_slow': [170, 180, 190],
        'plus_di': [25, 30, 35],
        'minus_di': [10, 15, 20],
        'psar': [0.3, 0.4, 0.5],
        'vwap': [200, 210, 220],
        'close': [2500, 2550, 2600],
    })

    result = calculate_ta_averages(df, mock_settings)
    assert isinstance(result, dict)
    assert 'avg_rsi' in result
    assert result['avg_rsi'] == 55

def test_check_ta_trend(mock_settings):
    df = pd.DataFrame({
        'rsi': [50, 55, 60],
        'adx': [20, 25, 30],
        'plus_di': [25, 30, 35],
        'minus_di': [10, 15, 20],
        'atr': [0.5, 0.6, 0.7],
        'high': [2550, 2600, 2650],
        'low': [2500, 2550, 2600],
    })
    
    result = check_ta_trend(df, mock_settings)
    assert result in ['uptrend', 'downtrend', 'horizontal', 'none'] 
    
    df.iloc[-1]['rsi'] = 25
    result_uptrend = check_ta_trend(df, mock_settings)
    assert result_uptrend == 'uptrend'

    df.iloc[-1]['rsi'] = 75
    result_downtrend = check_ta_trend(df, mock_settings)
    assert result_downtrend == 'downtrend'

    df.iloc[-1]['adx'] = 10
    result_horizontal = check_ta_trend(df, mock_settings)
    assert result_horizontal == 'horizontal'


class TestTechnicalAnalysisFunctions(unittest.TestCase):

    @patch('analysis.utils.logger')
    def test_is_df_valid_empty_dataframe(self, mock_logger):
        df = pd.DataFrame()
        result = is_df_valid(df)
        self.assertFalse(result)
        mock_logger.error.assert_called_with('DataFrame is empty.')

    @patch('analysis.utils.logger')
    def test_is_df_valid_non_empty_dataframe(self, mock_logger):
        df = pd.DataFrame({'close': [1, 2, 3]})
        result = is_df_valid(df)
        self.assertTrue(result)
        mock_logger.error.assert_not_called()

    @patch('pandas.to_numeric')
    @patch('pandas.to_datetime')
    def test_handle_ta_df_initial_praparation(self, mock_to_datetime, mock_to_numeric):
        df = pd.DataFrame({
            'close': ['1', '2', '3'],
            'high': ['1', '2', '3'],
            'low': ['1', '2', '3'],
            'volume': ['100', '200', '300'],
            'open_time': [123, 456, 789],
            'close_time': [123, 456, 789]
        })
        settings = MagicMock()
        result_df = handle_ta_df_initial_praparation(df, settings)
        self.assertTrue(result_df.equals(df))
        
    @patch('talib.RSI')
    def test_calculate_ta_rsi(self):
        df = pd.DataFrame({'close': [1, 2, 3, 4, 5]})
        settings = MagicMock(rsi_timeperiod=14)
        with patch('talib.RSI', return_value=[50, 60, 70, 80, 90]):
            result_df = calculate_ta_rsi(df, settings)
            self.assertTrue('rsi' in result_df.columns)
            self.assertEqual(result_df['rsi'].iloc[0], 50)

    @patch('talib.CCI')
    def test_calculate_ta_cci(self):
        df = pd.DataFrame({'high': [1, 2, 3], 'low': [1, 2, 3], 'close': [1, 2, 3]})
        settings = MagicMock(cci_timeperiod=14)
        with patch('talib.CCI', return_value=[100, 110, 120]):
            result_df = calculate_ta_cci(df, settings)
            self.assertTrue('cci' in result_df.columns)
            self.assertEqual(result_df['cci'].iloc[0], 100)

    @patch('talib.MFI')
    def test_calculate_ta_mfi(self):
        df = pd.DataFrame({'high': [1, 2], 'low': [1, 2], 'close': [1, 2], 'volume': [100, 200]})
        settings = MagicMock(mfi_timeperiod=14)
        with patch('talib.MFI', return_value=[50, 60]):
            result_df = calculate_ta_mfi(df, settings)
            self.assertTrue('mfi' in result_df.columns)
            self.assertEqual(result_df['mfi'].iloc[0], 50)

    @patch('talib.ADX')
    def test_calculate_ta_adx(self):
        df = pd.DataFrame({'high': [1, 2], 'low': [1, 2], 'close': [1, 2]})
        settings = MagicMock(adx_timeperiod=14)
        with patch('talib.ADX', return_value=[25, 30]):
            result_df = calculate_ta_adx(df, settings)
            self.assertTrue('adx' in result_df.columns)
            self.assertEqual(result_df['adx'].iloc[0], 25)

    @patch('talib.ATR')
    def test_calculate_ta_atr(self):
        df = pd.DataFrame({'high': [1, 2], 'low': [1, 2], 'close': [1, 2]})
        settings = MagicMock(atr_timeperiod=14)
        with patch('talib.ATR', return_value=[1.5, 1.7]):
            result_df = calculate_ta_atr(df, settings)
            self.assertTrue('atr' in result_df.columns)
            self.assertEqual(result_df['atr'].iloc[0], 1.5)

if __name__ == '__main__':
    unittest.main()