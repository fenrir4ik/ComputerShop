from __future__ import absolute_import, unicode_literals

from celery import shared_task

from services.recommender_service import RecommenderService


@shared_task
def products_rating_update():
    recommender_service = RecommenderService()
    recommender_service.fade_products_rating()
