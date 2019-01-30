from django.shortcuts import HttpResponse
from requests import get


def proxy_view(request, url):
    html = get('https://habr.com/' + url).text
    return HttpResponse(html)
