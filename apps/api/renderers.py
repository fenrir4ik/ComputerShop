from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer


class CustomBrowsableAPIRenderer(BrowsableAPIRenderer):
    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)

        # get_full_path() returns api_root/current_api_folder/api
        path_items =  context['request'].get_full_path().strip('/').split('/')
        if len(path_items) > 2:
            name = path_items[1].replace('_', ' ').title()
            path = f"/{'/'.join(path_items[:2])}/"
            context['current_api_folder'] = {'name': name, 'link': path}
        else:
            context['current_api_folder'] = 'WARNING'
        context['api_root'] = '/api/'
        return context

    def get_default_renderer(self, view):
        return JSONRenderer()

