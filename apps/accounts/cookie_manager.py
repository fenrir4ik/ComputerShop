from django.middleware.csrf import get_token


class CookieManager:
    @staticmethod
    def get_auth_credentials(request):
        ses_id = request.session.session_key
        token = get_token(request)
        cookies = {'csrftoken': token,
                   'sessionid': ses_id}
        headers = {'X-CSRFToken': token}
        return {'cookies': cookies, 'headers': headers}
