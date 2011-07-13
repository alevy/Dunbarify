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
import hashlib
import hmac
from models.person import Person

from google.appengine.ext import db
from google.appengine.api import users

class Account(db.Model):
  user = db.UserProperty(required=True)
  nickname = db.StringProperty(required=True)
  display_name = db.StringProperty(required=True)
  secret_token = db.StringProperty(required=True)
  restricted = db.BooleanProperty(required=True, default=True)
  about = db.TextProperty()
  email = db.EmailProperty()
  people = db.ListProperty(db.Key)
  def verify(self, nonce, signature):
    return hmac.new(str(self.secret_token), str(nonce), hashlib.sha1).hexdigest() == signature
  def people_models(self):
    return Person.get(self.people)
  def circles(self):
    """docstring for circles"""
    cs = dict()
    peeps = Person.get(self.people)
    for person in peeps:
      for circle in person.circles:
        cs.setdefault(circle, []).append(person)
    return cs
  def people_in(self, circle):
    return self.circles()[circle]
  @classmethod
  def get_by_user(cls, user):
    return Account.all().filter("user =", user).get()