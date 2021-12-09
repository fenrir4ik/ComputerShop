import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.middleware.csrf import get_token

@login_required
def index(request):
    ses_id = request.session.session_key
    token = get_token(request)

    cookies = {'csrftoken': token,
               'sessionid': ses_id}
    headers = {'X-CSRFToken': token}
    response = requests.post('http://127.0.0.1:8000/api/shopping_cart/cart/', cookies=cookies, headers=headers)
    print(response.status_code, response.json())
    return HttpResponse(f'CSRFToken {token} SessiongId {ses_id}')