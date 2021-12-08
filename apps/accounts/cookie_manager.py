from django.middleware.csrf import get_token


class CookieManager:
    @staticmethod
    def get_cookies_dict(request):
        ses_id = request.session.session_key
        token = get_token(request)
        return {'csrftoken': token, 'sessionid': ses_id}
