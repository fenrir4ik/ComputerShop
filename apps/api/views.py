from django.shortcuts import render
from django.views import View

from apps.api.utils import get_current_api_folder

#TODO get_current_api_folder прописать что бы можно было получить api_user надпись на странице list user
class SingleApiList(View):
    template_name = 'api/api_list.html'
    urlpatterns = None

    def get(self, request, *args, **kwargs):
        absolute_uri = request.build_absolute_uri()
        current_api_folder = get_current_api_folder(request)
        api_dict = {}
        for urlpattern in self.urlpatterns:
            key = urlpattern.pattern._route.replace('/', '').capitalize() + ' Api'
            api_dict[key] = absolute_uri+urlpattern.pattern._route
        return render(request, self.template_name, {'api_dict': api_dict, 'current_api_folder': current_api_folder,'api_root': '/api/'})


# class ApiList(TemplateView):
#     template_name = "api/api_list.html"
#
# def api_list(request):
#     context = {'data': 228}
#     return render(request,'api/api_list.html', context)