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
import webapp2

#config = ('default-group':'base-data')

app = webapp2.WSGIApplication([
	('/ballot', 'ballot.Ballot'),
    ('/', 'base_page.BaseHandler'),
    ('/votes', 'votes.Votes'),
    ('/states', 'states.States'),
    ('/districts', 'districts.Districts'),
    ('/admin', 'admin.Admin')
], debug=True)

app.router.add(webapp2.Route(r'/states/<state:([0-9]+|[A-Z][A-Z]|all)><:/?>', 'states.States'))
app.router.add(webapp2.Route(r'/districts/<district:([0-9]+|[A-Z][A-Z]|all)><:/?>', 'districts.Districts'))
app.router.add(webapp2.Route(r'/districts/<district:([0-9]+|[A-Z][A-Z]|all)>/states/<state:([0-9]+|[A-Z][A-Z]|all)><:/?>', 'districts.Districts_by_State'))
app.router.add(webapp2.Route(r'/districts/states/<state:([0-9]+|[A-Z][A-Z])><:/?>', 'districts.Districts_by_State'))
app.router.add(webapp2.Route(r'/votes/<vote:([0-9]+|all)><:/?>', 'votes.Votes'))
app.router.add(webapp2.Route(r'/voters/<voter:([0-9]+|all)><:/?>', 'voters.Voters'))