from django.shortcuts import render
from django.views import View

from apps.api.utils import get_current_api_folder, get_methods_from_url


class SingleApiList(View):
    template_name = 'api/api_list.html'
    urlpatterns = None

    def get(self, request, *args, **kwargs):
        absolute_uri = request.build_absolute_uri()
        current_api_folder = get_current_api_folder(request)
        api_details = {}

        for urlpattern in self.urlpatterns:
            api_path = urlpattern.pattern._route
            real_uri = absolute_uri + api_path
            api_methods = get_methods_from_url(urlpattern)

            # FOR details links like api/api_folder/instance/1/
            if '<int:pk>' in api_path:
                display_uri = absolute_uri + api_path.replace('<int:pk>', '{id}')
                real_uri = real_uri.replace('<int:pk>', '1')
            # FOR simple links like api/api_folder/instance/
            else:
                display_uri = real_uri
            api_details[urlpattern.name + ' API'] = {'real_uri': real_uri, 'display_uri': display_uri, 'api_methods': api_methods}

        return render(request, self.template_name, {'api_dict': api_details, 'current_api_folder': current_api_folder,'api_root': '/api/'})
