from django.test import TestCase
from bs4 import BeautifulSoup

from mainapp.views import proxy_view, set_jquery_script_tag


class SetJQueryScriptTagTest(TestCase):
    """
    Tests for set_jquery_script_tag func in mainapp/views.py
    """
    def test_what_return(self):
        """
        Check what function returns
        """
        soup_obj = BeautifulSoup('', 'lxml')
        self.assertEqual(set_jquery_script_tag(soup_obj, 'some text'), None)

    def test_with_valid_html_param(self):
        """
        Check how the function changes the bs4 object when receiving valid parameters
        """
        soup_obj1 = BeautifulSoup('', 'lxml')
        soup_obj2 = BeautifulSoup('', 'lxml')
        src = 'some text'
        set_jquery_script_tag(soup_obj1, src)

        # Has the soup_obj1 really changed?
        self.assertNotEqual(soup_obj1, soup_obj2)

        # Checking the value of the bs4 object with an empty html
        self.assertEqual('<script src="{}" type="text/javascript"></script>'.format(src), str(soup_obj1))

        # Checking the value of the bs4 object with html having a <head> tag
        soup = BeautifulSoup('<head></head>', 'lxml')
        set_jquery_script_tag(soup, src)
        self.assertEqual(
            '<html><head><script src="some text" type="text/javascript"></script></head></html>'.format(src),
            str(soup)
        )

        # Checking the value of the bs4 object with html not having a <head> tag
        soup = BeautifulSoup('<h1></h1>', 'lxml')
        set_jquery_script_tag(soup, src)
        self.assertEqual(
            '<html><body><h1></h1></body></html><script src="{}" type="text/javascript"></script>'.format(src),
            str(soup)
        )

    def test_with_invalid_html_param(self):
        """
        What happens if the function gets a different type of object instead of bs4 object?
        """
        objects = ((1, 1), ('text', 'text'), (print, print), (['hello'], ['hello']))

        for obj in objects:
            obj1, obj2 = obj
            set_jquery_script_tag(obj1, 'some text')
            self.assertEqual(obj1, obj2)
            self.assertEqual(set_jquery_script_tag(obj2, 'some text'), None)
