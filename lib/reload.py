import os
import logging
import subprocess
import tornado.escape
import tornado.websocket
from tornado import autoreload
from tornado.options import options

_base_path = ''


def _check_file(modify_times, path):
  try:
    modified = os.stat(path).st_mtime
  except Exception:
    return
  if path not in modify_times:
    modify_times[path] = modified
    return
  if modify_times[path] != modified:
    logging.info("%s modified; restarting server", path)
    reload(path, modify_times, modified)
    type = path.split('.')[-1]
    if type in ['py', 'html', 'md', 'js']:  # restart with python,templete,javascript change only
      #autoreload._reload()
      ReloadHandler.emit({'reload': path})
    elif type == 'less':
      css_path = path.replace('.less', '.css')
      subprocess.call(['lessc', '-x', path, css_path], shell=False)


def reload(path, modify_times, modified):
  global _base_path
  print path
  res = path.split(_base_path)[1]
  ReloadHandler.emit({'reload': res})
  modify_times[path] = modified


def static_watcher(path):
  global _base_path
  _base_path = os.path.abspath(path)
  for dir, sub, files in os.walk(path):
    if dir[0:3] != './.':  # ignore dirname == '.\w'
      for f in files:
        if f[0] != '.':  # ignore filename == '.\w'
          autoreload.watch(os.path.abspath(os.path.join(dir, f)))

autoreload._check_file = _check_file


class ReloadHandler(tornado.websocket.WebSocketHandler):
  waiters = set()

  def allow_draft76(self):
    # for iOS 5.0 Safari
    return True

  def open(self):
    ReloadHandler.waiters.add(self)

  def on_close(self):
    ReloadHandler.waiters.remove(self)

  @classmethod
  def emit(cls, chat):
    logging.info("sending message to %d waiters", len(cls.waiters))
    for waiter in cls.waiters:
      try:
        waiter.write_message(chat)
      except:
        logging.error("Error sending message", exc_info=True)

  def on_message(self, message):
    ReloadHandler.emit(message)

if options.debug:
  handlers = [
    ("/debug", ReloadHandler),
  ]
