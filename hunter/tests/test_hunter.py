import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime as dt
from hunter.utils.hunter_logic import run_single_hunter_logic

class TestHunterLogic(unittest.TestCase):

    @patch('hunter.utils.fetch_data')
    @patch('hunter.utils.calculate_ta_indicators')
    @patch('hunter.utils.check_ta_trend')
    @patch('hunter.utils.check_classic_ta_buy_signal')
    @patch('hunter.utils.check_classic_ta_sell_signal')
    @patch('hunter.utils.send_email')
    @patch('hunter.utils.fetch_and_save_df')
    def test_run_single_hunter_logic(self, mock_fetch_and_save_df, mock_send_email, mock_sell_signal, mock_buy_signal,
                                     mock_check_trend, mock_calculate_indicators, mock_fetch_data):
        hunter = MagicMock()
        hunter.symbol = 'BTCUSDC'
        hunter.interval = '1h'
        hunter.running = True
        hunter.user.email = 'testuser@example.com'
        
        mock_fetch_data.return_value = MagicMock()
        mock_calculate_indicators.return_value = MagicMock()
        mock_check_trend.return_value = MagicMock()
        mock_buy_signal.return_value = True
        mock_sell_signal.return_value = False
        mock_send_email.return_value = None

        run_single_hunter_logic(hunter)

        mock_send_email.assert_called_once()
        mock_fetch_and_save_df.assert_called()
        mock_buy_signal.assert_called()
        mock_sell_signal.assert_not_called()