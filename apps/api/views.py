import re

from django.shortcuts import render
from django.views import View

from apps.api.utils import get_current_api_folder

class SingleApiList(View):
    template_name = 'api/api_list.html'
    urlpatterns = None

    def get(self, request, *args, **kwargs):
        absolute_uri = request.build_absolute_uri()
        current_api_folder = get_current_api_folder(request)
        api_dict = {}
        for urlpattern in self.urlpatterns:
            api_path = urlpattern.pattern._route
            real_uri = absolute_uri + api_path
            # FOR details links like api/api_folder/instance/1/
            if '<int:pk>' in api_path:
                display_uri = absolute_uri + api_path.replace('<int:pk>', '{id}')
                api_name = api_path.replace('/', '').capitalize().replace('<int:pk>', ' Details') + ' Api'
                real_uri = real_uri.replace('<int:pk>', '0')
            # FOR simple links like api/api_folder/instance/
            else:
                display_uri = real_uri
                api_name = api_path.replace('/', '').capitalize() + ' Api'
            api_dict[api_name] = {'real_uri': real_uri, 'display_uri': display_uri}
            # else:
            #     api_path = re.findall(r'[a-zA-Z0-9]*/', urlpattern.pattern._regex)
            #     if len(api_path) >= 1:
            #         api_path = api_path[0]
            #         api_name = api_path.replace('/', '').capitalize() + ' Api'
        return render(request, self.template_name, {'api_dict': api_dict, 'current_api_folder': current_api_folder,'api_root': '/api/'})


# class ApiList(TemplateView):
#     template_name = "api/api_list.html"
#
# def api_list(request):
#     context = {'data': 228}
#     return render(request,'api/api_list.html', context)