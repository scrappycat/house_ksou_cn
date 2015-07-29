# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
from lxml import etree
from datetime import datetime

# Read in a page
suburb = "Caulfield+South"
html = scraperwiki.scrape("http://house.ksou.cn/p.php?q=" + suburb +"%2C+VIC")

# Drop previous data table
try:
    scraperwiki.sql.execute("DROP TABLE data")
except:
    print "table data not found"

# Find something on the page using css selectors
root = etree.HTML(html)
extractedOn = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

# The scraper part where things break
for elem in root.xpath("//tr[td/span[@class='addr']]/../../../.."):
    blob = etree.tostring(elem, pretty_print=True)
    address = elem.xpath(".//span[@class='addr']/a/text()")[0]
    sold = elem.xpath(".//span[@class='addr']/../../..//table/tr[1]/td/b/text()")[0]
    sold_on = elem.xpath(".//span[@class='addr']/../../..//table/tr[1]/td/text()")[0]
    print sold_on
    # Save found data
    scraperwiki.sqlite.save(unique_keys=['extracted_on','address'], data={
        "extracted_on": extractedOn,
        "address": address,
        "sold": sold.split()[1],
        "sold_on": sold_on,
        "blob": blob
    })

# Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})

# An arbitrary query against the database
#print scraperwiki.sql.select("* from data")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
