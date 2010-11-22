#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import logging
from django.utils import simplejson as json
from google.appengine.api import mail
from config import *

class Committer(object):
  def __init__(self, name, email, commit, msg, url):
    self.email = email
    self.name = name
    self.commits = [(commit, msg, url)]
  
  def add_commit(self, commit, msg, url):
    self.commits.append((commit, msg, url))
  
  def send_email(self, payload):
    if len(self.commits) == 1:
      subj = "1 of your commits was merged into %s!" % payload['repository']['name']
    else:
      subj = "%s of your commits were merged into %s!" % (len(self.commits), payload['repository']['name'])
    logging.debug("Generated email subject [%s]" % subj)  
    body = '''
    Greetings, %s!

    The following commits of yours have been pulled into %s by %s.

    Commits
    -------
    %s

    -- The GitHub EmailHook
   	    ''' % (self.name, payload['repository']['name'], payload['pusher']['name'], self.list_commits())
   	    
    logging.debug("About to email %s <%s> with info on %s commits (%s)" % (self.name, self.email, len(self.commits), self.list_commits()))
    mail.send_mail(EMAIL_FROM, "%s <%s>" % (self.name, self.email), subj, body)
  
  def list_commits(self):
    s = ""
    for c in self.commits:
      s += "%s : %s : %s\n" % (c[0][:7], c[2], c[1])    
    return s

def notify_committers(payload):
  # First check if this is in the list of watched repositories!
  if payload['repository']['url'] in ALLOWED_REPOS or payload['repository']['organization'] in ALLOWED_ORGS:
    committers_to_notify = {}
    for c in payload['commits']:
      committer_email = c['author']['email']
      if committer_email != payload['pusher']['email']:
        if committer_email in committers_to_notify:
          committers_to_notify[committer_email].add_commit(c["id"], c["message"], c["url"])
        else:
          committers_to_notify[committer_email] = Committer(c['author']['name'], committer_email, c["id"], c["message"], c["url"])
    logging.info("Found %s committers to notify" % len(committers_to_notify))
    for committer in committers_to_notify.values():
      committer.send_email(payload)
  else:
    logging.warn("Received a request for repository %s which is not on the whitelist" % payload['repository']['url'])
    mail.send_mail_to_admins(EMAIL_FROM, "Unrecognized repository %s" % payload['repository']['url'], "Unrecognized repository %s.  JSON payload submitted: %s" % (payload['repository']['url'], payload))

class MainHandler(webapp.RequestHandler):    
  def post(self):
    payload_json = self.request.POST['payload']
    payload = json.loads(payload_json)
    notify_committers(payload)

def main():
  application = webapp.WSGIApplication([('/', MainHandler)], debug=False)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()
