import unittest
from unittest.mock import MagicMock
import pandas as pd
from datetime import datetime as dt
from analysis.utils.report_utils import generate_ta_report_email

class TestGenerateTAReportEmail(unittest.TestCase):

    def test_generate_ta_report_email(self):
        settings_mock = MagicMock()
        settings_mock.df_last_fetch_time = dt(2025, 2, 17, 10, 30, 0)
        settings_mock.symbol = "BTC/USDC"
        settings_mock.interval = "1m"
        settings_mock.lookback = 30
        settings_mock.rsi_timeperiod = 14
        settings_mock.rsi_buy = 30
        settings_mock.rsi_sell = 70

        df_mock = pd.DataFrame({
            'open_time': [dt(2025, 2, 17, 10, 30, 0)],
            'close_time': [dt(2025, 2, 17, 10, 31, 0)],
            'close': [10000],
            'volume': [200],
            'rsi': [30],
            'cci': [50],
            'mfi': [40],
            'macd': [0.5],
            'macd_signal': [0.3],
        })

        subject, content = generate_ta_report_email(settings_mock, df_mock)

        self.assertTrue(subject.startswith("Technical Analysis report"))
        self.assertIn("symbol: BTC/USDC", content)
        self.assertIn("rsi_latest_data: 30", content)
        self.assertIn("rsi_buy: 30", content)
        self.assertIn("close_latest_data: 10000", content)

if __name__ == "__main__":
    unittest.main()