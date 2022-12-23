from django.http import QueryDict
from django.test import TestCase
from rest_framework.exceptions import ParseError
from helpers import get_param

class GetParamTestCase(TestCase):
    def setUp(self) -> None:
        self.query_params = QueryDict("user=User&number=123&nonum=12a3")

    def test_should_return_user(self):
        value = get_param(self.query_params, "user")
        self.assertEqual(value, "User")
    
    def test_should_return_number_as_str(self):
        value = get_param(self.query_params, "number")
        self.assertEqual(value, "123")
    
    def test_should_return_number_as_int(self):
        value = get_param(self.query_params, "number", cast=int)
        self.assertEqual(value, 123)

    def test_should_throw_parse_error_with_casting_nonum(self):
        with self.assertRaises(ParseError) as ctx:
            get_param(self.query_params, "nonum", cast=int)

    def test_should_throw_parse_error_if_param_does_not_exist(self):
        with self.assertRaises(ParseError) as ctx:
            get_param(self.query_params, "hi")

    def test_should_return_default_value_if_param_does_not_exist(self):
        default = "Yes"
        value = get_param(self.query_params, "hi", default)
        self.assertEqual(value, default)
