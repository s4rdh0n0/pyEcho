# Tornado Framework
import tornado.web

class NodeNotFoundController(tornado.web.RequestHandler):

    def get(self):
        self.render("page/error/400.html")
