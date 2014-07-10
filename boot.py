#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
#import re
#import logging
#import pymongo
import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import options, parse_config_file, parse_command_line
#from tornado import template
from pyjade.ext.tornado import patch_tornado
patch_tornado()

#Static
from lib.static import StaticComboHandler

parse_config_file(os.path.join(os.path.dirname(__file__), "setting.py"))
parse_command_line()

URLS = [
  (r'/', 'handler.home.home')
]


class Application(tornado.web.Application):
  def __init__(self):
    _file = os.path.dirname(__file__)
    settings = {
      "template_path": os.path.join(_file, 'tpl'),
      "static_path": os.path.join(_file, 'static'),
      "static_handler_class": StaticComboHandler,
      # http://www.v2ex.com/t/12646
      #"cookie_secret": base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
      "cookie_secret": 'xxT0/WW+Tf6K+fzwo1CoH3Z/JcA+50EShx62Cot68io=',
      "xsrf_cookies": False,
      "gzip": True,
      #"autoescape": None,
      "debug": options.debug,
    }
    tornado.web.Application.__init__(self, URLS, **settings)

    if options.debug:
      from lib.reload import static_watcher, ReloadHandler
      def_router = [(r"/debug", ReloadHandler)]
      static_watcher('./')
      self.add_handlers(r'.*', def_router)


if __name__ == "__main__":
  http_server = tornado.httpserver.HTTPServer(Application())
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()
