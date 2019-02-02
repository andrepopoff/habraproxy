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
        print(self.soup_obj2)
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

