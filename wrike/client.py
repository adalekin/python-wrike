from wrike.exceptions import WrikeAPIError

__author__ = 'adalekin'

import datetime
import requests

from wrike.bind import bind_method
from wrike.storage import MemoryStorage

from requests_oauth2 import OAuth2


class WrikeAPI(object):
    host = "www.wrike.com"
    base_path = "/api/v3"
    protocol = "https"
    user_agent = "python-wrike 0.0.0"

    def __init__(self, client_id, client_secret, code=None, storage=MemoryStorage()):
        self.oauth2 = OAuth2(
                client_id=client_id,
                client_secret=client_secret,
                site="{0}://{1}/".format(self.protocol, self.host),
                redirect_uri="http://localhost",
                authorization_url="oauth2/authorize",
                token_url="oauth2/token")
        self.storage = storage

        if code:
            self._get_token(code=code)

    def _get_token(self, code):
        response = self.oauth2.get_token(code, grant_type="authorization_code")

        if "error" in response:
            raise WrikeAPIError(400,
                                response["error"],
                                response["error_description"])


        if "expire" in response:
            response["expire_at"] = datetime.datetime.utcnow() + datetime.timedelta(seconds=response["expire"])

        self.storage.set(**response)
        return response

    def _refresh_token(self):
        refresh_token = self.storage.get("refresh_token")
        response = self.oauth2.get_token('', grant_type="refresh_token", refresh_token=refresh_token)
        self.storage.set(**response)
        return response

    @property
    def authorize_url(self):
        return self.oauth2.authorize_url(response_type='code')

    @property
    def session(self):
        expire_at = self.storage.get("expire_at")
        if datetime.datetime.utcnow() > expire_at:
            self._refresh_token()

        return requests.Session()

    accounts = bind_method(
        path="accounts",
        method="GET",
        accepts_parameters=["metadata", "fields"])

    account_tasks = bind_method(
        path="accounts/{account_id}/tasks",
        method="GET",
        accepts_parameters=["account_id", "metadata", "fields"])
