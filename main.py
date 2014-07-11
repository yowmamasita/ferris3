import endpoints
from ferris3.discovery import discover_api_services
from ferris3 import apis

apis.add('default-api.yaml', default=True)
API_CLASSES = discover_api_services()
APPLICATION = endpoints.api_server(API_CLASSES)
