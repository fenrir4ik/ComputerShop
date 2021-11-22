#TODO steps to join api:
# ~in apps\api\api_name\apps.py set name = 'apps.api.api_name'      REQUIRED
# ~add app_name into apps\api\api_name\urls.py                      OPTIONAL WILL BE SET TO DEFAULT
# +in computershop\settings.py add api_name in installed apps       REQUIRED
# ~every api should implement APIBaseView from apps\api\views.py    OPTIONAL WILL BE SET TO DEFAULT DICT