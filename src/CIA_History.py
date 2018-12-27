# copyright (c) 2018  Larz60+
from lxml import html
import ScraperPaths
import CIA_ScanTools
import GetPage
import os
import json
import sys
from bs4 import BeautifulSoup


class CIA_History:
    def __init__(self):
        self.spath = ScraperPaths.ScraperPaths()
        self.gp = GetPage.GetPage()
        self.getpage = self.gp.get_page
        self.get_filename = self.gp.get_filename
        self.cst = CIA_ScanTools.CIA_Scan_Tools()

        self.fact_links = self.cst.fact_links

        url = 'https://www.cia.gov/library/publications/resources/the-world-factbook/docs/history.html'
        filename = self.get_filename(url)
        
        self.get_history(url, filename)
        self.cst.save_fact_links()

    def get_history(self, url, filename):
        page = self.getpage(url, filename)
        c1 = self.fact_links['History'] = {}
        soup = BeautifulSoup(page, 'lxml')
        tables = soup.findAll('table')
        trs = tables[1].find_all('tr')
        for n, tr in enumerate(trs):
            if n == 0:
                item = tr.find('span', {'class': 'h1'})
                title = item.text
                c2 = c1[title] = {}
            elif n == 1:
                allps = tr.find_all('p')
                descr = []
                for p in allps:
                    descr.append(p.text)
                c2['Description'] = descr
        trs = tables[3].find_all('tr')
        for n, tr in enumerate(trs):
            if n == 0:
                title1 = tr.find('span').text
                c3 = c2[title1] = {}
            elif n == 1:
                subtext = tr.find('p').text
                c3['subtitle'] = subtext
            elif n == 2:
                newtable = tr.find('table')
                newtrs = newtable.find_all('tr')
                for newtr in newtrs:
                    newtds = newtr.find_all('td')
                    year = newtds[0].text
                    year_text = newtds[1].text
                    c3[year] = year_text

if __name__ == '__main__':
    CIA_History()
