from django.test import TestCase
from django.shortcuts import HttpResponse
from django.test.client import RequestFactory
from bs4 import BeautifulSoup

from mainapp.views import delete_tags, replace_words_in_html, create_bs4_obj, add_tms, proxy_view


class DeleteTagsTest(TestCase):
    """
    Tests for delete_tags func in mainapp/views.py
    """
    def setUp(self):
        self.soup_obj1 = BeautifulSoup('', 'lxml')
        self.soup_obj2 = BeautifulSoup('', 'lxml')

    def test_what_returns(self):
        """
        Check what function returns
        """
        self.assertEqual(delete_tags(self.soup_obj1, ['script']), None)

    def test_with_valid_func_params(self):
        """
        Check how the function changes the bs4 object when receiving valid parameter
        """
        delete_tags(self.soup_obj1, ['script'])

        # Check that the soup_obj1 has not changed.
        self.assertEqual(self.soup_obj1, self.soup_obj2)

        soup_obj1 = BeautifulSoup('<script></script><style></style>', 'lxml')
        soup_obj2 = BeautifulSoup('<script></script><style></style>', 'lxml')
        delete_tags(soup_obj1, ['script'])

        # Check that the soup_obj1 has changed.
        self.assertNotEqual(soup_obj1, soup_obj2)

        # Verify that correct data is returned after removing tags.
        delete_tags(soup_obj2, ['script', 'style'])
        self.assertEqual(soup_obj2, BeautifulSoup('<html><head></head></html>', 'lxml'))

    def test_with_invalid_func_params(self):
        """
        Check how the function works when receiving invalid parameter
        """

        # If something else came in instead of the soup object
        instead_of_soup_obj = [1, 'some text', ['list'], max, {'mutable'}, True]
        instead_of_soup_obj_copy = instead_of_soup_obj.copy()

        for idx, param in enumerate(instead_of_soup_obj):
            self.assertEqual(delete_tags(param, ['script']), None)
            self.assertEqual(param, instead_of_soup_obj_copy[idx])

        # If something else came in instead of the list of the tag names
        instead_of_tag_names = [1, 'some text', max, {'mutable'}, True]
        instead_of_tag_names_copy = instead_of_tag_names.copy()

        for idx, param in enumerate(instead_of_tag_names):
            self.assertEqual(delete_tags(self.soup_obj1, param), None)
            self.assertEqual(param, instead_of_tag_names_copy[idx])


class ReplaceWordsTest(TestCase):
    """
    Tests for replace_words_in_html func in mainapp/views.py
    """
    def setUp(self):
        self.html = '<h1>Hello world</h1>'
        self.soup_obj = BeautifulSoup(self.html, 'lxml')
        self.changed_words = {}
        self.string = self.soup_obj.string

    def test_what_func_returns(self):
        """
        Check what function returns
        """
        # Check the type of response function
        new_html = replace_words_in_html(self.string, self.changed_words, self.html)
        self.assertEqual(type(new_html), type(self.html))

    def test_without_six_letter_words(self):
        """
        Check answer if html does not contain 6 letter words
        """
        new_html = replace_words_in_html(self.string, self.changed_words, self.html)
        self.assertEqual(new_html, self.html)

    def test_with_six_letter_words(self):
        """
        Check answer if html contains 6 letter words
        """
        html = '<h1>Friends friend</h1>'
        soup_obj = BeautifulSoup(html, 'lxml')
        changed_html = '<h1>Friends friend™</h1>'
        new_html = replace_words_in_html(soup_obj.string, self.changed_words, html)
        self.assertEqual(new_html, changed_html)


class CreateBsObjectTest(TestCase):
    """
    Tests for create_bs4_obj func in mainapp/views.py
    """
    def test_what_func_returns(self):
        """
        Check what function returns
        """
        # HTML without script and style tags
        html_without_scripts = '<h1>Hello world</h1>'
        soup_obj = BeautifulSoup(html_without_scripts, 'lxml')
        new_soup = create_bs4_obj(html_without_scripts)
        self.assertEqual(new_soup, soup_obj)

        # HTML with script tag
        html_with_scripts = '<h1>Hello world</h1><script>text</script>'
        soup_obj = BeautifulSoup(html_with_scripts, 'lxml')
        new_soup = create_bs4_obj(html_with_scripts, scripts=False)
        self.assertNotEqual(new_soup, soup_obj)

        # HTML with style tag
        html_with_styles = '<h1>Hello world</h1><style>text</style>'
        soup_obj = BeautifulSoup(html_with_styles, 'lxml')
        new_soup = create_bs4_obj(html_with_styles, styles=False)
        self.assertNotEqual(new_soup, soup_obj)

    def test_with_invalid_param(self):
        """
        Check how the function works when receiving invalid parameter instead of string
        """

        # If instead of html string came another data type
        instead_of_html_string = [1, 2.0, {'mutable'}, ['some list'], max]
        for param in instead_of_html_string:
            new_soup = create_bs4_obj(param)
            self.assertEqual(new_soup, BeautifulSoup('', 'lxml'))

        # If instead of scripts or styles parameters came another data type
        wrong_data = [1, 2.0, {'mutable'}, ['some list'], max]
        for param in wrong_data:
            new_soup = create_bs4_obj('<h1>Hello world</h1><script>text</script>', scripts=param, styles=param)
            self.assertEqual(new_soup, BeautifulSoup('<h1>Hello world</h1><script>text</script>', 'lxml'))


class AddTMsTest(TestCase):
    """
    Tests for add_tms func in mainapp/views.py
    """
    def test_returned_data(self):
        """
        Checks that function returns
        """

        # HTML without 6 letter words
        html_without_six_letter_words = '<h1>Hello world</h1>'
        new_html = add_tms(html_without_six_letter_words)
        self.assertEqual(new_html, html_without_six_letter_words)

        # HTML with 6 letter words
        html_with_six_letter_words = '<h1>Friend друзья</h1>'
        new_html = add_tms(html_with_six_letter_words)
        self.assertEqual(new_html, '<h1>Friend™ друзья™</h1>')

        # HTML with same 6 letter words in <h1> and <script>
        html = '<h1>Friend друзья</h1><script>Friend друг</script><style>друзья friends</style>'
        new_html = add_tms(html)
        self.assertEqual(new_html, '<h1>Friend™ друзья™</h1><script>Friend друг</script><style>друзья friends</style>')


class ProxyViewTest(TestCase):
    """
    Tests for proxy_view func in mainapp/views.py
    """
    def setUp(self):
        self.factory = RequestFactory()

    def test_returned_type(self):
        """
        Checks that function returns
        """
        request = self.factory.get('/')
        self.assertEqual(type(proxy_view(request, '/')), type(HttpResponse('')))
