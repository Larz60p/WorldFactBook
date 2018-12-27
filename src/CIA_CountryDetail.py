# copyright (c) 2018  Larz60+
import ScraperPaths
import GetPage
import CIA_ScanTools
from bs4 import BeautifulSoup
import os
import sys

class CIA_CountryDetail:
    def __init__(self):
        self.spath = ScraperPaths.ScraperPaths()
        self.gp = GetPage.GetPage()
        self.getpage = self.gp.get_page
        self.get_filename = self.gp.get_filename
        self.cst = CIA_ScanTools.CIA_Scan_Tools()

        self.fact_links = self.cst.fact_links
        self.mainurl = 'https://www.cia.gov/library/publications/world-leaders-1/index.html'
    
        self.filename = self.get_filename(self.mainurl)

        self.mainpage = self.getpage(self.mainurl, self.filename, encoding=None)

        self.scrape_page()
        self.cst.save_fact_links()
    
    def scrape_page(self):
        soup = BeautifulSoup(self.mainpage, 'lxml')
        newpage = None

        c1 = self.fact_links['WorldLeaders'] = {}

        maindiv = soup.find('div', {'class': 'demo'})
        subdivs = maindiv.find_all('div')
        table = subdivs[0].find('table', {'id': 'abbreviationsTable'})
        trs = table.find_all('tr')

        # First extract abbreviations used in titles from div[0]
        c2 = c1['Abbreviations'] = {}
        for n, tr in enumerate(trs):
            # skip first 2 nothing needed
            if n < 2:
                continue
            # Remainder each contain a single abbreviation trs[2] is heading
            if n == 2:
                ths = tr.find_all('th')
                column1 = ths[0].text.strip()
                column2 = ths[1].text.strip()
                c2['Header'] = [column1, column2]
            else:
                tds = tr.find_all('td')
                terms = []
                for n1, td in enumerate(tds):
                    terms.append(td.find('div').text.strip())
                c2[terms[0]] = terms[1]

        c2 = c1['Country Detail'] = {}
        # Next get files for each country and extract contents
        country_baseurl = 'https://www.cia.gov/library/publications/resources/world-leaders-1/'
        uls = soup.find_all('ul')

        ul_no = 12
        lastone = False
        while True:
            try:
                ul = uls[ul_no]
                ul_no += 1

                li_list = ul.find_all('li')
                for n, li in enumerate(li_list):
                    link = li.find('a')
                    country = link.text.strip()
                    if country == 'Zimbabwe':
                        lastone = True
                    print(f'Processing leaders for {country}')
                    c3 = c2[country] = {}
                    purl = link.get('href')
                    if purl.startswith('http'):
                        url = purl
                    else:
                        url = f"{country_baseurl}{link.get('href')}"
                    filename = self.get_filename(url)
                    newpage = self.getpage(url, filename)
                    c3['URL'] = url
                    c3['Filename'] = os.fspath(filename)

                    new_soup = BeautifulSoup(newpage, 'lxml')
                    newuls = new_soup.find_all('ul')
                    lis = newuls[31].find_all('li')
                    c4 = c3['Leader List'] = {}
                    for n2, li in enumerate(lis):
                        span = li.find('span', {'class': 'title'})
                        title = span.text.strip()

                        # c5 = c4[f'{str(n2)}'] = {}
                        # c5['Title'] = title
                        span1 = li.find('span', {'class': 'cos_name'})
                        name = span1.text.strip()
                        # c5['Name'] = name
                        c4[title] = name
                if lastone:
                    break
            except IndexError:
                break


if __name__ == '__main__':
    CIA_CountryDetail()
