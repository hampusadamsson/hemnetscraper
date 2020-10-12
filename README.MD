# Hemnetscraper
This is a webscraper that crawls Hemnet - https://www.hemnet.se/. 
Use the output from the script **result.csv** to perform your analysis or data driven development. There is an example notbook and example data in the analysis directory.

Happy hacking!

# Instructions
```python
$ git clone https://github.com/hampusadamsson/hemnetscraper.git
$ cd hemnetscraper
$ pip3 install -r requirement.txt
$ python3 src/main.py -n 50 
```

## Expected output
```
Crawling Hemnet
Fetching listings...[1/2]
100%|███████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  1.66it/s]
Collecting objects...[2/2]
100%|█████████████████████████████████████████████████████████| 50/50 [00:29<00:00,  1.72it/s]
Parsing HTML...
100%|███████████████████████████████████████████████████████| 119/119 [00:02<00:00, 41.67it/s]
Saved result to: resources/result.csv
```

Use this tool at your own risk. I take no responsibility.