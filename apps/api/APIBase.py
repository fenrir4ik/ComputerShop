import json

class APIBase:
    in_arguments = {} #in json {'agr1': 'value1', 'arg2': 'value2'}
    out_arguments = {} #out json {'out1': 'value1', 'out2': 'value2'}
    http_methods = () #http methods available {'GET', 'POST'}
    auth_required = False #auth required: True/False
    call_path = '' #uri to call

    @classmethod
    def get_api_details(cls):
        return json.dumps({
            'in_arguments': cls.__cast_args(cls.in_arguments),
            'out_arguments': cls.__cast_args(cls.out_arguments),
            'http_methods':cls.http_methods,
            'auth_required': cls.auth_required,
            'call_path': cls.call_path,
        }, separators=(',', ':'), indent=4)

    @classmethod
    def __cast_args(self, dictionary):
        result = {}
        for key, value in dictionary.items():
            if isinstance(value, dict):
                result[key] = self.__cast_args(value)
            else:
                result[key] = value.__name__ if value in (int, float, str, bool) else None
        return result