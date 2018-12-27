# copyright (c) 2018  Larz60+
import ScraperPaths
import GetPage
import CIA_ScanTools
from bs4 import BeautifulSoup
import os


class CIA_WeightsAndMeasures:
    def __init__(self):
        self.spath = ScraperPaths.ScraperPaths()
        self.gp = GetPage.GetPage()
        self.getpage = self.gp.get_page
        self.get_filename = self.gp.get_filename
        self.cst = CIA_ScanTools.CIA_Scan_Tools()

        self.fact_links = self.cst.fact_links

        self.mainurl = 'https://www.cia.gov/library/publications/resources/the-world-factbook/appendix/appendix-g.html'

        self.filename = self.get_filename(self.mainurl)

        self.mainpage = self.getpage(self.mainurl, self.filename)

        self.scrape_page()
        self.cst.save_fact_links()

    def scrape_page(self):
        soup = BeautifulSoup(self.mainpage, 'lxml')
        c1 = self.fact_links['Weights and Measures'] = {}
        ttl = soup.find('td', {'style': 'background-image: url(../graphics/gold_gradiant.gif); '})
        title = ttl.text.strip()
        c1['Title'] = title
        entry1 = soup.find('div', {'class': "category_data"})
        description = entry1.text.strip()
        c1['Description'] = description
        table = soup.find_all('table')
        table_no = 4
        while True:
            try:
                trs = table[table_no].find_all('tr')
                for n, tr in enumerate(trs):
                    if n == 0:
                        name = tr.find('th').text.strip()
                        c2 = c1[name] = {}
                    elif n == 1:
                        header = []
                        ths = tr.find_all('th')
                        for th in ths:
                            header.append(th.text.strip())
                        c2['Header'] = header
                    else:
                        tds = tr.find_all('td')
                        entry = []
                        for n1, td in enumerate(tds):
                            ent = td.text.strip()
                            if n1 == 0:
                                sub = ent
                            else:
                                entry.append(ent)
                        if len(entry) == 1:
                            c2[sub] = entry[0]
                        else:
                            c2[sub] = entry
                        
                table_no += 1
            except IndexError:
                break


if __name__ == '__main__':
    CIA_WeightsAndMeasures()
