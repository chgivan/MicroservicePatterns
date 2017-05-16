from html.parser import HTMLParser
import urllib.request

class LinkHTMLParser(HTMLParser):
    def __init__(self, host):
        HTMLParser.__init__(self)
        self.links = []
        self.host = host
    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            for attr in attrs:
                if attr[0].lower() == "href":
                    link = attr[1]
                    if not link.startswith("https://") and not link.startswith("http://"):
                        link = self.host + link
                    self.links.append(link)

def getLinks(host):
    try:
        with urllib.request.urlopen(host) as response:
             parser = LinkHTMLParser(host)
             parser.feed(str(response.read()))
             parser.close()
             return parser.links
    except Exception as e:
        print (str(e))
        return None
