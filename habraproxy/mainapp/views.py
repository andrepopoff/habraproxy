from django.shortcuts import HttpResponse
from requests import get
from bs4 import BeautifulSoup


def set_jquery_script_tag(html, src):
    jquery_script = html.new_tag('script')
    jquery_script.attrs['type'] = 'text/javascript'
    jquery_script.attrs['src'] = src

    try:
        html.append(jquery_script)
    except AttributeError:
        pass


def proxy_view(request, url):
    source_html = get('https://habr.com/' + url).text

    html_with_right_urls = source_html.replace('href="https://habr.com/', 'href="http://{}/'.format(request.get_host()))
    html_with_right_pluses = html_with_right_urls.replace('&plus;', '&#43;')

    html = BeautifulSoup(html_with_right_pluses, 'lxml')

    set_jquery_script_tag(html, 'https://code.jquery.com/jquery-3.1.1.js')
    set_jquery_script_tag(html, '/static/js/addTMs.js')

    return HttpResponse(str(html))
