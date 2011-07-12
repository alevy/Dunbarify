# Copyright (c) 2011 Amit Levy <amit@amitlevy.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import re

import utils

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class RestfulController(webapp.RequestHandler):
  def __init__(self):
    self.vars = {}
    self.params = {}
  def get(self, *args):
    self.parse_params()
    if (len(args) > 0 and args[0] != ''):
      self.show(*args)
    else:
      self.index()
  def post(self, *args):
    self.parse_params()
    if (len(args) > 0 and args[0] != ''):
      self.update(*args)
    else:
      self.create()
      
  def index(self):
    pass
  def show(self, *arg):
    pass
  def create(self):
    pass
  def update(self, *args):
    pass
  
  def parse_params(self):
    for key in self.request.arguments():
      ar_match = re.search("([^\[]+)\[([0-9]+)\]", key)
      ar_match_str = re.search("([^\[]+)\[([^\]]+)\]", key)
      if ar_match:
        self.params.setdefault(ar_match.group(1), {})[int(ar_match.group(2))] = self.request.get(key)
      elif ar_match_str:
        self.params.setdefault(ar_match_str.group(1), {})[ar_match_str.group(2)] = self.request.get(key)
      else:
        self.params[key] = self.request.get(key)
  
  def render(self, tmpl):
    self.write(template.render(utils.view_path(tmpl), self.vars))
  def write(self, output):
    self.response.out.write(output)
