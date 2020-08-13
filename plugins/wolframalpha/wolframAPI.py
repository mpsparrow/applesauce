import requests
import defusedxml.cElementTree as cET
from urllib.parse import quote_plus
from utils.config import readINI
from utils.logger import log

URL_TEMPLATE=f'http://api.wolframalpha.com/v2/query?appid={readINI("config.ini")["WolframAlpha"]["appID"]}&input='

class WolframResult:
    def __init__(self, query):
        self.query = query
        self.url = URL_TEMPLATE + quote_plus(self.query)
        self.root = None

        self.request()

        self.success = False
        self.error = "Failed to reach Wolfram|Alpha. Tell the bot provider to check their logs."
        self.didyoumean = None

        if self.root is None:
            return

        self.success = True if (self.root.get("success") == "true") else False

        if not self.success:
            dym = self.root.find("didyoumeans")
            if dym is None:
                self.error = "Your search returned nothing."
                return
            
            self.didyoumean = dym.find("didyoumean").text
            return

        self.numpods = self.root.attrib["numpods"]
        self.pods = []

    def request(self):
        r = requests.get(self.url)
        if r.status_code != 200:
            log.error(f"Failed to reach Wolfram|Alpha API: HTTP {r.status_code}")
            return

        self.root = cET.fromstring(r.text)
        