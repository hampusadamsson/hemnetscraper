from bs4 import BeautifulSoup
import json
from tqdm import tqdm
from os import listdir
import pandas as pd


class Parser:
    def __init__(self, to_csv="resources/result.csv"):
        print("Parsing HTML...")
        self.df = None
        self.parse_html()
        clean = self.clean_data()
        clean.to_csv(to_csv, index=False)
        print("Saved result to: " + to_csv)

    def parse_html(self):
        """
        Parse files into Json
        """
        objects = []
        for f in tqdm(listdir("resources/objects")):
            if ".html" in f:
                with open("resources/objects/{}".format(f), "r") as f:
                    data = f.read()
                soup = BeautifulSoup(data, features="html.parser")
                mydivs = soup.findAll("div", {"class": "sold-property__map js-listing-map-sold"})
                jdata = json.loads(mydivs[0]["data-initial-data"])
                objects.append(jdata)
        self.df = pd.DataFrame.from_dict([t['listing'] for t in objects])

    @staticmethod
    def parse_num(x, n_remove_suff=0):
        if x == None:
            return None
        t = "".join([v for v in x if v.isnumeric() or v == ","])
        t = t.replace(",", ".")
        if n_remove_suff:
            t = t[:-n_remove_suff]
        return float(t)

    @staticmethod
    def contains_num(s):
        return any(filter(lambda x: x.isnumeric(), s))

    @staticmethod
    def floor(x):
        try:
            x = x.lower()
            if "vån " in x:
                last = x.split("vån")[-1]
                return Parser.parse_num(last)
            if x[-2:] == "tr":
                return Parser.parse_num(x[-4:-2])
        except:
            return 0
        return 0

    def clean_data(self):
        df = self.df
        df_parsed = pd.DataFrame()
        df_parsed["price_per_area"] = df.price_per_area.apply(lambda x: Parser.parse_num(x, 1))
        df_parsed["rooms"] = df.rooms.apply(Parser.parse_num)
        df_parsed["fee"] = df.fee.apply(Parser.parse_num)
        df_parsed["living_space"] = df.living_space.apply(lambda x: Parser.parse_num(x, 1))
        df_parsed["supplemental_area"] = df.supplemental_area.apply(lambda x: Parser.parse_num(x, 1))
        df_parsed["price"] = df.price.apply(Parser.parse_num)
        df_parsed["asked_price"] = df.asked_price.apply(Parser.parse_num)
        df_parsed["land_area"] = df.land_area.apply(lambda x: Parser.parse_num(x, 1))
        df_parsed["longitude"] = df.coordinate.apply(lambda x: x[0])
        df_parsed["latitude"] = df.coordinate.apply(lambda x: x[1])
        df_parsed["typeSummary"] = df.typeSummary
        df_parsed["year"] = df.sale_date.apply(lambda x: x[5:].split("-")[0])
        df_parsed["month"] = df.sale_date.apply(lambda x: x[5:].split("-")[1])
        df_parsed["day"] = df.sale_date.apply(lambda x: x[5:].split("-")[2])
        df_parsed["floor"] = df.address.apply(Parser.floor)
        return df_parsed