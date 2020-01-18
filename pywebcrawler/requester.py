import requests, os, random
from requests.exceptions import TooManyRedirects, Timeout, ConnectionError
class Requester:
    """Will handle the HTTP Requests to be made"""

    def __init__(self, page_url, host, proxies=None, user_agents=None, headers=None, delay=0, timeout=10):
        if proxies is None:
            self.proxies = None
        else:
            self.proxies = proxies
        self.host = host
        self.page_url = page_url
        self.user_agents = user_agents or None
        self.user_agents = user_agents
        self.headers = headers
        self.timeout = timeout
        self.mime_types = None  # All other mimes excluding text/plain and text/html
        self.startup()

    def startup(self):
        # Get the user agents
        with open(os.path.join(os.path.dirname(__file__), "data", "useragents.txt"), "r") as file:
            if self.user_agents is None:
                self.user_agents = [user_agent.replace("\n", "") for user_agent in file]
        with open(os.path.join(os.path.dirname(__file__), "data", "mimetypes.txt"), "r") as file:
            self.mime_types = [mime_type.replace("\n", "") for mime_type in file]

    def request(self):
        headers = self.headers or {
            'Host': self.host,
            'User-Agent': str(random.choice(self.user_agents)),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        try:
            if self.proxies is not None:
                random_proxy = random.choice(self.proxies)
                response = requests.get(url=self.page_url,
                                        headers=headers,
                                        proxies={random_proxy[0]: random_proxy[1]},
                                        verify=False,
                                        timeout=self.timeout)
            else:
                response = requests.get(url=self.page_url,
                                        headers=headers,
                                        verify=False,
                                        timeout=self.timeout)
        except TooManyRedirects:
            return self.page_url, "TooManyRedirects"
        except Timeout:
            return self.page_url, "Timeout"
        except ConnectionError:
            return self.page_url, "ConnectionError"

        if "text/html" in response.headers['Content-Type'] or "text/plain" in response.headers['Content-Type']:
            if response.status_code == 200:
                response.close()
                return response.text
            else:
                response.close()
                return self.page_url, "UnknownError"
        elif response.headers['Content-Type'] in self.mime_types:
            # We got a file
            response.close()
            return self.page_url, "File"
