from apps.api.settings import DEFAULT_API_PACKAGE_NAME, DEFAULT_API_NAME, DEFAULT_API_ROOT
import json


class ApiLoader:
    api_data = {}

    @staticmethod
    def load_api(urlpatterns):
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

            print('\n' + package_name)
            for single_api in api_package.urlconf_name.urlpatterns:
                if not single_api.pattern._is_endpoint or \
                        len(single_api.callback.__dict__.keys()) <= 1:
                    # if path has include() in it or view is not API
                    continue
                api_name = ApiLoader.get_api_name(single_api)
                api_path = ApiLoader.get_api_path(single_api, package_url)
                try:
                    api_documentation = ApiLoader.get_api_documentation(single_api, api_path)
                except:
                    # api documentation is not implemented
                    # TODO ADD DEFAULT DICT ADD THROUGH HTTP_REQUEST_METHODS {in: out:}
                    continue
                print(f'{api_name=}, {api_path=}, api_methods={api_documentation.keys()}')

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