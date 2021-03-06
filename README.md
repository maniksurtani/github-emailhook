# GitHub Email Hooks

This is a simple [Google AppEngine](http://code.google.com/appengine) webapp written in [Python](http://www.python.org) that can be used as a post-receive web hook on GitHub.

The script simply emails the author(s) of a push who are not also the pusher, informing them that the push has taken place.  This allows contributors to be automatically notified when their contributions have been accepted by an upstream project.

## Usage

1. Clone this project.
2. Edit ``config.py`` and edit the values of ``ALLOWED_REPOS`` and ``EMAIL_FROM``.
3. Edit ``app.yaml`` and edit the value of application.
4. Deploy to Google AppEngine for Python
5. Configure your GitHub repository to call your AppEngine app (Browse to your repo and select Admin -> Service Hooks -> Post-Receive URLs)
 
That's it!

# TODO

 * Create a formal set of TODOs!
 * Extract email contents into customisable templates
 * HTML + plaintext emails
 * Extract email subject to config file
 * Queue emails in a task queue and batch-deliver to ensure http request doesn't time out 

# License

These scripts are open source and released under the BSD License.  See the accompanying LICENSE.txt file for details.
