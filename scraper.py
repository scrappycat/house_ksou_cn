# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
from lxml import etree
from datetime import datetime
import csv
import urllib

def parsePage(suburb ,state, page):
    html = scraperwiki.scrape("http://house.ksou.cn/p.php?" +
                              urllib.urlencode({
                                  'q': suburb,
                                  'sta': state.lower(),
                                  'region': suburb,
                                  'p': page,
                                  's': page-1
                              }))

    # Find something on the page using css selectors
    root = etree.HTML(html)
    extractedOn = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

    # translates row identifier and returns a dictionary with coolection of parsed parameters
    # to be merged with the original information dictionary
    def translate(value):
        if len(value) == 0:
            return {}

        key = "".join(value[0].xpath("./b/text()")).split(":")[0].lower()
        val = "".join(value[0].xpath("./text()"))
        if key == "house" or \
                        key == "unit" or \
                        key == "townhouse" or \
                        key == "apartment" or
                        key == "commercial property":
            (bedrooms, bathrooms) = val.strip().partition(" ")[::2]
            return {
                "type": key,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms
            }

        if key[0:4] == "sold":
            return {
                "sold": key.split()[1],
                "sold on": val.strip()
            }

        return { key: val.strip() }

    # The scraper part where things break
    for elem in root.xpath("//tr[td/span[@class='addr']]/../../../.."):
        blob = etree.tostring(elem, pretty_print=True)
        streetAddress = elem.xpath(".//span[@class='addr']/a/text()")[0]

        info = {
            "type": "",
            "land size": "",
            "last sold": "",
            "list": "",
            "rent": "",
            "bedrooms": "",
            "bathrooms": "",
            "sold": "",
            "sold on": "",
            "agent": ""
        }

        for line in range(1,5):
            lineSelector = elem.\
                xpath(".//span[@class='addr']/../../..//table/tr[" + str(line) + "]/td")
            info.update(translate(lineSelector))

#        print info

        # Save found data
        scraperwiki.sqlite.save(unique_keys=['extracted_on','address'], data={
            "extracted_on": extractedOn,
            "address": streetAddress,
            "sold": info["sold"],
            "bathrooms": info["bathrooms"],
            "land_size": info["land size"],
            "type": info["type"],
            "bedrooms": info["bedrooms"],
            "list": info["list"],
            "rent": info["rent"],
            "land_size": info["land size"],
            "suburb": suburb,
            "sold_on": info["sold on"],
            "agent": info["agent"],
            "blob": blob
        })



# Drop previous data table
try:
    scraperwiki.sql.execute("DROP TABLE data")
except:
    print "table data not found"

dictReader = csv.DictReader(open('suburbs.csv', 'rb'))

for line in dictReader:
    for page in range(1, int(line['pages'])):
        # Read in a page
        parsePage(line['suburb'], line['state'], page)

# An arbitrary query against the database
#print scraperwiki.sql.select("* from data")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
