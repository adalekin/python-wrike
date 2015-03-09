python-wrike
======
A Python 2 client for the Wrike API

Installation
-----
pip install python-wrike

Requires
-----
  * requests
  * requests_oauth2
  * six


Wrike APIs
------------------------------
Wrike [developer site](https://developers.wrike.com/) documents all the Wrike API.


Authentication
-----

Wrike API uses the OAuth 2.0 protocol for authorization. Every API request must contain the Authorization header (preferred option) or the access_token parameter with the OAuth 2.0 access token. See the OAuth 2.0 authorization description for details.
See the docs for more information: https://developers.wrike.com/documentation/oauth2

### Obtaining an access token

If you're using a method that requires authentication and need an access token, you can use the provided bin/wrike-config.py script to obtain an access token for yourself.
You should provide your app's Client ID, Client Secret, and Redirect URI, and walk you through instructions for getting your own access token for your app.

```
python bin/wrike-config.py --client-id="YOUR_CLIENT_ID" --client-secret="YOUR_CLIENT_SECRET"
```

Open the link, provide permissions for you app and copy a code from the browser address bar.

```
python bin/wrike-config.py --client-id="YOUR_CLIENT_ID" --client-secret="YOUR_CLIENT_SECRET" --code="YOUR_CODE" --output=default.conf
```

Then your access token and other authentication infromation will be saved into the output file.

### Using an access token

Once you have an access token (whether via the script or from the user flow), you can pass that token into the WrikeAPI constructor:

``` python
from wrike.client import WrikeAPI

access_token = "YOUR_ACCESS_TOKEN"
api = WrikeAPI(access_token=access_token)
api.accounts(fields=["subscription", "customFields", "metadata"])
```
       
Data Retrieval:
-----

See the endpoints docs for more on these methods: https://developers.wrike.com/documentation/api/methods/query-users-and-groups

Here's an example of retrieving accounts:

``` python
accounts = api.accounts(fields=["subscription", "customFields", "metadata"])
for account in accounts["data"]:
    print account.name
```

Error handling
------
Importing the bind module allows handling of specific error status codes. An example is provided below:
``` python
from wrike.exceptions import WrikeAPIError

try:
   # your code goes here
except WrikeAPIError as e:
   if (e.status_code == 400):
      print "\nYou have to provide a title for a new folder."
```

Contributing
------------
In the spirit of [free software](http://www.fsf.org/licensing/essays/free-sw.html), **everyone** is encouraged to help improve this project.

Here are some ways *you* can contribute:

* by using alpha, beta, and prerelease versions
* by reporting bugs
* by suggesting new features
* by writing or editing documentation
* by writing specifications
* by writing code (**no patch is too small**: fix typos, add comments, clean up inconsistent whitespace)
* by refactoring code
* by closing [issues](https://github.com/adalekin/python-wrike/issues)
* by reviewing patches


Submitting an Issue
-------------------
I prefer to use the [GitHub issue tracker](https://github.com/adalekin/python-wrike/issues) to track bugs and
features. Before submitting a bug report or feature request, check to make sure it hasn't already
been submitted. You can indicate support for an existing issue by voting it up. When submitting a
bug report, please include a [Gist](http://gist.github.com/) that includes a stack trace and any
details that may be necessary to reproduce the bug, including your version number, and
operating system. Ideally, a bug report should include a pull request with failing specs.
