# get_full_path() returns api_root/current_api_folder/api
#TODO сильный хардкод и возвращает оно не совсем то что надо, смотреть атупт, должно возвращать директорию и пас
def get_current_api_folder(request):
    path_items = request.get_full_path().strip('/').split('/')
    name = path_items[1].replace('_', ' ').title()
    if len(path_items) >= 2:
        path = f"/{'/'.join(path_items[:2])}/"
        return {'name': name, 'link': path}
    else:
        return 'WARNING'

def get_methods_from_url(urlpattern):
    ALLOWED_HTTP_METHODS = {'GET': '#1E8449',
                            'POST': '#6495ED',
                            'PUT': '#F1C40F',
                            'PATCH': '#E67E22',
                            'DELETE': '#ff0000'}
    api_methods = []
    modelset_actions = getattr(urlpattern.callback, 'actions', None)
    if modelset_actions:
        api_methods+=modelset_actions.keys()
    else:
        api_class = getattr(urlpattern.callback, 'cls', None)
        if api_class:
            api_methods += api_class.http_method_names
    api_methods = [(name, color) for name, color in ALLOWED_HTTP_METHODS.items() if name.lower() in api_methods]
    return api_methods