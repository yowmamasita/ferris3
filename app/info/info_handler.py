import webapp2
from ferris3 import template


class InfoHandler(webapp2.RequestHandler):

    def get(self):
        output = template.render("app/info/info.html")
        self.response.write(output)
        return self.response


webapp2_routes = [
    webapp2.Route('/', InfoHandler)
]
