# copyright (c) 2018  Larz60+
import ScraperPaths
import GetPage
import CIA_ScanTools
from bs4 import BeautifulSoup
import os
import sys


class CIA_RefMaps:
    def __init__(self):
        self.spath = ScraperPaths.ScraperPaths()
        self.gp = GetPage.GetPage()
        self.getpage = self.gp.get_page
        self.get_filename = self.gp.get_filename
        self.cst = CIA_ScanTools.CIA_Scan_Tools()

        self.fact_links = self.cst.fact_links

        self.mainurl = 'https://www.cia.gov/library/publications/resources/the-world-factbook/docs/refmaps.html'

        self.filename = self.get_filename(self.mainurl)

        self.mainpage = self.getpage(self.mainurl, self.filename)

        self.scrape_page()
        self.cst.save_fact_links()

    def get_header(self, table, baseurl, c1):
        # Heading is in tables[2]
        #Maps in table[4] - Table[30]
        header_trs = table.find_all('tr')        
        image1 = header_trs[0].find('td')
        style = image1.get('style')
        url = f"{baseurl}{style.split('(')[1].split(')')[0][2:]}"
        filename = self.get_filename(url)
        self.getpage(url, filename, image=True)
        c2 = c1['HeadImages'] = {}
        c3 = c2[filename.name] = {}
        c3['style'] = style
        c3['URL'] = url
        c3['Filename'] = os.fspath(filename)
        image2 = header_trs[1].find('img')
        caption = image2.get('alt')
        purl = image2.get('src')
        url = f"{baseurl}/docs/{purl}"
        filename = self.get_filename(url)
        self.getpage(url, filename, image=True)
        c3 = c2[filename.name] = {}
        c3['Caption'] = caption
        c3['URL'] = url
        c3['Filename'] = os.fspath(filename)
        return c3

    def get_sp(self):
        sp = ''
        if self.level:
            sp = ' ' * self.level
        return sp

    def scrape_page(self):
        baseurl = 'https://www.cia.gov/library/publications/resources/the-world-factbook'
        soup = BeautifulSoup(self.mainpage, 'lxml')
        c1 = self.fact_links['Regional and World Maps'] = {}
        tables = soup.find_all('table')
        c3 = self.get_header(tables[2], baseurl, c1)

        # Last used table is 84
        table_no = 4
        while True:
            print(f'table_no: {table_no}')
            try:
                table = tables[table_no]
                trs = table.find_all('tr')
                map_name = None
                url1 = url2 = url3 = caption1 = caption2 = caption3 = \
                    filename1 = filename2 = filename3 = None
                for n, tr in enumerate(trs):
                    if n == 0:
                        image = tr.find('img')
                        caption1 = image.get('regionname')
                        purl = image.get('src')
                        url1 = f"{baseurl}/docs/{purl}"
                        filename1 = self.get_filename(url1)
                        self.getpage(url1, filename1, image=True)
                    elif n == 1:
                        map_name  = tr.find('td').text.strip()
                    elif n == 2:
                        divs = tr.find_all('div')
                        for n1, div in enumerate(divs):
                            if n1 == 0:
                                link = div.find('a')
                                url2 = link.get('href')
                                caption2 = link.text.strip()
                                filename2 = self.get_filename(url2)
                                self.getpage(url2, filename2, image=True)
                            elif n1 == 1:
                                link = div.find('a')
                                url3 = link.get('href')
                                caption3 = link.text.strip()
                                filename3 = self.get_filename(url3)
                                self.getpage(url3, filename3, image=True)
                c4 = c3[map_name] = {}
                c5 = c4['image1'] = {}
                c5['URL'] = url1
                c5['Filename'] = os.fspath(filename1)
                c5['Caption'] = caption1
                c5 = c4['image2'] = {}
                c5['URL'] = url2
                c5['Filename'] = os.fspath(filename2)
                c5['Caption'] = caption2
                c5 = c4['pdf'] = {}
                c5['URL'] = url3
                c5['Filename'] = os.fspath(filename3)
                c5['Caption'] = caption3
                table_no += 1
            except IndexError:
                break



if __name__ == '__main__':
    CIA_RefMaps()
