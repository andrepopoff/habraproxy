import re

from django.shortcuts import HttpResponse
from requests import get
from bs4 import BeautifulSoup


def delete_tags(soup_obj, tag_names=None):
    """
    This function removes tags from the bs4.BeautifulSoup object.

    :param soup_obj: bs4.BeautifulSoup object
    :param tag_names: list with tag names to remove
    :return: None
    """
    try:
        if tag_names and isinstance(tag_names, list):
            for tag in soup_obj(tag_names):
                tag.decompose()
        else:
            print('Invalid "tag_names" parameter!')
    except (TypeError, AttributeError):
        print('Parameter "soup_obj" is not equal to bs4.BeautifulSoup object')


def replace_words_in_html(text, changed_words, html):
    """
    This function finds words of 6 letters and adds ™ to them.
    Example: letter --> letter™

    :param text: bs4.element.NavigableString or bs4.element.text
    :param changed_words: set of words that have already been replaced
    :param html: string containing HTML code
    :return: changed string containing HTML code
    """
    try:
        words_of_six_letters = re.findall(r'\b(\w{6})\b', text)
        for word in words_of_six_letters:
            if word not in changed_words and not word.replace('.', '', 1).isdigit():
                html = re.sub(r'\b({})\b'.format(word), word + '™', html)
                changed_words.add(word)
    except (AttributeError, TypeError):
        print('One of the parameters of the function of the wrong type')
    finally:
        return html


def create_bs4_obj(html, scripts=True, styles=True):
    """
    This function creates a bs4.BeautifulSoup object from the string

    :param html: string containing HTML code
    :param scripts: if False, the <script> tags will be removed
    :param styles: if False, the <style> tags will be removed
    :return: bs4.BeautifulSoup object
    """
    try:
        soup = BeautifulSoup(html, 'lxml')
        scripts or delete_tags(soup, ['script'])
        styles or delete_tags(soup, ['style'])
    except TypeError:
        print('Expected string or bytes-like object in html param')
        soup = BeautifulSoup('', 'lxml')

    return soup


def add_tms(html):
    """
    This function prepares data for processing and adds ™ to all 6 letter words.

    :param html: string containing HTML code
    :return: changed string containing HTML code
    """
    soup = create_bs4_obj(html, scripts=False, styles=False)
    changed_words = set()

    for tag in soup.find_all(True):
        if tag.string:
            html = replace_words_in_html(tag.string, changed_words, html)
        elif tag.text:
            html = replace_words_in_html(tag.text, changed_words, html)

    return html


def proxy_view(request, url):
    """
    The view that displays pages of the site https://habr.com/.
    Appends ™ to all 6 letter words
    """
    source_html = get('https://habr.com/' + url).text
    html = add_tms(source_html)
    soup = create_bs4_obj(html, styles=False)
    html_with_right_urls = str(soup).replace('href="https://habr.com/', 'href="http://{}/'.format(request.get_host()))

    # I had to change the code for the plus signs, because they were displayed incorrectly
    html_with_right_pluses = html_with_right_urls.replace('&amp;plus;', '&#43;')
    return HttpResponse(html_with_right_pluses)
