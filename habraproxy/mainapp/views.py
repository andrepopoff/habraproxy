from django.shortcuts import HttpResponse
from requests import get
from bs4 import BeautifulSoup


def set_jquery_script_tag(html, src):
    """
    Adds <script></script> tag to HTML code
    :param html: bs4.BeautifulSoup object that contains HTML code
    :param src: the value for the <script> 'src' attribute
    """
    try:
        jquery_script = html.new_tag('script')
        jquery_script.attrs['type'] = 'text/javascript'
        jquery_script.attrs['src'] = src
    except AttributeError:
        print('"html" parameter is not a bs4 object')
    else:
        try:
            html.head.append(jquery_script)
        except AttributeError:
            html.append(jquery_script)


def proxy_view(request, url):
    """
    The view that displays pages of the site https://habr.com/.
    Appends ™ to all 6 letter words
    """
    source_html = get('https://habr.com/' + url).text
    html_with_right_urls = source_html.replace('href="https://habr.com/', 'href="http://{}/'.format(request.get_host()))

    # I had to change the code for the plus signs, because they were displayed incorrectly
    html_with_right_pluses = html_with_right_urls.replace('&plus;', '&#43;')
    html = BeautifulSoup(html_with_right_pluses, 'lxml')

    # Just in case, added the jQuery CDN script to HTML
    set_jquery_script_tag(html, 'https://code.jquery.com/jquery-3.1.1.js')

    # Added jQuery script to HTML that adds ™ to 6 letter words
    set_jquery_script_tag(html, '/static/js/addTMs.js')
    return HttpResponse(str(html))
