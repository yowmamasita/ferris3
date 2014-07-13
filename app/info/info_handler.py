import webapp2


class InfoHandler(webapp2.RequestHandler):

    def get(self):
        self.response.write("Hi")
        return self.response


webapp2_routes = [
    webapp2.Route('/', InfoHandler)
]
