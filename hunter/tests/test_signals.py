import pandas as pd
import unittest
from unittest.mock import MagicMock
from hunter.utils.buy_signals import (
    psar_buy_signal,
    ma50_buy_signal,
    ma200_buy_signal,
    ma_cross_buy_signal,
    check_classic_ta_buy_signal,
)
from hunter.utils.sell_signals import (
    mfi_sell_signal,
    mfi_divergence_sell_signal,
    atr_sell_signal,
    vwap_sell_signal,
    psar_sell_signal,
    ma50_sell_signal,
    ma200_sell_signal,
    ma_cross_sell_signal,
    check_classic_ta_sell_signal,
)


class TestTradingSellSignals(unittest.TestCase):

    def setUp(self):
        self.latest_data = {
            "mfi": "80",
            "close": "100",
            "atr": "1.2",
            "vwap": "95",
            "psar": "98",
            "ma_50": "105",
            "ma_200": "110",
        }
        self.averages = {"avg_close": "98", "avg_mfi": "75", "avg_atr": "1.0"}
        self.hunter_settings = MagicMock()
        self.hunter_settings.mfi_signals = True
        self.hunter_settings.mfi_sell = "70"
        self.hunter_settings.mfi_divergence_signals = True
        self.hunter_settings.atr_signals = True
        self.hunter_settings.vwap_signals = True
        self.hunter_settings.psar_signals = True
        self.hunter_settings.ma50_signals = True
        self.hunter_settings.ma200_signals = True
        self.hunter_settings.ma_cross_signals = True

    def test_mfi_sell_signal(self):
        result = mfi_sell_signal(self.latest_data, self.hunter_settings)
        self.assertTrue(result)

    def test_mfi_divergence_sell_signal(self):
        result = mfi_divergence_sell_signal(
            self.latest_data, self.averages, self.hunter_settings
        )
        self.assertTrue(result)

    def test_atr_sell_signal(self):
        result = atr_sell_signal(self.latest_data, self.averages, self.hunter_settings)
        self.assertTrue(result)

    def test_vwap_sell_signal(self):
        result = vwap_sell_signal(self.latest_data, self.hunter_settings)
        self.assertTrue(result)

    def test_psar_sell_signal(self):
        result = psar_sell_signal(self.latest_data, self.hunter_settings)
        self.assertTrue(result)

    def test_ma50_sell_signal(self):
        result = ma50_sell_signal(self.latest_data, self.hunter_settings)
        self.assertTrue(result)

    def test_ma200_sell_signal(self):
        result = ma200_sell_signal(self.latest_data, self.hunter_settings)
        self.assertTrue(result)

    def test_ma_cross_sell_signal(self):
        previous_data = {"ma_50": "106", "ma_200": "108"}
        result = ma_cross_sell_signal(
            self.latest_data, previous_data, self.hunter_settings
        )
        self.assertTrue(result)

    def test_check_classic_ta_sell_signal(self):
        with unittest.mock.patch(
            "trading_signals.trend_sell_signal", return_value=True
        ), unittest.mock.patch(
            "trading_signals.rsi_sell_signal", return_value=True
        ), unittest.mock.patch(
            "trading_signals.rsi_divergence_sell_signal", return_value=True
        ), unittest.mock.patch(
            "trading_signals.macd_cross_sell_signal", return_value=True
        ), unittest.mock.patch(
            "trading_signals.macd_histogram_sell_signal", return_value=True
        ), unittest.mock.patch(
            "trading_signals.bollinger_sell_signal", return_value=True
        ), unittest.mock.patch(
            "trading_signals.stoch_sell_signal", return_value=True
        ), unittest.mock.patch(
            "trading_signals.stoch_divergence_sell_signal", return_value=True
        ), unittest.mock.patch(
            "trading_signals.stoch_rsi_sell_signal", return_value=True
        ), unittest.mock.patch(
            "trading_signals.ema_cross_sell_signal", return_value=True
        ), unittest.mock.patch(
            "trading_signals.ema_fast_sell_signal", return_value=True
        ), unittest.mock.patch(
            "trading_signals.ema_slow_sell_signal", return_value=True
        ), unittest.mock.patch(
            "trading_signals.di_cross_sell_signal", return_value=True
        ), unittest.mock.patch(
            "trading_signals.cci_sell_signal", return_value=True
        ), unittest.mock.patch(
            "trading_signals.cci_divergence_buy_signal", return_value=True
        ), unittest.mock.patch(
            "trading_signals.mfi_sell_signal", return_value=True
        ), unittest.mock.patch(
            "trading_signals.mfi_divergence_sell_signal", return_value=True
        ), unittest.mock.patch(
            "trading_signals.atr_sell_signal", return_value=True
        ), unittest.mock.patch(
            "trading_signals.vwap_sell_signal", return_value=True
        ), unittest.mock.patch(
            "trading_signals.psar_sell_signal", return_value=True
        ), unittest.mock.patch(
            "trading_signals.ma50_sell_signal", return_value=True
        ), unittest.mock.patch(
            "trading_signals.ma200_sell_signal", return_value=True
        ), unittest.mock.patch(
            "trading_signals.ma_cross_sell_signal", return_value=True
        ):
            df = pd.DataFrame()
            result = check_classic_ta_sell_signal(
                df, self.hunter_settings, "uptrend", self.averages
            )
            self.assertTrue(result)


