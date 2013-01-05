#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import db
try:import webapp2, time, os, template
except ImportError:from google.appengine.ext.webapp import template
class Command(db.Model):
  command = db.StringProperty(required=True)
class StylHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
            }
        path = os.path.join(os.path.dirname(__file__), 'controlstyle.css')
        self.response.out.write(template.render(path, template_values))

def deletecommand():
        for command in Command.all():
            command.delete()
    
class ControlsHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
                           "time":time.asctime(), "robocmd":self.request.get("command")
            }
        deletecommand()
        e = Command(command=self.request.get("command"))
        path = os.path.join(os.path.dirname(__file__), 'Commands.html')
        e.put()
        self.response.out.write(template.render(path, template_values))
class GetCommandHandler(webapp2.RequestHandler):
    def get(self):
        x=Command.all()
        y=""
        for cmd in x:
            y=cmd.command
        z="0 0 0"
        if y=="Backward":z="60 -50 -50"
        if y=="Forward":z="-60 50 50"
        if y=="<-":z="50 50 -60"
        if y=="->":z="50 -60 50"
        if y==" Stop ":z="0 0 0"
        if y=="/\\":
            z="70 -60 70"
            deletecommand()
        if y=="\\/":
            z="-70 60 -70"
            deletecommand()
        self.response.out.write(z)
class TitleHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
                           "time":time.asctime()
            }
        path = os.path.join(os.path.dirname(__file__), 'Welcome.html')
        self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication([('/', TitleHandler),  ('/title', TitleHandler), ('/gamestyle.css', StylHandler), ('/controls', ControlsHandler), ("/getcmd", GetCommandHandler)],
                              debug=True)
