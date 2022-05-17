from dateutil.relativedelta import relativedelta
from django.utils import timezone

# Product images constants
DEFAULT_PRODUCT_IMAGE = 'product/default_product.png'
PRODUCT_IMAGE_MAX_AMOUNT = 5

# Recommender constants
REC_T_START = timezone.now() - relativedelta(months=3)
REC_PERIOD = 'week'
REC_FADING_CYCLES = 12
