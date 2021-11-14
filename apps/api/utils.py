# get_full_path() returns api_root/current_api_folder/api
def get_current_api_folder(request):
    path_items = request.get_full_path().strip('/').split('/')
    name = path_items[1].replace('_', ' ').title()
    if len(path_items) >= 2:
        path = f"/{'/'.join(path_items[:2])}/"
        return {'name': name, 'link': path}
    else:
        return dict.fromkeys(['name', 'link'])

def get_methods_from_url(urlpattern):
    ALLOWED_HTTP_METHODS = {'GET': '#68b641',
                            'POST': '#337ab7',
                            'PUT': '#F1C40F',
                            'PATCH': '#E67E22',
                            'DELETE': '#d9534f'}
    api_methods = []
    modelset_actions = getattr(urlpattern.callback, 'actions', None)
    if modelset_actions:
        api_methods+=modelset_actions.keys()
    else:
        api_class = getattr(urlpattern.callback, 'cls', None)
        if api_class:
            api_methods += api_class.http_method_names
    list_of_methods = []
    for name, color in ALLOWED_HTTP_METHODS.items():
        list_of_methods.append((name.lower() in api_methods, name, color))
    return list_of_methods