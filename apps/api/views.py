from abc import ABC, abstractmethod
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class ApiRepository(APIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'api/api_repository.html'

    def get(self, request):
        data = ''
        return Response({'data': data})


class APIBaseView(ABC):
    """
    Child class should implement document and set doc to its proper description
    Documentation dict will be returned for methods available in http_method_names from API class
    If class has no http_method_names in it, doc will be empty
    After implementation call return super(class_name, cls).document()
    For proper work API classes with details options should have **kwargs in it
    Doc example:
    {
        'get': {
            'in': {'field': 'type'},
            'out': {'field': 'type'}
        },
        'post': {
            'in': {'field': 'type'},
            'out': {'field': 'type'}
        }
    }
    """
    http_method_names = []
    doc = {}

    @classmethod
    @abstractmethod
    def document(cls, **kwargs) -> dict:
        api_dict = cls.doc
        documented_methods = set(api_dict.keys())
        available_methods = set(cls.http_method_names)
        documented_available_methods = list(documented_methods & available_methods)
        description_dict = {}
        for method in documented_available_methods:
            description_dict[method] = api_dict[method]
        return description_dict
