def create_api_request_url(request, reverse):
    return 'http://' + request.get_host() + reverse
