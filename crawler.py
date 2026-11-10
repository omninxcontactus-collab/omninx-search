
from urllib.request import Request, urlopen
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser
from html.parser import HTMLParser
import json

USER_AGENT = "OMNINXBot/0.1"
SEED_URLS = ["https://www.python.org/"]

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title_parts = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "title":
            self.in_title = True

        if tag.lower() == "a":
            for key, value in attrs:
                if key.lower() == "href" and value:
                    self.links.append(value)

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data.strip())


def crawl(url):
    parsed = urlparse(url)

    if parsed.scheme != "https":
        print("HTTPS required. Skipping:", url)
        return

    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    robots = RobotFileParser()

    try:
        req = Request(robots_url, headers={"User-Agent": USER_AGENT})
        with urlopen(req, timeout=10) as response:
            robots.parse(
                response.read().decode("utf-8", "replace").splitlines()
            )
    except Exception:
        print("Cannot verify robots.txt. Skipping:", url)
        return

    if not robots.can_fetch(USER_AGENT, url):
        print("Access disallowed:", url)
        return

    try:
        req = Request(url, headers={"User-Agent": USER_AGENT})

        with urlopen(req, timeout=15) as response:
            if "text/html" not in response.headers.get("Content-Type", ""):
                print("Not HTML:", url)
                return

            html = response.read(1000000).decode("utf-8", "replace")

        parser = PageParser()
        parser.feed(html)

        result = {
            "url": url,
            "title": " ".join(parser.title_parts),
            "crawled_by": "OMNINX CRAWLER"
        }

        with open("index.jsonl", "a", encoding="utf-8") as file:
            file.write(json.dumps(result) + "\n")

        print("Indexed:", result["title"])

    except Exception as error:
        print("Error:", error)


if __name__ == "__main__":
    print("OMNINX SEARCH - CRAWLER STARTED")

    for url in SEED_URLS:
        crawl(url)

    print("CRAWLER FINISHED")

