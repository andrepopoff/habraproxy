from django.test import TestCase
from bs4 import BeautifulSoup

from mainapp.views import delete_script_and_style_tags, replace_words_in_html, create_bs4_obj, add_tms, proxy_view


class DeleteTagsTest(TestCase):
    """
    Tests for delete_script_and_style_tags func in mainapp/views.py
    """
    def setUp(self):
        self.soup_obj1 = BeautifulSoup('', 'lxml')
        self.soup_obj2 = BeautifulSoup('', 'lxml')

    def test_what_return(self):
        """
        Check what function returns
        """
        self.assertEqual(delete_script_and_style_tags(self.soup_obj1), None)

    def test_with_valid_func_param(self):
        """
        Check how the function changes the bs4 object when receiving valid parameter
        """
        delete_script_and_style_tags(self.soup_obj1)

        # Check that the soup_obj1 has not changed.
        self.assertEqual(self.soup_obj1, self.soup_obj2)

        soup_obj1 = BeautifulSoup('<script></script><style></style>', 'lxml')
        soup_obj2 = BeautifulSoup('<script></script><style></style>', 'lxml')
        delete_script_and_style_tags(soup_obj1)

        # Check that the soup_obj1 has changed.
        self.assertNotEqual(soup_obj1, soup_obj2)

        # Verify that correct data is returned after removing tags.
        delete_script_and_style_tags(soup_obj2)
        self.assertEqual(soup_obj2, BeautifulSoup('<html><head></head></html>', 'lxml'))

    def test_with_invalid_func_param(self):
        """
        Check how the function works when receiving invalid parameter
        """
        params = [1, 'some text', ['list'], max, {'mutable'}]
        params_copy = params.copy()

        for idx, param in enumerate(params):
            self.assertEqual(delete_script_and_style_tags(param), None)
            self.assertEqual(param, params_copy[idx])


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
        # HTML without script ans style tags
        html_without_scripts = '<h1>Hello world</h1>'
        soup_obj = BeautifulSoup(html_without_scripts, 'lxml')
        new_soup = create_bs4_obj(html_without_scripts)
        self.assertEqual(new_soup, soup_obj)

        # HTML with script tag
        html_with_scripts = '<h1>Hello world</h1><script>text</script>'
        soup_obj = BeautifulSoup(html_with_scripts, 'lxml')
        new_soup = create_bs4_obj(html_with_scripts)
        self.assertNotEqual(new_soup, soup_obj)

        # HTML with style tag
        html_with_styles = '<h1>Hello world</h1><style>text</style>'
        soup_obj = BeautifulSoup(html_with_styles, 'lxml')
        new_soup = create_bs4_obj(html_with_styles)
        self.assertNotEqual(new_soup, soup_obj)

    def test_with_invalid_param(self):
        """
        Check how the function works when receiving invalid parameter instead of string
        """
        params = [1, 2.0, {'mutable'}, ['some list'], max]
        for param in params:
            new_soup = create_bs4_obj(param)
            self.assertEqual(new_soup, BeautifulSoup('', 'lxml'))


