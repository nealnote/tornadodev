#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mimetypes
import tornado.web
from tornado.options import options


def is_combo(path):
  return True if (';' in path or ',' in path) else False

class StaticCrossDomain(tornado.web.StaticFileHandler):
  # allow javascript cross domain for dev
  def set_extra_headers(self, path):
    self.set_header('Access-Control-Allow-Origin', '*')

class StaticComboHandler(tornado.web.StaticFileHandler):
  # allow javascript cross domain for dev
  def set_extra_headers(self, path):
    if options.debug:
      self.set_header('Access-Control-Allow-Origin', '*')

  def get(self, path, include_host=True):
    '''TODO
      file.save(path) for prodction mode with static_url
    '''
    print path
    mime_type, encoding = mimetypes.guess_type(path)
    if is_combo(path) and mime_type in ['text/css', 'application/javascript', 'application/x-javascript']:
      tmp_list = []
      #print path
      for dir in path.split(';'):
        tmp = dir.split('/')
        for file in tmp[-1].split(','):
          abs_path = '/'.join([self.settings['static_path'], "/".join(tmp[:-1]), file])
          content = open(abs_path, 'r')
          tmp_list.append(content.read())
      if mime_type:
        self.set_header("Content-Type", mime_type)
      self.set_header("expires", "-1")
      return self.finish(''.join(tmp_list))

    tornado.web.StaticFileHandler.get(self, path, include_host)
