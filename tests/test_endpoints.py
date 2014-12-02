from ferrisnose import AppEngineTest
import ferris3
from ferris3 import endpoints
from protorpc import messages
from protorpc.message_types import VoidMessage
import mock


class EndpointsTest(AppEngineTest):
    def setUp(self):
        super(EndpointsTest, self).setUp()
        endpoints._endpoints = {}
        endpoints._default_endpoint_name = None

    def _load_api(self):
        api = endpoints.add('tests/data/api_config.yaml', True)
        return api

    def test_configuration(self):
        self.assertRaises(RuntimeError, endpoints.get)

        api = self._load_api()
        info = api._ApiDecorator__common_info

        assert info.canonical_name == 'Example API'
        assert info.name == 'example'
        assert info.version == 'v1'
        assert info.description == 'Ferris-based API'

        assert endpoints.default() == api
        assert endpoints.get() == api
        assert endpoints.get('example') == api
        assert endpoints.get_all() == [api]

    def test_underscore(self):
        assert endpoints.underscore("MeepDeMeep") == "meep_de_meep"

    def test_auto_service(self):
        self._load_api()
        service = endpoints.auto_service()(MeowService)
        assert service.api_info.name == 'example'
        assert service.api_info.resource_name == 'meow'

    def test_auto_method(self):

        @endpoints.auto_method
        def void_and_void_no_args(self, request):
            pass

        assert void_and_void_no_args.method_info.http_method == 'POST'
        assert void_and_void_no_args.method_info.name == 'void_and_void_no_args'
        assert void_and_void_no_args.remote.request_type == VoidMessage
        assert void_and_void_no_args.remote.response_type == VoidMessage

        @endpoints.auto_method(returns=ExampleMessageOne)
        def example_and_example_no_args(self, request=(ExampleMessageOne,)):
            pass

        assert example_and_example_no_args.remote.request_type == ExampleMessageOne
        assert example_and_example_no_args.remote.response_type == ExampleMessageOne

        @endpoints.auto_method
        def void_with_args(self, request, str_arg=(str,), int_arg=(int,), float_arg=(float,), bool_arg=(bool,), default_arg=(str, 'def')):
            assert default_arg == 'def'

        assert isinstance(void_with_args.remote.request_type.str_arg, messages.StringField)
        assert isinstance(void_with_args.remote.request_type.float_arg, messages.FloatField)
        assert isinstance(void_with_args.remote.request_type.bool_arg, messages.BooleanField)
        assert isinstance(void_with_args.remote.request_type.int_arg, messages.IntegerField)
        assert void_with_args.remote.response_type == VoidMessage

        @endpoints.auto_method(path='{str_arg}')
        def void_with_path_args(self, request, str_arg=(str,), default_arg=(str, 'def')):
            assert default_arg == 'def'

        assert isinstance(void_with_path_args.remote.request_type.str_arg, messages.StringField)
        assert void_with_path_args.remote.response_type == VoidMessage

        def invalid_args(self, request, dict_arg=(dict,)):
            pass

        self.assertRaises(ValueError, endpoints.auto_method, invalid_args)

        # try invoking
        void_with_args(mock.Mock(), void_with_args.remote.request_type())


class MeowService(ferris3.Service):
    pass


class ExampleMessageOne(messages.Message):
    content = messages.StringField(1)
