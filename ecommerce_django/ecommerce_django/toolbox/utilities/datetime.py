from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.utils import timezone
import calendar
import pytz


class Day:

    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    DAY_LIST = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY]
    NAME_LIST = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


class DateFormatter:

    DEFAULT_FORMAT = "%Y-%m-%d"
    DEFAULT_FORMATII = "%Y.%m.%d"
    DEFAULT_FORMATIII = "%Y%m%d"
    DEFAULT_FORMATIV = "%b.%d.%Y"
    DEFAULT_FORMATV = "%d %B %Y"
    DEFAULT_FORMATVI = "%a, %d %b %Y"


class TimeFormatter:

    DEFAULT_FORMAT = "%H:%M:%S"
    DEFAULT_FORMATII = "%H:%M"
    DEFAULT_FORMATIII = "%H:%M %p"


class DateTimeFormatter:

    DEFAULT_FORMAT = "%Y-%m-%d %H:%M:%S%Z"

    DEFAULT_FORMAT2 = "%Y-%m-%d %H:%M:%S"

    DEFAULT_FORMAT3 = "%Y%m%dT%H%M%SZ"

    DEFAULT_FORMAT4 = "%Y%m%d%H%M%S%f"

    DEFAULT_FORMAT5 = "%b.%d.%Y %H:%M:%S"

    DEFAULT_FORMAT6 = "%d.%b.%Y %H:%M"


def today():
    return date.today()


def now():
    return datetime.now()


def get_day(date):
    return date.strftime("%a")


def get_day_of_week(date):
    return int(date.strftime("%w"))


def get_weekday_name(date, format="%A"):
    # %A for full name
    # %a for short name
    return date.strftime(format)


def get_week_days(week_date):
    day_of_week = get_day_of_week(week_date)
    day_of_week = 7 if day_of_week == 0 else day_of_week
    first_date = week_date - timedelta(days=day_of_week-1)
    return [first_date + timedelta(days=i) for i in range(7)]


def get_week_range(week_date, start_day=1):
    day_of_week = get_day_of_week(week_date)
    diff_days = 7 - (start_day - day_of_week)
    diff_days = 0 if day_of_week == start_day else diff_days
    first_date = week_date - timedelta(days=diff_days)
    return [first_date + timedelta(days=i) for i in range(7)]


def stringify_datetime(dt, datetime_format=DateTimeFormatter.DEFAULT_FORMAT, timezone=settings.TIME_ZONE):
    if not isinstance(dt, datetime):
        raise TypeError('%s is not datetime object' % dt)

    if timezone is not None:
        tz = pytz.timezone(timezone)
        dt = dt.astimezone(tz)

    return dt.strftime(datetime_format)


def stringify_date(d, date_format=DateFormatter.DEFAULT_FORMAT):
    if not isinstance(d, date):
        raise TypeError('%s is not date object' % d)

    return d.strftime(date_format)


def stringify_time(string_time, time_format=DateTimeFormatter.DEFAULT_FORMAT):
    if not isinstance(string_time, time):
        raise TypeError('%s is not time object' % string_time)

    return string_time.strftime(time_format)


def datetimeify_string(datetime_string, datetime_format=DateTimeFormatter.DEFAULT_FORMAT):
    return datetime.strptime(datetime_string, datetime_format)


def month_range(year, month):
    year, month = int(year), int(month)
    range = calendar.monthrange(year, month)
    return date(year, month, 1), date(year, month, range[1])


def monthdelta(months):
    return relativedelta(months=+months) if months > 0 else relativedelta(months=-months)


def week_range(week_date):
    day_of_week = get_day_of_week(week_date)
    first_date_of_week = week_date - timedelta(days=day_of_week-1)
    return first_date_of_week, first_date_of_week + timedelta(days=6)


def make_aware_datetime(year, month, day, hour, minute, second, timezone=settings.TIME_ZONE):
    return pytz.timezone(timezone).localize(datetime(year, month, day, hour, minute, second))


def aware_now():
    n = now()
    return make_aware_datetime(n.year, n.month, n.day, n.hour, n.minute, n.second)


def merge_datetime(d, t, is_aware=settings.USE_TZ):
    if is_aware:
        return make_aware_datetime(d.year, d.month, d.day, t.hour, t.minute, t.second)
    return datetime(d.year, d.month, d.day, t.hour, t.minute, t.second)


def convert_datetime_timezone(dt, tz):
    tz = pytz.timezone(tz)
    return dt.astimezone(tz)


def is_date(dt, format=DateFormatter.DEFAULT_FORMAT):
    try:
        dt = datetime.strptime(dt, format)
        return True
    except:
        return False


def is_time(dt, format=TimeFormatter.DEFAULT_FORMAT):
    try:
        dt = datetime.strptime(dt, format)
        return True
    except:
        return False


def current_timestamp():
    return int(datetime.timestamp(now()))


def timestamp_to_datetime(timestamp):
    if isinstance(timestamp, int):
        return datetime.fromtimestamp(timestamp)
    return None


def datetime_to_timestamp(date_time):
    if isinstance(date_time, datetime):
        return int(datetime.timestamp(date_time))
    return 0