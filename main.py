# Python Default
import os
import logging

import tornado
import tornado.gen
import tornado.ioloop
import tornado.locks
from tornado.options import define, options
from tornado.log import app_log, gen_log, access_log, LogFormatter

# Controller
from controller.auth import SignInController, SignOutController, NotFoundController
from controller.dashboard import DashboardController
from controller.administrator import DaftarPegawaiController


define("dir", default=os.path.dirname(__file__), help="root path")

class Application(tornado.web.Application):

   handlers = [(r"/logout", SignOutController),
               (r"/login", SignInController),
               (r"/", DashboardController),
               (r"/administrator/daftarpegawai", DaftarPegawaiController),
               (r"/administrator/daftarpegawai/userid=([A-Za-z0-9\-]+)", DaftarPegawaiController.PegawaiController),
               (r"/administrator/daftarpegawai/add", DaftarPegawaiController.PegawaiController),
               (r"/administrator/daftarpegawai/kkp/username=([A-Za-z0-9\-]+)", DaftarPegawaiController),
               (r"/.*", NotFoundController)]

   def __init__(self):

      settings = dict(
          title='pyEcho',
          version='1.0.0',
          template_path=os.path.join(options.dir, 'view'),
          static_path=os.path.join(options.dir, 'assets'),
          xsrf_cookies=True,
          cookie_secret='16b56537-b94e-49bc-9f98-9be58f0b2d28',
          login_url=r"/login",
          debug=True,
      )

      super(Application, self).__init__(self.handlers, **settings)


def logger():
    # define your new format, for instance :
    my_log_format = '%(color)s::%(levelname)s %(asctime)s::%(end_color)s - %(message)s'

    # create an instance of tornado formatter, just overriding the 'fmt' arg
    my_log_formatter = LogFormatter(fmt=my_log_format, color=True)

    # get the parent logger of all tornado loggers :
    root_logger = logging.getLogger()

    # set your format to root_logger
    root_streamhandler = root_logger.handlers[0]
    root_streamhandler.setFormatter(my_log_formatter)


@tornado.gen.coroutine
def main():
    # logger format
    logger()
    tornado.options.parse_command_line()

    server = Application()
    server.listen('4231')

    # In this demo the server will simply run until interrupted
    # with Ctrl-C, but if you want to shut down more gracefully,
    # call shutdown_event.set().
    shutdown_event = tornado.locks.Event()
    yield shutdown_event.wait()

if __name__ == "__main__":
    tornado.ioloop.IOLoop.current().run_sync(main)
