from __future__ import absolute_import
from protorpc import message_types
from protorpc import messages
import endpoints
from .anodi import annotated
import inspect
import re
import yaml
import os

_endpoints = {}
_default_endpoint_name = None

base_directory = os.getcwd()


def add(config_or_file, default=False):
    """
    Add an endpoint.
    """
    global _endpoints, _default_endpoint_name

    if isinstance(config_or_file, (str, unicode)):
        config = load_config_file(config_or_file)
    else:
        config = config_or_file

    api = endpoints.api(**config)
    _endpoints[config['name']] = api

    if default:
        _default_endpoint_name = config['name']

    return api


def get(name=None):
    """Get an endpoint"""
    if not name:
        if not _default_endpoint_name:
            raise RuntimeError("No default endpoint has been configured")
        name = _default_endpoint_name

    return _endpoints.get(name)


def default():
    return get()


def get_all():
    return _endpoints.values()


def load_config_file(config_file):
    with open(os.path.join(base_directory, config_file)) as f:
        config = yaml.load(f)

    # Replace constants
    recursive_replace(config, 'API_EXPLORER_CLIENT_ID', endpoints.API_EXPLORER_CLIENT_ID)
    recursive_replace(config, 'USERINFO', 'https://www.googleapis.com/auth/userinfo.email')

    auth_level = config.get('auth_level', 'optional')
    config['auth_level'] = {
        'required': endpoints.AUTH_LEVEL.REQUIRED,
        'optional': endpoints.AUTH_LEVEL.OPTIONAL,
        'optional_continue': endpoints.AUTH_LEVEL.OPTIONAL_CONTINUE,
        'none': endpoints.AUTH_LEVEL.NONE
    }.get(auth_level)

    return config


def recursive_replace(container, old, new):
    if isinstance(container, dict):
        for key, value in container.iteritems():
            if value == old:
                container[key] = new
            if isinstance(value, (dict, list)):
                recursive_replace(value, old, new)
    else:
        for ix, value in enumerate(container):
            if value == old:
                container[ix] = new


def underscore(string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def auto_class(cls=None, endpoint=None, **kwargs):
    def auto_class_decr(cls):
        if 'resource_name' not in kwargs:
            name = underscore(cls.__name__).replace('_api', '').replace('_service', '')
            kwargs['resource_name'] = name

        if 'path' not in kwargs:
            kwargs['path'] = kwargs['resource_name']

        ep_api = get(endpoint)
        return ep_api.api_class(**kwargs)(cls)

    if cls:
        return auto_class_decr(cls)
    return auto_class_decr


def auto_method(func=None, returns=message_types.VoidMessage, name=None, http_method='GET'):
    def auto_api_decr(func):
        func_name = func.__name__ if not name else name
        func = annotated(returns=returns)(func)
        f_annotations = func.__annotations__
        f_args, f_varargs, f_kwargs, f_defaults = inspect.getargspec(func)

        if f_defaults:
            f_args_to_defaults = {f_args[len(f_args) - len(f_defaults) + n]: x for n, x in enumerate(f_defaults)}
        else:
            f_args_to_defaults = {}

        RequestMessage = f_annotations.pop('request', message_types.VoidMessage)
        ResponseMessage = f_annotations.pop('return', message_types.VoidMessage)

        RequestMessageOrContainer, request_args = annotations_to_resource_container(f_annotations, f_args_to_defaults, RequestMessage)

        ep_dec = endpoints.method(
            RequestMessageOrContainer,
            ResponseMessage,
            http_method=http_method,
            name=func_name,
            path=func_name  #TODO: include required params
        )

        def inner(self, request):
            kwargs = {}
            for arg_name in request_args:
                if hasattr(request, arg_name):
                    kwargs[arg_name] = getattr(request, arg_name)
                if arg_name in f_args_to_defaults and kwargs.get(arg_name) is None:
                    kwargs[arg_name] = f_args_to_defaults[arg_name]

            return_val = func(self, request, **kwargs)

            # return voidmessage if the return val is none
            if ResponseMessage == message_types.VoidMessage and return_val is None:
                return message_types.VoidMessage()

            return return_val

        return ep_dec(inner)

    if func:
        return auto_api_decr(func)

    return auto_api_decr


def annotations_to_resource_container(annotations, defaults, RequestMessage):
    args = {}

    if annotations:
        for n, (name, type) in enumerate(annotations.iteritems(), 1):
            required = True if name not in defaults else False

            if type == str:
                args[name] = messages.StringField(n, required=required)
            if type == int:
                args[name] = messages.IntegerField(n, required=required)
            #TODO: more types

    if args:
        return endpoints.ResourceContainer(RequestMessage, **args), args.keys()

    return RequestMessage, args.keys()
