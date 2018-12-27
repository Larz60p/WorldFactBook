# copyright (c) 2018  Larz60+
import ScraperPaths
import GetPage
import CIA_ScanTools
from lxml import html
from lxml.cssselect import CSSSelector
from lxml import etree
from lxml.etree import XPath
import re
import os
import sys


class CIA_InternationalOrgnizationsAndGroups:
    def __init__(self):
        self.spath = ScraperPaths.ScraperPaths()
        self.gp = GetPage.GetPage()
        self.getpage = self.gp.get_page
        self.get_filename = self.gp.get_filename
        self.cst = CIA_ScanTools.CIA_Scan_Tools()

        self.fact_links = self.cst.fact_links

        self.mainurl = 'https://www.cia.gov/library/publications/resources/the-world-factbook/appendix/appendix-b.html'
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

    def scrape_text(self):
        tree = html.fromstring(self.mainpage)
        # html.open_in_browser(tree)
        c1 = self.fact_links['InternationalOrginizationsAndGroups'] = {}
        childno = 1
        while True:
            xx = tree.cssselect(f'#GetAppendix_B > li:nth-child({childno}) > span:nth-child(1)')
            # print(xx[0].text)
            if len(xx) == 0:
                break
            title = self.remove_fluff(xx[0].text.strip())
            # print(f'Title: {title}')
            c2 = c1[title] = {}
            
            # yy = tree.cssselect(f'li.ln-a:nth-child({childno}) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1)')
            yy = tree.cssselect(f'#GetAppendix_B > li:nth-child({childno}) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1)')
            if len(yy[0]) > 1:
                # print(f'\n...length yy: {len(yy[0])}')
                c3 = c2['Description'] = []
                # print(f'{html.tostring(yy[0])}')
                for n, element in enumerate(yy[0]):
                    if n % 2 == 0:
                        desc = self.cst.fluffinutter(html.tostring(element).decode('utf-8'))
                        c3.append(desc)
            else:
                c3 = c2['Description'] = []
                description = self.remove_fluff(yy[0].text.strip())
                c3.append(description)
                # print(f'Description: {description}')
            childno += 1


if __name__ == '__main__':
    CIA_InternationalOrgnizationsAndGroups()
