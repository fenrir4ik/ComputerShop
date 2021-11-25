from abc import ABC, abstractmethod

from django.db.models import F
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.models import Endpoint
from apps.api.serializers import RepositorySerializer


class ApiRepository(APIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'repository/api_repository.html'

    def get(self, request):
        queryset = Endpoint.objects.values("endpoint_name", "endpoint_url",
                                           package_name=F("package__package_name"),
                                           method_name = F("methods__method_name"),
                                           in_params = F("endpointmethod__in_params"),
                                           out_params= F("endpointmethod__out_params"))
        for i in range(len(queryset)):
            queryset[i]['index'] = i
            queryset[i]['available'] = True
        serializer = RepositorySerializer(queryset, many=True)
        return Response({'endpoints':serializer.data})


class APIBaseView(ABC):
    """
    Child class should implement document class method and set doc to its proper API description
    Documentation dict will be returned for methods available in http_method_names from API class
    If class has no http_method_names in it, doc will be empty
    Http methods in resulting documentation is a result of intersection http_method_names and doc.keys
    After document(cls, **kwargs) body return super(class_name, cls).document() required
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
