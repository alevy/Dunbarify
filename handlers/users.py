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
import os
import base64
import hashlib

import base
from models.account import Account

class UsersHandler(base.BaseController):
  def new(self):
    if self.account:
      self.redirect('/u/' + self.account.nickname + '/')
    else:
      self.render("users/new.html")
  
  def edit(self, nickname):
    if self.account:
      if self.account.user == self.user:
        self.render("users/edit.html")
      else:
        self.error(500)
    else:
      self.error(404)
  
  def show(self, nickname):
    account = Account.get_by_key_name(nickname)
    if account.user != self.user:
      nonce = signature = None
      if "nonce" in self.params and "signature" in self.params:
        nonce = self.params["nonce"]
        signature = self.params["signature"]
      if not nonce or not signature:
        self.error(500)
        return
      if not account.verify(nonce, signature):
        self.error(500)
        return
    self.vars["account"] = account
    self.render("users/show.html")
  
  def update(self, nickname):
    if not self.account:
      self.error(404)
    elif self.account.user != self.user:
      self.error(500)
    else:
      self.account.email=self.params["account"]["email"]
      self.account.display_name=self.params["account"]["display_name"]
      self.account.about=self.params["account"]["about"]
      self.account.restricted = "restricted" in self.params["account"]
      self.account.put()
      self.redirect('/u/' + nickname)
  
  def create(self):
    if self.account:
      self.error(500)
    else:
      nickname = self.params["account"]["nickname"]
      email=self.params["account"]["email"]
      display_name=self.params["account"]["display_name"]
      secret_token = base64.urlsafe_b64encode(os.urandom(33))
      account = Account(key_name=nickname,
        user=self.user, nickname=nickname, email=email, display_name=display_name, secret_token=secret_token)
      account.put()
      self.response.out.write(account.to_xml())
