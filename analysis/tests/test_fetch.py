import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from analysis.utils.fetch_utils import (
    get_binance_api_credentials,
    create_binance_client,
    fetch_and_save_df,
    calculate_lookback_extended,
    fetch_data,
    fetch_system_status,
    fetch_server_time
)

class TestBinanceFunctions(unittest.TestCase):

    @patch('os.environ.get')
    def test_get_binance_api_credentials(self, mock_get):
        mock_get.side_effect = lambda key: 'test_api_key' if key == 'BINANCE_GENERAL_API_KEY' else 'test_api_secret'
        
        api_key, api_secret = get_binance_api_credentials()
        
        self.assertEqual(api_key, 'test_api_key')
        self.assertEqual(api_secret, 'test_api_secret')

    @patch('mymodule.Client')
    def test_create_binance_client(self, MockClient):
        mock_client = MagicMock()
        MockClient.return_value = mock_client
        
        client = create_binance_client()
        
        self.assertIsInstance(client, MagicMock)
        MockClient.assert_called_once_with('test_api_key', 'test_api_secret')

    @patch('mymodule.fetch_data')
    @patch('mymodule.TechnicalAnalysisSettings')
    def test_fetch_and_save_df(self, MockSettings, mock_fetch_data):
        settings = MockSettings.return_value
        settings.symbol = 'BTCUSDT'
        settings.interval = '1h'
        settings.df = None
        
        mock_df = pd.DataFrame({'open': [100], 'close': [105]})
        mock_fetch_data.return_value = mock_df
        
        result = fetch_and_save_df(settings)
        
        self.assertTrue(result)
        self.assertEqual(settings.df, mock_df.to_json(orient='records'))
        self.assertIsNotNone(settings.df_last_fetch_time)
        settings.save.assert_called_once()

    def test_calculate_lookback_extended(self):
        settings = MagicMock()
        settings.interval = '5m'
        
        result = calculate_lookback_extended(settings)
        
        self.assertEqual(result, '1025m')

    @patch('mymodule.Client')
    def test_fetch_data(self, MockClient):
        mock_client = MagicMock()
        MockClient.return_value = mock_client
        
        mock_klines = [
            [1609459200000, '100', '110', '90', '105', '1000', '1609459260000', '105000', 100, 50, 55, 'ignore']
        ]
        
        mock_client.get_historical_klines.return_value = mock_klines
        df = fetch_data('BTCUSDT', '1h', '2d')
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 1)
        self.assertEqual(df['close'][0], 105.0)

    @patch('mymodule.Client')
    def test_fetch_system_status(self, MockClient):
        mock_client = MagicMock()
        MockClient.return_value = mock_client
        
        mock_status = {'status': 'ok'}
        mock_client.get_system_status.return_value = mock_status
        
        status = fetch_system_status()
        
        self.assertEqual(status, mock_status)
        mock_client.get_system_status.assert_called_once()

    @patch('mymodule.Client')
    def test_fetch_server_time(self, MockClient):
        mock_client = MagicMock()
        MockClient.return_value = mock_client
        
        mock_time = {'serverTime': 1609459200000}
        mock_client.get_server_time.return_value = mock_time
        
        server_time = fetch_server_time()
        
        self.assertEqual(server_time, mock_time)
        mock_client.get_server_time.assert_called_once()

if __name__ == '__main__':
    unittest.main()