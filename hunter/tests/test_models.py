from django.test import TestCase
from django.contrib.auth.models import User
from hunter.models import TechnicalAnalysisHunter, default_df
from django.utils import timezone


class TechnicalAnalysisHunterTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_create_technical_analysis_hunter(self):
        hunter = TechnicalAnalysisHunter.objects.create(
            user=self.user,
            symbol="BTCUSDC",
            interval="1h",
            lookback="1d",
            running=True,
            trend_signals=True,
            rsi_signals=False,
        )
        self.assertEqual(hunter.user.username, "testuser")
        self.assertEqual(hunter.symbol, "BTCUSDC")
        self.assertTrue(hunter.running)
        self.assertTrue(hunter.trend_signals)
        self.assertFalse(hunter.rsi_signals)

    def test_str_method(self):
        hunter = TechnicalAnalysisHunter.objects.create(user=self.user)
        self.assertEqual(str(hunter), f"Hunter settings for {self.user.username}")

    def test_df_default_value(self):
        hunter = TechnicalAnalysisHunter.objects.create(user=self.user)
        self.assertEqual(hunter.df, default_df)

    def test_df_last_fetch_time_default(self):
        hunter = TechnicalAnalysisHunter.objects.create(user=self.user)
        self.assertAlmostEqual(
            hunter.df_last_fetch_time,
            timezone.now(),
            delta=timezone.timedelta(seconds=1),
        )
