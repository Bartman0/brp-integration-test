from datetime import datetime, timedelta


def number_of_days_back_in_time_as_iso(days: int):
    return (datetime.today() - timedelta(days)).strftime("%Y-%m-%d")
