from django.shortcuts import HttpResponse


def proxy_view(request, url):
    html = '<h1>Hello world</h1>'
    return HttpResponse(html)
