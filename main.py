# Python Default
import os

import app

import tornado
from tornado.options import define, options


define("api", default="http://localhost:8000", help="web service")
define("dir", default=os.path.dirname(__file__), help="root path")
define("cookies", default="echo_web", help="web")

@tornado.gen.coroutine
def main():
    tornado.options.parse_command_line()

    server = app.Application()
    server.listen('4231')

    # In this demo the server will simply run until interrupted
    # with Ctrl-C, but if you want to shut down more gracefully,
    # call shutdown_event.set().
    shutdown_event = tornado.locks.Event()
    yield shutdown_event.wait()

if __name__ == "__main__":
    tornado.ioloop.IOLoop.current().run_sync(main)
