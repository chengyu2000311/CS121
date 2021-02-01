
import re, shelve, urllib
from urllib.parse import urlparse
from urllib.request import urlopen
from utils.response import Response
from bs4 import BeautifulSoup
from collections import defaultdict

# global variable for regular expression
allowed_url = ['.+\.cs.uci.edu/.*', '.+\.ics.uci.edu/.*', '.+\.informatics.uci.edu/.*', '.+\.stat.uci.edu/.*', 'today.uci.edu/department/information_computer_sciences/.*']
allowed_url = [re.compile(x) for x in allowed_url]
#black_list the second is for wics calendar
black_list = ['https://evoke.ics.uci.edu/qs-personal-data-landscapes-poster/?replytocom=.*', 'www.stat.ics.uci.edu/wp-content/.*', '.*/[0-9]+-[0-9]+-[0-9]+$']
black_list = [re.compile(x) for x in black_list]

def scraper(url: str, resp: Response) -> list:
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    # get links from resp
    if 200 > resp.status or resp.status > 599 or resp.raw_response == None or resp.raw_response.content == "": return []
    else:
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
        # Store url and text to shelve
        try:
            url_parsed = urlparse(url)
            s = shelve.open('urlText.db')
            if url_parsed.fragment != '':
                url = url.split('#')[0]
            s[url] = soup.get_text() 

            links = []
            for link in soup.find_all('a'):
                link = link.get('href')
                if link != None and link not in s: # check if it is already crawled
                    for i in black_list:
                        if not (i.match(link)):
                            links.append(link) # check if last path is date in format 2000-02-01
        finally:
            s.close()
        return links

def is_valid(url):
    try:
        parsed = urlparse(url)
        The_path = parsed.path.split("/")
        pass_dict = defaultdict(int)
        s = shelve.open('urlText.db')
        if parsed.scheme not in set(["http", "https"]):
            return False
        elif len(parsed.path.split('/')) > 20:
            return False
        elif not any([i.match(url) for i in allowed_url]):
            return False
        elif 'action=download' in parsed.query:
            return False
        for i in The_path:
            if 'pdf' in i or 'img' in i:
                return False
            pass_dict[i] += 1
            
            if pass_dict[i] > 4:
                return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|ppsx|Z)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
    finally:
        s.close()


