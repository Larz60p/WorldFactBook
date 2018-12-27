# copyright (c) 2018  Larz60+
import ScraperPaths
import GetPage
import CIA_ScanTools
from lxml import html
from lxml.cssselect import CSSSelector
# from lxml.html import clean_html
from lxml import etree
from lxml.etree import XPath
import re
import os
import sys


class CIA_EnvironmentalAgreements:
    def __init__(self):
        self.spath = ScraperPaths.ScraperPaths()
        self.gp = GetPage.GetPage()
        self.getpage = self.gp.get_page
        self.get_filename = self.gp.get_filename
        self.cst = CIA_ScanTools.CIA_Scan_Tools()

        self.fact_links = self.cst.fact_links

        self.mainurl = 'https://www.cia.gov/library/publications/resources/the-world-factbook/appendix/appendix-c.html'
        self.filename = self.get_filename(self.mainurl)

        self.mainpage = self.getpage(self.mainurl, self.filename)

        self.scrape_text()
        self.cst.save_fact_links()

    def remove_fluff(self, item):
        if '\r\n' in item or '\n' in item:
            nitem = ''
            parts = item.split('\n')
            for part in parts:
                nitem = f'{nitem.strip()} {part.strip()}'
            return nitem
        else:
            return item

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
        for n, item in enumerate(intrum):
            item = item.replace('&#160;', '')
            if '<' in item:
                item = self.remove_tags(item)
            newtext = f'{newtext} {item.strip()}'
        return newtext

    def scrape_text(self):
        tree = html.fromstring(self.mainpage)
        # html.open_in_browser(tree)
        c1 = self.fact_links['EnvironmentalAgreements'] = {}
        childno = 1
        while True:
            xx = tree.cssselect(f'#GetAppendix_C > li:nth-child({childno}) > span:nth-child(1)')
            if len(xx) == 0:
                break
            title = xx[0].text.strip()
            c2 = c1[title] = {}
            yy = tree.cssselect(f'#GetAppendix_C > li:nth-child({childno}) > div:nth-child(2)')
            if len(yy[0]) > 1:
                c3 = c2['Description'] = []
                for n, element in enumerate(yy[0]):
                    if n % 2 == 0:
                        desc = self.fluffinutter(html.tostring(element).decode('utf-8'))
                        c3.append(desc)
            else:
                c3 = c2['Description'] = []
                description = self.remove_fluff(yy[0].text.strip())
                c3.append(description)
            childno += 1

if __name__ == '__main__':
    CIA_EnvironmentalAgreements()
