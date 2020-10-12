import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm


class Crawler:
    def __init__(self, listings_to_fetch=50):
        print("Crawling Hemnet")
        self.links = []
        print("Fetching listings...[1/2]")
        self.fetch_links(min(50, listings_to_fetch))
        self.save_links()
        print("Collecting objects...[2/2]")
        self.fetch_objects_from_links()

    def fetch_links(self, n_calls=50):
        """
        Get links to Hemnet listings through recurrent GET
        Multiple calls are needed since only a limited number of objects are visible in every request
        """
        links = []
        for page_n in tqdm(range(n_calls)):
            http = requests.get("https://www.hemnet.se/salda/bostader?page={}".format(page_n))
            soup = BeautifulSoup(http.content, features="html.parser")
            for a in soup.find_all('a', href=True):
                res = a['href']
                if "https" in res and "salda" in res:
                    links.append(res)
        self.links = links

    def save_links(self, fname="resources/links.txt"):
        """
        Save the result to a text file
        """
        with open(fname, "w") as fn:
            for line in self.links:
                fn.write(line+"\n")

    def read_links(self, fname="resources/links.txt"):
        """
        Save the result to a text file
        """
        with open(fname, "r") as fn:
            self.links = fn.readlines()
        return self.links

    def fetch_objects_from_links(self):
        """
        Save the result to a text file
        """
        for link in tqdm(self.links):
            data = requests.get(link)
            soup = BeautifulSoup(data.text, features="html.parser")
            mydivs = soup.findAll("div", {"class": "sold-property__map js-listing-map-sold"})
            try:
                jdata = json.loads(mydivs[0]["data-initial-data"])
                with open("resources/objects/{}.html".format(jdata['listing']['id']), "w") as fn:
                    fn.writelines(data.text)
            except Exception as e:
                print(e)
