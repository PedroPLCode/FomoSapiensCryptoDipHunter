import pytest
from unittest.mock import MagicMock
from pandas import DataFrame
from hunter.utils.report_utils import generate_hunter_signal_email


@pytest.fixture
def hunter_mock():
    hunter = MagicMock()
    hunter.id = 1
    hunter.symbol = "BTCUSDT"
    hunter.interval = "1m"
    hunter.lookback = 100
    hunter.comment = "Test Hunter"
    hunter.price_signals = True
    hunter.avg_close_period = 14
    hunter.vol_signals = True
    hunter.avg_volume_period = 14
    return hunter


@pytest.fixture
def df_mock():
    data = {
        "open_time": [1, 2],
        "close_time": [3, 4],
        "close": [10000, 10500],
        "volume": [200, 220],
        "rsi": [30, 35],
        "cci": [50, 55],
        "mfi": [60, 65],
        "macd": [0.5, 0.6],
        "upper_band": [1.1, 1.2],
        "middle_band": [1.0, 1.1],
        "lower_band": [0.9, 1.0],
        "stoch_k": [30, 35],
        "stoch_d": [40, 45],
        "stoch_rsi_k": [50, 55],
        "stoch_rsi_d": [60, 65],
        "ema_fast": [10000, 10050],
        "ema_slow": [9500, 9600],
        "plus_di": [20, 25],
        "minus_di": [15, 20],
        "atr": [100, 105],
        "vwap": [200, 210],
    }
    return DataFrame(data)


def test_generate_hunter_signal_email(hunter_mock, df_mock):
    averages = {
        "avg_close": 10250,
        "avg_volume": 210,
        "avg_rsi": 32.5,
        "avg_cci": 52.5,
        "avg_mfi": 62.5,
        "avg_macd": 0.55,
        "avg_macd_signal": 0.55,
        "avg_stoch_k": 32.5,
        "avg_stoch_d": 42.5,
        "avg_stoch_rsi_k": 52.5,
        "avg_stoch_rsi_d": 62.5,
        "avg_ema_fast": 10025,
        "avg_ema_slow": 9550,
        "avg_plus_di": 22.5,
        "avg_minus_di": 17.5,
        "avg_atr": 102.5,
    }
    trend = "bullish"

    result = generate_hunter_signal_email("buy", hunter_mock, df_mock, trend, averages)
    assert "Hunter 1 BTCUSDT" in result
    assert "interval: 1m" in result
    assert "lookback: 100" in result
    assert "Comment: Test Hunter" in result
    assert "Recent BUY signal" in result
    assert "close_latest_data: 10000" in result
    assert "rsi_latest_data: 30" in result
    assert "cci_latest_data: 50" in result
    assert "avg_ema_fast: 10025" in result
