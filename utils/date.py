from django.utils import timezone


def get_month_from_range(start, end):
    return dict.fromkeys((start + timezone.timedelta(_)).strftime("%Y-%m-01") for _ in range((end - start).days))
