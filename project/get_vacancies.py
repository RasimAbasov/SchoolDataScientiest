import datetime

from project.helpers.hh_loader import HHLoader


# https://github.com/hhru/api/blob/master/docs/general.md


loader = HHLoader()

start_time = datetime.datetime.now() - datetime.timedelta(days=30)
end_time = datetime.datetime.now()

while start_time <= end_time:
    interval_end = start_time + datetime.timedelta(hours=1)
    start_time_iso = start_time.isoformat(timespec='seconds')
    interval_end_iso = interval_end.isoformat(timespec='seconds')
    print(f"startTimeIso: {start_time_iso}, intervalEndIso: {interval_end_iso}")
    loader.get_all_vacancies(date_from=start_time_iso, date_to=interval_end_iso)
    start_time = interval_end

