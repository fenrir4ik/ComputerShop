from dateutil.relativedelta import relativedelta
from django.utils import timezone

# Product images defaults
DEFAULT_PRODUCT_IMAGE = 'product/default_product.png'
PRODUCT_IMAGE_MAX_AMOUNT = 5

# Price history settings
PH_START = timezone.now() - timezone.timedelta(days=365)
PH_PERIOD = 'month'

# Recommender service settings
# Defines the start of evaluating product history
REC_START = timezone.now() - relativedelta(month=3)
# Defines the period by which the history is divided
REC_PERIOD = 'week'
# Defines the constant H in softsign function
REC_SOFTSIGN_H = 10
# Defines default correlation for product
REC_DEFAULT_CORRELATION = 0.01
# Defines fading cycles number
REC_FADING_CYCLES = 12
# Defines single fading cycle duration
REC_FADING_CYCLE_DURATION = timezone.timedelta(weeks=1)
