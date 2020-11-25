import logging
import requests
import re
from bs4 import BeautifulSoup

logger = logging.getLogger(name="html_parser")
logging.basicConfig(level=logging.DEBUG)
SEARCH_QUERIES = [
    "vaccines side effects",
    "vaccines autism",
    "vaccines why are they bad",
    "is vaccination safe",
    "should I vaccine my child"]

CERTIFIED_DOMAINS = [
    "mayoClinic.com",   # Certificate validity: valid until Apr 2021
    "webmd.com",   # Certificate validity: valid until Aug 2021
    "caringforkids.cps.ca",    # Certificate validity: valid until Jul 2021
    "healthline.com",    # Certificate validity: valid until Jan 2021
    "cancer.net",    # Certificate validity: valid until Oct 2020
    "vaccinestoday.eu",    # Certificate validity: valid until May 2021
    "drugs.com",    # Certificate validity: valid until Feb 2021
    "everydayhealth.com"    # Certificate validity: valid until Jun 2021
]

params = {
    "lang": "en"
}


def get_articles_from_google_search(search_queries, certified=False):
    article_links = []
    for query in search_queries:
        urls = ""
        if certified:
            urls = ["https://www.google.com/search?q={} site:{}".format(query, page) for page in CERTIFIED_DOMAINS]
        else:
            urls = ["https://www.google.com/search?q={}".format(query)]
        for url in urls:
            response = requests.get(url=url, params=params)
            # for next pages: url="https://www.google.com/search?q={}&start=10" or 20, 30 ...
            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.find_all('a'):
                possible_article_link = link.get('href')
                if (possible_article_link.startswith("/url?q=")
                        and "google.com" not in possible_article_link
                        and "youtube.com" not in possible_article_link):
                            link = str(link.get('href').strip("/url?q=").split("&", 1)[0])
                            if not link.endswith(".pdf"):
                                article_links.append(link)
    return article_links

def get_articles_from_urls(article_links):
    for link in article_links:
        response = requests.get(url=link)
        soup = BeautifulSoup(response.text, "html.parser")
        #regex = re.compile(r'[A-Z][^.?!].+((?![.?!][’"]?\s["’]?[A-Z][^.?!]).)+[.?!]')
        #matched_sentences = regex.finditer(soup.get_text())
        matched_sentences = soup.find_all('p')

        print(link)
        for match in matched_sentences:
            print(match.get_text())
        #     print(match.group())
        #print(regex.match(" eqw e qw ewq we qw e  weqq ew \n Who should have the chickenpox vaccine? \n eqweqw eqweqw eqw e"))


if __name__ == "__main__":
    logger.info("HMTL parser started")
    article_links = get_articles_from_google_search(SEARCH_QUERIES, certified=False)
    logger.info(article_links)
    get_articles_from_urls(article_links)
