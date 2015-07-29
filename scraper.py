# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
from lxml import etree
import datetime

# Read in a page
html = scraperwiki.scrape("http://house.ksou.cn/p.php?q=Caulfield+South%2C+VIC")

# Find something on the page using css selectors
root = etree.HTML(html)
extractedOn = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
for elem in root.xpath("//tr[td/span[@class='addr']]/../../../.."):
    blob = etree.tostring(elem, pretty_print=True)
    address = elem.xpath(".//span[@class='addr']/a/text()")[0]
    sold = elem.xpath(".//span[@class='addr']/../../..//table/tr[1]/td/b/text()")[0]
#    print sold.split()[1]
    scraperwiki.sqlite.save(unique_keys=['extracted_on','address'], data={
        "extracted_on": extractedOn,
        "address": address,
        "sold": sold.split()[1],
        "blob": blob
    })

# Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})

# An arbitrary query against the database
print scraperwiki.sql.select("* from data")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
