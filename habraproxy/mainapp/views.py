from django.shortcuts import HttpResponse
from requests import get


def proxy_view(request, url):
    raw_html = get('https://habr.com/' + url).text
    html = raw_html.replace('href="https://habr.com/', 'href="http://{}/'.format(request.get_host()))
    return HttpResponse(html)
