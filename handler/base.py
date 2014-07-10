import os
import sys
import json
import datetime
import traceback
#from bson.objectid import ObjectId
#import random
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import tornado.web
import tornado.gen
from tornado.httpclient import AsyncHTTPClient
from tornado.options import options


class base(_base):
  def initialize(self, **kargs):
    #self._db = db
    super(base, self).initialize(**kargs)

class _base(tornado.web.RequestHandler):
  def initialize(self, **kwargs):
    if not hasattr(self, 'package'):
      self.package = self.__module__.split('.')[0]
    #self.db = self.application._db[self.package]

  def set_default_headers(self):
    if options.debug:
      self.set_header("Access-Control-Allow-Origin", "*")
      self.set_header('Access-Control-Allow-Methods', 'GET, PUT, OPTIONS')

  def get_error_html(self, status_code, **kwargs):
    kwargs['exc_info'] = sys.exc_info()
    error_code_orig = ''.join(traceback.format_exception(*kwargs["exc_info"]))
    formatter = HtmlFormatter(linenos=True, cssclass="codehilite")
    kwargs['error'] = highlight(error_code_orig, PythonLexer(), formatter)
    return self.render_string("error.html", **kwargs)

  def static_dev(self, path):
    domain = '127.0.0.1' if options.debug else '71.19.147.84'
    return '//%s:%d/static/%s' % (domain, options.port, path)

  def redirect_by_referer(self):
    redirect = self.request.headers.get('Referer', '/')
    self.redirect(redirect)

  def _json(self, data):
    def type_handler(obj):
      if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
        return obj.isoformat()
      #elif isinstance(obj, ObjectId):
        #return str(obj)
      else:
        return obj
    return json.dumps(data, default=type_handler)

  def jsondump(self, data):
    self.write(self._json(data))

  def set_global(self, obj={}):
    return obj

class proxy(_base):
  # allow javascript cross domain for dev
  def set_extra_headers(self, path):
    self.set_header('Access-Control-Allow-Origin', '*')

  @tornado.web.asynchronous
  @tornado.gen.coroutine
  def get(self, act=''):
    url = "http://reader.browser.miui.com" + self.request.uri
    async = AsyncHTTPClient()
    res = yield async.fetch(url)
    self.write(res.body)
    self.finish()
