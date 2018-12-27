# copyright (c) 2018  Larz60+
import ScraperPaths
import GetPage
import CIA_ScanTools
from bs4 import BeautifulSoup
import re
import os
import sys


class CIA_Faqs:
    def __init__(self):
        self.spath = ScraperPaths.ScraperPaths()
        self.gp = GetPage.GetPage()
        self.getpage = self.gp.get_page
        self.get_filename = self.gp.get_filename
        self.cst = CIA_ScanTools.CIA_Scan_Tools()

        self.soup = None
        self.category_id = -1
        self.categories = []

        self.fact_links = self.cst.fact_links

        self.mainurl = 'https://www.cia.gov/library/publications/resources/the-world-factbook/docs/faqs.html'

        self.filename = self.get_filename(self.mainurl)

        self.mainpage = self.getpage(self.mainurl, self.filename)

        self.scrape_page()
        self.cst.save_fact_links()

    def next_category(self):
        if self.category_id == -1:
            headers = self.soup.find_all('h2')
            for n, hd in enumerate(headers):
                if n < 2:
                    continue
                head = hd.text.strip()[:-4]
                self.categories.append(head)
            self.categories.append(None)
        self.category_id += 1
        return self.categories[self.category_id]

    def scrape_page(self):
        self.soup = BeautifulSoup(self.mainpage, 'lxml')
        prettyfile = self.spath.tmppath / 'faqs_pretty.html'

        with prettyfile.open('w') as fp:
            fp.write(self.soup.prettify())

        c1 = self.fact_links['Faqs'] = {}

        # Start with tbody
        tables = self.soup.find_all('table')

        title = self.cst.fluffinutter(tables[2].find('div', {'class': 'region'}).text.strip())
        c1['Title'] = title
        main_descritpion = self.cst.fluffinutter(tables[2].find('td', {'class': 'category_data'}).text.strip())
        c1['Description'] = main_descritpion


        table_no = 3
        while True:
            category = self.next_category()
            c2 = c1[category] = {}
            seqno = 0
            faq_trs = tables[table_no].find_all('tr')
            for n, tr in enumerate(faq_trs):
                tds = tr.find_all('td')
                for n1, td in enumerate(tds):
                    if td.has_attr("height") and td.get('height') == '10':
                        continue
                    elif td.has_attr("class"):
                        cname = td.get('class')[0]
                        if cname == 'faqQuestion':
                            question = self.cst.fluffinutter(td.text.strip())
                        elif cname == 'faqAnswer':
                            answer = self.cst.fluffinutter(td.text.strip())
                            faq_no = f'FAQ Number {seqno}:'
                            c3 = c2[faq_no] = {}
                            c3['Question'] = question
                            c3['Answer'] = answer
                            seqno += 1
            if table_no == 9:
                break
            table_no += 1

if __name__ == '__main__':
    CIA_Faqs()
