from dateutil.relativedelta import relativedelta
from django.utils import timezone

# Product images defaults
DEFAULT_PRODUCT_IMAGE = 'product/default_product.png'
PRODUCT_IMAGE_MAX_AMOUNT = 5

# Price history settings
PH_START = timezone.now() - timezone.timedelta(days=365)
PH_PERIOD = 'month'

# Recommender service settings
REC_START = timezone.now() - relativedelta(months=3)
REC_PERIOD = 'week'
REC_FADING_CYCLES = 12
REC_SOFTSIGN_H = 10
REC_DEFAULT_CORRELATION = 0.01
