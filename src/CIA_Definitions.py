# copyright (c) 2018  Larz60+
from lxml import html
import ScraperPaths
import CIA_ScanTools
import GetPage
import os
import json
import sys
from bs4 import BeautifulSoup


class CIA_Definitions:
    def __init__(self):
        self.spath = ScraperPaths.ScraperPaths()
        self.gp = GetPage.GetPage()
        self.getpage = self.gp.get_page
        self.get_filename = self.gp.get_filename
        self.cst = CIA_ScanTools.CIA_Scan_Tools(seed=100, precision=5)

        self.fact_links = self.cst.fact_links
        lid = self.cst.AutoId
        self.nextid = lid.next

        url = 'https://www.cia.gov/library/publications/resources/the-world-factbook/docs/notesanddefs.html'
        filename = self.get_filename(url)
        
        self.get_definitions(url, filename)
        self.cst.save_fact_links()

    def get_definitions(self, url, filename):
        baseurl = 'https://www.cia.gov/library/publications/resources/the-world-factbook'
        page = self.getpage(url, filename)
        c1 = self.fact_links['Deinitions'] = {}
        soup = BeautifulSoup(page, 'lxml')
        # Golden... do not change see notepadd++ output.txt
        groups = soup.find_all('div', {'name': True})
        definition_id = ''

        for group in groups:
            definition_id = group.get('name').strip()
            if len(definition_id) == 0:
                definition_id = self.nextid()
            definition_name = group.find('td').text.strip()
            c2 = c1[definition_id] = {}
            c2['Name'] = definition_name
            catdat = group.find_all("div",{"class":"category_data"})
            definition = catdat[1].text.strip()
            c2['Definition'] = definition
            link = group.find('a')
            if link:
                mpart = link.get('href')[2:]
                mtext = link.text.strip()
                murl = f'{baseurl}{mpart}'
                mfilename = self.get_filename(murl)
                print(f'murl: {murl}\nmfilename: {mfilename.resolve()}')
                c2['URL'] = murl
                c2['Filename'] = os.fspath(mfilename)
                self.getpage(murl, mfilename)

if __name__ == '__main__':
    CIA_Definitions()
