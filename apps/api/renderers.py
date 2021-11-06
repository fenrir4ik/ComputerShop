from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

from apps.api.utils import get_current_api_folder


class CustomBrowsableAPIRenderer(BrowsableAPIRenderer):
    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context['current_api_folder'] = get_current_api_folder(context['request'])
        context['api_root'] = '/api/'
        return context

    def get_default_renderer(self, view):
        return JSONRenderer()

