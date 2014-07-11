import endpoints
from ferris3.discovery import discover_api_services

APIS = discover_api_services()
APPLICATION = endpoints.api_server(APIS)
