= GitHub Email Hooks

This is a simple [Google AppEngine](http://code.google.com/appengine) webapp written in [Python](http://www.python.org) that can be used as a post-receive web hook on GitHub.

The script simply emails the author(s) of a push who are not also the committer, informing them that the push has taken place.  This allows contributors to be automatically notified when their contributions have been accepted by an upstreamm project.

