from django_cron import CronJobBase, Schedule
from fomo_sapiens.utils.logs_utils import (
    send_daily_logs,
    clear_logs
)
from utils.hunter_logic import (
    run_all_1h_hunters,
    run_all_4h_hunters,
    run_all_1d_hunters
)

class HourlyCronHunterJob(CronJobBase):
    schedule = Schedule(run_every_mins=60)  # co 60 minut
    code = 'hunter.hourly_cron_job'

    def do(self):
        run_all_1h_hunters()

class FourHoursCronHunterJob(CronJobBase):
    schedule = Schedule(run_every_mins=240)  # co 240 minut (4 godziny)
    code = 'hunter.four_hourly_cron_job'

    def do(self):
        run_all_4h_hunters()

class DailyCronHunterJob(CronJobBase):
    schedule = Schedule(run_every_mins=1440)  # codziennie
    code = 'hunter.daily_cron_job'

    def do(self):
        run_all_1d_hunters()
        send_daily_logs()
        clear_logs()