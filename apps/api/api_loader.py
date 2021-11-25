import datetime

from django.db import transaction, DatabaseError
from django.utils import timezone

from apps.api.models import HttpMethod, ApiPackage, Endpoint, EndpointMethod
from apps.api.settings import DEFAULT_API_PACKAGE_NAME, DEFAULT_API_NAME, DEFAULT_API_ROOT, \
    DEFAULT_API_REGISTER_CLEAR_TIME


class ApiLoader:
    """
    # Steps to include API in project:
    # 1. Set app name = 'apps.api.api_name' in apps/api/api_name/apps.py       REQUIRED
    # 2. Add app_name variable into apps/api/api_name/urls.py                  OPTIONAL WILL BE SET TO DEFAULT IF NONE
    # 3. Add app name in installed apps in project/settings.py                 REQUIRED
    # 4. Implement APIBaseView.document from apps/api/views.py                 OPTIONAL WILL BE SET TO DEFAULT IF NONE

    api_data structure:
    api_data[api_package_name] = [{name: string, url: string, doc: dict}...]
    """
    api_data = {}

    @staticmethod
    def load_api(urlpatterns, **kwargs):
        for api_package in urlpatterns:
            if api_package.__dict__.get('urlconf_name') is None:
                # case when api_package is view in current app like following
                # path('', ApiRepository.as_view(), name='API Repository')
                continue
            package_name = ApiLoader.get_package_name(api_package)
            package_url = ApiLoader.get_package_url(api_package)
            if package_name is None:
                # app.urls.app_name is not set
                package_name = DEFAULT_API_PACKAGE_NAME
            if package_name not in ApiLoader.api_data:
                ApiLoader.api_data[package_name] = []

            for single_api in api_package.urlconf_name.urlpatterns:
                if not single_api.pattern._is_endpoint or \
                        len(single_api.callback.__dict__.keys()) <= 1:
                    # if path has include() in it or view is not API
                    continue
                api_name = ApiLoader.get_api_name(single_api)
                api_url = ApiLoader.get_api_path(single_api, package_url)
                api_documentation = None
                try:
                    api_documentation = ApiLoader.get_api_documentation(single_api, api_url)
                except:
                    # api documentation is not implemented
                    pass
                finally:
                    # api documentation is not implemented or API is not inherited from APIBaseView
                    if not api_documentation:
                        api_documentation = {method: {'in': {}, 'out': {}} for method in
                                             single_api.callback.cls.http_method_names if method != 'options'}
                ApiLoader.api_data[package_name].append(
                    {'name': api_name, 'url': api_url.replace('<int:pk>', '0'), 'doc': api_documentation})
        ApiLoader.update_repository(ApiLoader.api_data, **kwargs)

    @staticmethod
    def update_repository(api_data, **kwargs):
        """
        :param api_data: dict[api_package_name] = [{name: string, url: string, doc: dict} ...]
        :param kwargs: dict, clear_db key if set to true perform database clear with default clear time delta
                       Clearing db is used to delete old api older then timezone.now() - timedelta
                       In such way old api will be removed from repository on startup, but an API with
                       appropriate time which not included into the project or have improper url settings
                       are still available in repository, and will be used for display with not available status
        :return: None
        """
        if kwargs.get('clear_db', False):
            time_bound = timezone.now() - datetime.timedelta(seconds=DEFAULT_API_REGISTER_CLEAR_TIME)
            Endpoint.objects.filter(date_updated__lt=time_bound).all().delete()
            ApiPackage.objects.filter(endpoint=None).delete()
        for package_name, endpoints in api_data.items():
            for endpoint in endpoints:
                endpoint_name = endpoint.get("name")
                endpoint_url = endpoint.get("url")
                endpoint_documentation = endpoint.get("doc")
                if endpoint_documentation is None:
                    continue
                for method, doc in endpoint_documentation.items():
                    try:
                        with transaction.atomic():
                            http_method, created = HttpMethod.objects.get_or_create(method_name=method)
                            api_package, created = ApiPackage.objects.get_or_create(package_name=package_name)
                            endpoint = Endpoint.objects.filter(endpoint_url=endpoint_url).first()

                            package_to_delete = None
                            # is there is no endpoint with this unique url
                            if endpoint is None:
                                # create endpoint and set all data
                                endpoint = Endpoint(endpoint_name=endpoint_name, endpoint_url=endpoint_url,
                                                    package=api_package)
                            else:
                                # there is an endpoint with url endpoint_url
                                # save previous package for delete attempt
                                package_to_delete = endpoint.package
                                # change data to current package and change endpoint name to current
                                endpoint.package = api_package
                                endpoint.endpoint_name = endpoint_name
                            endpoint.save()

                            endpoint_method, created = EndpointMethod.objects.get_or_create(method=http_method,
                                                                                            endpoint=endpoint)
                            endpoint_method.in_params = doc.get('in')
                            endpoint_method.out_params = doc.get('out')
                            endpoint_method.save()
                            # try to delete previous endpoint package if it was changed
                            if package_to_delete is not None:
                                ApiPackage.objects.filter(package_name=package_to_delete.package_name,
                                                          endpoint=None).delete()
                    except DatabaseError as ex:
                        print(ex)

    @staticmethod
    def get_package_name(api_package):
        return api_package.__dict__.get('app_name')

    @staticmethod
    def get_package_url(api_package):
        return api_package.pattern._route

    @staticmethod
    def get_api_name(api):
        return api.name if api.name is not None else DEFAULT_API_NAME

    @staticmethod
    def get_api_path(api, package_url):
        return DEFAULT_API_ROOT + package_url + api.pattern._route

    @staticmethod
    def get_api_documentation(api, api_path):
        # if link is details link, return details document (details=True)
        return api.callback.cls.document(details=True) if '<int:pk>' in api_path else api.callback.cls.document()
