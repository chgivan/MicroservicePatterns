from html.parser import HTMLParser

class LinkHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            for attr in attrs:
                if attr[0].lower() == "href":
                    self.links.append(attr[1])
