from dateutil.rrule import rrule, WEEKLY, MONTHLY, DAILY


def get_periods_from_range(start, end, period='month'):
    if period == 'month':
        return dict.fromkeys(_.strftime("%Y-%m-%d") for _ in rrule(freq=MONTHLY,
                                                                   dtstart=start,
                                                                   until=end,
                                                                   bymonthday=1))
    elif period == 'week':
        return dict.fromkeys(_.strftime("%Y-%m-%d") for _ in rrule(freq=WEEKLY,
                                                                   dtstart=start,
                                                                   until=end,
                                                                   byweekday=0))
    elif period == 'day':
        return dict.fromkeys(_.strftime("%Y-%m-%d") for _ in rrule(freq=DAILY,
                                                                   dtstart=start,
                                                                   until=end))
    else:
        raise ValueError('Given period is wrong, options: month, week, day')
