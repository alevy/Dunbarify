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

import base
from models.person import Person
from google.appengine.ext.db import Key

class PeopleHandler(base.BaseController):
  def index(self):
    self.vars["people"] = Person.get(self.account.people)
    self.render('people/index.html')
  def new(self):
    self.render('people/new.html')
  def edit(self, key):
    self.vars["person"] = Person.get(key)
    self.render("people/edit.html")
  
  def show(self, key):
    pass
  
  def update(self, key):
    person = Person.get(key)
    person.name=self.params["name"]
    person.identifiers=map(unicode.lower, self.params["identifiers"])
    person.circles=map(unicode.lower, self.params["circles"])
    person.put()
    self.redirect("/p")
  
  def create(self):
    person = Person(parent=self.account,
                    name=self.params["name"],
                    identifiers=map(unicode.lower, self.params["identifiers"]),
                    circles=map(unicode.lower, self.params["circles"]))
    person.put()
    self.account.people.append(person.key())
    self.account.put()
    self.redirect("/p")
