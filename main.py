import endpoints
from ferris3.discovery import discover_api_services, discover_webapp2_routes
from ferris3 import apis

# APIs

apis.add('default-api.yaml', default=True)

API_CLASSES = discover_api_services()
API_APPLICATION = endpoints.api_server(API_CLASSES)


# WSGI handlers
import webapp2

WSGI_ROUTES = discover_webapp2_routes()
WSGI_APPLICATION = webapp2.WSGIApplication(WSGI_ROUTES)