class TestTradingBuySignals(unittest.TestCase):

    def setUp(self):
        self.hunter_settings = MagicMock()
        self.latest_data = {
            "psar": "10.5",
            "close": "10.0",
            "ma_50": "9.5",
            "ma_200": "9.0",
        }
        self.previous_data = {
            "psar": "9.8",
            "close": "9.6",
            "ma_50": "9.2",
            "ma_200": "8.8",
        }

    def test_psar_buy_signal(self):
        self.hunter_settings.psar_signals = True
        result = psar_buy_signal(
            self.latest_data, self.previous_data, self.hunter_settings
        )
        self.assertTrue(result)

    def test_psar_buy_signal_no_signal(self):
        self.hunter_settings.psar_signals = False
        result = psar_buy_signal(
            self.latest_data, self.previous_data, self.hunter_settings
        )
        self.assertTrue(result)

    def test_ma50_buy_signal(self):
        self.hunter_settings.ma50_signals = True
        result = ma50_buy_signal(self.latest_data, self.hunter_settings)
        self.assertTrue(result)

    def test_ma50_buy_signal_no_signal(self):
        self.hunter_settings.ma50_signals = False
        result = ma50_buy_signal(self.latest_data, self.hunter_settings)
        self.assertTrue(result)

    def test_ma200_buy_signal(self):
        self.hunter_settings.ma200_signals = True
        result = ma200_buy_signal(self.latest_data, self.hunter_settings)
        self.assertTrue(result)

    def test_ma200_buy_signal_no_signal(self):
        self.hunter_settings.ma200_signals = False
        result = ma200_buy_signal(self.latest_data, self.hunter_settings)
        self.assertTrue(result)

    def test_ma_cross_buy_signal(self):
        self.hunter_settings.ma_cross_signals = True
        result = ma_cross_buy_signal(
            self.latest_data, self.previous_data, self.hunter_settings
        )
        self.assertTrue(result)

    def test_ma_cross_buy_signal_no_signal(self):
        self.hunter_settings.ma_cross_signals = False
        result = ma_cross_buy_signal(
            self.latest_data, self.previous_data, self.hunter_settings
        )
        self.assertTrue(result)

    def test_check_classic_ta_buy_signal(self):
        from unittest.mock import patch

        with patch(
            "my_module.get_latest_and_previus_data",
            return_value=(self.latest_data, self.previous_data),
        ), patch("my_module.is_df_valid", return_value=True), patch(
            "my_module.psar_buy_signal", return_value=True
        ), patch(
            "my_module.ma50_buy_signal", return_value=True
        ), patch(
            "my_module.ma200_buy_signal", return_value=True
        ), patch(
            "my_module.ma_cross_buy_signal", return_value=True
        ):

            result = check_classic_ta_buy_signal(
                None, self.hunter_settings, "uptrend", {}
            )
            self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
