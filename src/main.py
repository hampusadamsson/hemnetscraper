import sys
sys.path.append('src')
from Crawler import Crawler
from Parser import Parser
import os
import argparse

try:
    os.mkdir("resources")
    os.mkdir("resources/objects")
except:
    pass

parser = argparse.ArgumentParser(description='A Python based Hemnet parser. Fetch N number of Hemnet listings (n = 1 '
                                             'to 1000)')
parser.add_argument("-n", type=int, default=50)
args = parser.parse_args()

n = args.n

if __name__ == '__main__':
    c = Crawler(int(n/50))
    p = Parser()
