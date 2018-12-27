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


class CIA_XrefGeographicNames:
    def __init__(self):
        self.spath = ScraperPaths.ScraperPaths()
        self.gp = GetPage.GetPage()
        self.getpage = self.gp.get_page
        self.get_filename = self.gp.get_filename
        self.cst = CIA_ScanTools.CIA_Scan_Tools()

        self.fact_links = self.cst.fact_links

        self.mainurl = 'https://www.cia.gov/library/publications/resources/the-world-factbook/appendix/appendix-f.html'

        self.filename = self.get_filename(self.mainurl)

        self.mainpage = self.getpage(self.mainurl, self.filename)

        self.scrape_page()
        self.cst.save_fact_links()

    def scrape_page(self):
        soup = BeautifulSoup(self.mainpage, 'lxml')
        c1 = self.fact_links['Geographic Names Xref'] = {}
        ttl = soup.find('td', {'style': 'background-image: url(../graphics/gold_gradiant.gif); '})
        title = ttl.text.strip()
        c1['Title'] = title
        entry1 = soup.find('div', {'class': "category_data"})
        c1['Description'] = entry1.text.strip()
        # print(c1['Description'])
        table = soup.find_all('table')
        # print(f'length table: {len(table)}')
        # for n, tbl in enumerate(table):
        #     print(f'\ntable_{n}: {tbl}')
        # detail header table_3
        # definitions table_4 through table_1479 (last one)
        header = []
        ths = table[3].find_all('th')
        for th in ths:
            header.append(th.text.strip())
        table_no = 4
        while True:
            try:
                tds = table[table_no].find_all('td')
                name = tds[0].text.strip()
                c2 = c1[name] = {}
                for n, td in enumerate(tds):
                    if n == 0:
                        continue
                    c2[header[n]] = td.text.strip()
                table_no += 1
            except IndexError:
                break

if __name__ == '__main__':
    CIA_XrefGeographicNames()
