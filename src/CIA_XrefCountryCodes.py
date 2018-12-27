# copyright (c) 2018  Larz60+
import ScraperPaths
import GetPage
import CIA_ScanTools
from lxml import html
from lxml.cssselect import CSSSelector
from lxml.html.clean import clean_html
from lxml import etree
from lxml.etree import XPath
from bs4 import BeautifulSoup
import re
import os
import sys


class CIA_XrefCountryCodes:
    def __init__(self):
        self.spath = ScraperPaths.ScraperPaths()
        self.gp = GetPage.GetPage()
        self.getpage = self.gp.get_page
        self.get_filename = self.gp.get_filename
        self.cst = CIA_ScanTools.CIA_Scan_Tools()

        self.fact_links = self.cst.fact_links

        self.mainurl = 'https://www.cia.gov/library/publications/resources/the-world-factbook/appendix/appendix-d.html'

        self.filename = self.get_filename(self.mainurl)

        self.mainpage = self.getpage(self.mainurl, self.filename)

        self.scrape_page()
        self.cst.save_fact_links()

    def scrape_page(self):
        baseurl = 'https://www.cia.gov/library/publications/resources/the-world-factbook'
        tempout = self.spath.tmppath / 'output.txt'
        soup = BeautifulSoup(self.mainpage, 'lxml')
        pretty = self.spath.tmppath / 'Appendix-d_pretty.html'
        # with pretty.open('w') as pp:
        #     pp.write(soup.prettify())
        c1 = self.fact_links['Country Codes Xref'] = {}
        ttl = soup.find_all('title')[1]
        title = ttl.text.strip()
        c1['Title'] = title


        entry1 = soup.find('td', {'class': "category_data"})
        txts = entry1.text
        texts = txts.split('\n')
        ptext = []
        for item in texts:
            item = self.cst.fluffinutter(item)
            if len(item) < 2:
                continue
            ptext.append(item)

        c1['Publications'] = ptext
        count = 0        
        thediv = soup.find('div', {'id': 'demo'})
        head = thediv.find('tr', {'class': 'smalltext'})
        header = []
        tds = head.find_all('td')
        for td in tds:
            header.append(td.text.strip())
        mainul = thediv.find('ul')
        lis = mainul.find_all('li')

        for n, li in enumerate(lis):
            link = li.find('a')
            lurl = link.get('href')[2:]
            url = f'{baseurl}{lurl}'
            filename = self.get_filename(url)
            badfile = False
            if not filename.exists():
                parts = filename.parts
                if parts[-1] != '-.html':
                    print(f'trying to fetch {lurl}')
                    # self.getpage(url, filename)
                else:
                    badfile = True
            title = link.text.strip()
            c2 = c1[title] = {}
            if not badfile:
                c2['URL'] = url
                c2['Filename'] = os._fspath(filename)
            tds = li.find_all('td')
            entity = tds[0].text.strip()
            c3 = c2[entity] = {}

            skips = [0, 3, 5, 6, 9]
            gec = iso = stanag = internet = comment = None
            for n, td in enumerate(tds):
                if n in skips:
                    continue
                elif n == 1:
                    # gec
                    gec = td.text.strip()
                elif n == 2:
                    # iso 3166
                    iso = []
                    subtds = td.find_all('td')
                    for std in subtds:
                        iso.append(std.text.strip())
                elif n == 4:
                    # stanag
                    stanag = td.text.strip()
                elif n == 7:
                    # internet
                    internet = td.text.strip()
                elif n == 8:
                    # comment
                    comment = td.text.strip()
                else:
                    print(f'td {n} > 8 This should never happen')
            c3['GEC'] = gec
            c3 ['ISO 3166'] = iso
            c3 ['Stanag'] = stanag
            c3 ['Internet'] = internet
            c3 ['Comment'] = comment

if __name__ == '__main__':
    CIA_XrefCountryCodes()
