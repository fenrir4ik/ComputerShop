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