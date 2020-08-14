import requests
import defusedxml.cElementTree as cET
from urllib.parse import quote_plus
from utils.config import readINI
from utils.logger import log

URL_TEMPLATE=f'http://api.wolframalpha.com/v2/query?appid={readINI("config.ini")["WolframAlpha"]["appID"]}&input='

class WolframSubPod:
    def __init__(self, xmlElement):
        self.img_src = xmlElement.find("img").get("src")
        pt = xmlElement.find("plaintext")
        if pt is None:
            self.plaintext = ""
        else:
            self.plaintext = xmlElement.find("plaintext").text

class WolframPod:
    def __init__(self, xmlElement):
        self.title = xmlElement.get("title")
        self.num_subpods = int(xmlElement.get("numsubpods"))

        self.subpods = []
        for subpod in xmlElement.findall("subpod"):
            self.subpods.append(WolframSubPod(subpod))

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

        self.num_pods = int(self.root.attrib["numpods"])
        self.pods = []

        self.get_pods()

    def request(self):
        r = requests.get(self.url)
        if r.status_code != 200:
            log.error(f"Failed to reach Wolfram|Alpha API: HTTP {r.status_code}")
            return

        self.root = cET.fromstring(r.text)

    def get_pods(self):
        for pod in self.root.findall("pod"):
            self.pods.append(WolframPod(pod))
        