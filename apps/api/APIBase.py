import json

from rest_framework import permissions

HTTP_METHODS_AVAILABLE = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']


class APIBase:
    # TODO добавить важность поля должно быть или нет и
    #  подумать над тем что класс может иметь несколько методов post/get
    #   print(getattr(RegisterAPI, 'post').__doc__) таким способом получаем докстринг каждого класса
    __call_path = '' #url to call

    @classmethod
    def get_api_details(cls):
        return json.dumps({
            'in_arguments': None,
            'out_arguments': None,
            'http_methods': cls.__get_http_methods(),
            'permission_required': cls.__permission_required(),
            'call_path': cls.__call_path,
        }, separators=(',', ':'), indent=4)

    @classmethod
    def __parse_args(self, dictionary):
        result = {}
        for key, value in dictionary.items():
            if isinstance(value, dict):
                result[key] = self.__parse_args(value)
            else:
                result[key] = value.__name__ if value in (int, float, str, bool) else None
        return result

    @classmethod
    def __get_http_methods(cls):
        return [m.upper() for m in HTTP_METHODS_AVAILABLE if hasattr(cls, m)]

    @classmethod
    def __permission_required(cls):
        return permissions.IsAuthenticated in getattr(cls, 'permission_classes', [])

    @classmethod
    def set_call_path(cls, path):
        cls.__call_path = path
        return cls.__call_path