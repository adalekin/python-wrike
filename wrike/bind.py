__author__ = 'adalekin'

import re
import requests

from six.moves.urllib.parse import quote

from wrike.exceptions import WrikeClientError, WrikeAPIError
from wrike.utils import encode_string

RE_PATH_TEMPLATE = re.compile('{\w+}')


def bind_method(**config):

    class WrikeAPIMethod(object):
        path = config['path']
        method = config.get('method', 'GET')
        accepts_parameters = config.get("accepts_parameters", [])
        parameters = {}

        def __init__(self, api, *args, **kwargs):
            self.api = api
            self._build_parameters(*args, **kwargs)
            self._build_path()

        def _build_parameters(self, *args, **kwargs):
            self.parameters = {
                "data": {},
                "headers": dict(
                    {
                        "User-Agent": self.api.user_agent,
                        "Accept": "*/*",
                        "Accept-Language": "en",
                        "Connection": "keep-alive"
                    }, **kwargs.get('headers', {}))
            }

            # via tweepy https://github.com/joshthecoder/tweepy/
            for index, value in enumerate(args):
                if value is None:
                    continue

                try:
                    self.parameters["data"][self.accepts_parameters[index]] = encode_string(value)
                except IndexError:
                    raise WrikeClientError("Too many arguments supplied")

            for key, value in kwargs.iteritems():
                if value is None:
                    continue
                if key in self.parameters:
                    raise WrikeClientError("Parameter %s already supplied" % key)
                self.parameters["data"][key] = encode_string(value)

        def _build_path(self):
            for variable in RE_PATH_TEMPLATE.findall(self.path):
                name = variable.strip('{}')

                try:
                    value = quote(self.parameters['data'][name])
                except KeyError:
                    raise Exception('No parameter value found for path variable: %s' % name)
                del self.parameters['data'][name]

                self.path = self.path.replace(variable, value)
            self.path = "{0}://{1}{2}{3}".format(self.api.protocol, self.api.host, self.api.base_path, self.path)

        def execute(self):
            session = self.api.session
            # Use an authorization header after the request object being created
            if "headers" in self.parameters:
                self.parameters["headers"]["Authorization"] = "{0} {1}".format(
                    self.api.storage.get("token_type"),
                    self.api.storage.get("access_token"))

            response = session.request(
                method=self.method,
                url=self.path,
                **self.parameters)

            try:
                result = response.json()
            except ValueError:
                raise WrikeClientError('Unable to parse response, not valid JSON.',
                                       status_code=response.status_code)

            if response.status_code != requests.codes.ok:
                raise WrikeAPIError(response.status_code,
                                    result["error"],
                                    result["errorDescription"])
            return result

    def _call(api, *args, **kwargs):
        method = WrikeAPIMethod(api, *args, **kwargs)
        return method.execute()

    return _call
