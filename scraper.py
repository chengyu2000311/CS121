
import re, shelve, urllib
from urllib.parse import urlparse
from urllib.request import urlopen
from utils.response import Response
from bs4 import BeautifulSoup

# global variable for regular expression
allowed_url = ['.+\.cs.uci.edu/.*', '.+\.ics.uci.edu/.*', '.+\.informatics.uci.edu/.*', '.+\.stat.uci.edu/.*', 'today.uci.edu/department/information_computer_sciences/.*']
allowed_url = [re.compile(x) for x in allowed_url]

def scraper(url: str, resp: Response) -> list:
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    # get links from resp
    if resp.status != 200: return []
    else:
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
        # Store text and url to shelve
        try:
            s = shelve.open('urlText.db')
            if resp.raw_response.content != "":
                s[url] = soup.get_text()

            links = []
            for link in soup.findAll('a'):
                if link not in s:
                    links.append(link.get('href'))         
        finally:
            s.close()
        return links

def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        elif parsed.fragment != "": 
            return False
        elif len(parsed.path.split('/')) > 20:
            return False
        else:
            if not any([i.match(url) for i in allowed_url]):
                return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|ppsx)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
