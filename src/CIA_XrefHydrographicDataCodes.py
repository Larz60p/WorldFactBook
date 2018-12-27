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


class CIA_XrefHydrographicDataCodes:
    def __init__(self):
        self.spath = ScraperPaths.ScraperPaths()
        self.gp = GetPage.GetPage()
        self.getpage = self.gp.get_page
        self.get_filename = self.gp.get_filename
        self.cst = CIA_ScanTools.CIA_Scan_Tools()

        self.fact_links = self.cst.fact_links

        self.mainurl = 'https://www.cia.gov/library/publications/resources/the-world-factbook/appendix/appendix-e.html'

        self.filename = self.get_filename(self.mainurl)

        self.mainpage = self.getpage(self.mainurl, self.filename)

        self.scrape_page()
        self.cst.save_fact_links()

    def remove_tags(self, item):
        intag = False
        oitem = ''
        for c in item:
            if c == '>':
                intag = False
                continue
            if c == '<':
                intag = True
            if intag:
                continue
            oitem += c
        return oitem

    def fluffinutter(self, text):
        newtext = ''
        intrum = text.split('\n')
        for item in intrum:
            item = item.replace('&#160;', '')
            if '<' in item:
                item = self.remove_tags(item)
            newtext = f'{newtext} {item.strip()}'
        return newtext

    def scrape_page(self):
        soup = BeautifulSoup(self.mainpage, 'lxml')
        c1 = self.fact_links['Hydrographic Data Codes Xref'] = {}
        ttl = soup.find('td', {'style': 'background-image: url(../graphics/gold_gradiant.gif); '})
        title = ttl.text.strip()
        c1['Title'] = title
        entry1 = soup.find('div', {'class': "category_data"})
        txts = entry1.text
        texts = txts.split('\n')
        texts[:] = [item.replace('\u00a0', '') for item in texts if not item == '\xa0']
        # htext = htext.replace('\u00a0', '')
        c1['Publications'] = texts

        # Get ocean info
        c2 = c1['Oceans'] = {}

        # Get table of interest and it's tr's
        tables = soup.find_all('table')
        table = tables[4]
        trs = table.find_all('tr')

        # get header
        head_title = self.fluffinutter(trs[0].find('td').text.strip())
        c2['Title'] = head_title
        header = []
        ths = trs[1].find_all('th')
        for n, th in enumerate(ths):
            if n == 0:
                continue
            header.append(th.text.strip())
        c2['Header'] = header
        ocean_idx = 2
        while True:
            try:
                oc = trs[ocean_idx]
                tds = oc.find_all('td')
                for n, td in enumerate(tds):
                    if n == 0:
                        ocean = f'{td.text.strip()}'
                        c3 = c2[ocean] = {}
                    else:
                        head = header[n-1]
                        htext = f'{td.text.strip()}'
                        c3[head] = htext
                ocean_idx += 1
            except IndexError:
                break


if __name__ == '__main__':
    CIA_XrefHydrographicDataCodes()
