#!/usr/bin/python
# -*- coding: utf8 -*-
from .base import base

class home(base):
  def get(self):
    self.render('home.jade')

