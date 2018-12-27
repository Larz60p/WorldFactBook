# copyright (c) 2018  Larz60+
import ScraperPaths
import GetPage
import CIA_ScanTools
from bs4 import BeautifulSoup
import os
import sys


class CIA_Gallery:
    def __init__(self):
        self.spath = ScraperPaths.ScraperPaths()
        self.gp = GetPage.GetPage()
        self.getpage = self.gp.get_page
        self.get_filename = self.gp.get_filename
        self.cst = CIA_ScanTools.CIA_Scan_Tools()

        self.fact_links = self.cst.fact_links

        self.mainurl = 'https://www.cia.gov/library/publications/resources/the-world-factbook/docs/gallery.html'

        self.filename = self.get_filename(self.mainurl)

        self.mainpage = self.getpage(self.mainurl, self.filename)

        self.scrape_page()
        self.cst.save_fact_links()

    def get_sp(self):
        sp = ''
        if self.level:
            sp = ' ' * self.level
        return sp

    def scrape_page(self):
        years = []
        soup = BeautifulSoup(self.mainpage, 'lxml')

        c1 = self.fact_links['Gallery'] = {}

        tables = soup.find_all('table')
        trs = tables[2].find_all('tr')

        header_info = trs[2].find('div').text.strip()
        description = self.cst.fluffinutter(header_info)
        c1['Description'] = description
        st1s = tables[2].find_all('img')
        for image in st1s:
            title = image.get('title')
            if title is not None and 'Cover' in title:
                year = image.get('year')
                if year not in years:
                    years.append(year)
        print(f'the following years will be downloaded" {years}\n\n')

        for year in years:
            c2 = c1[year] = {}
            print(f'fetching graphics for {year}')

            if int(year) > 1987:
                back_thumb = f'https://www.cia.gov/library/publications/resources/the-world-factbook/graphics/covers/thumbnails/{int(year)}-back.jpg'
                back_thumb_file = self.get_filename(back_thumb)
                self.getpage(back_thumb, back_thumb_file, image=True)
                c2['BackThumbURL'] = back_thumb
                c2['BackThumbFilename'] = os.fspath(back_thumb_file)

            if int(year) > 1986:
                back_jpg = f'https://www.cia.gov/library/publications/resources/the-world-factbook/graphics/covers/{int(year)}-back.jpg'
                back_file = self.get_filename(back_jpg)
                self.getpage(back_jpg, back_file, image=True)
                c2['BackJpgURL'] = back_jpg
                c2['BackJpgFilename'] = os.fspath(back_file)

            front_thumb = f'https://www.cia.gov/library/publications/resources/the-world-factbook/graphics/covers/thumbnails/{int(year)}-front.jpg'
            front_thumb_file = self.get_filename(front_thumb)
            self.getpage(front_thumb, front_thumb_file, image=True)
            c2['FrontThumbURL'] = front_thumb
            c2['FrontThumbFilename'] = os.fspath(front_thumb_file)


            front_jpg = f'https://www.cia.gov/library/publications/resources/the-world-factbook/graphics/covers/{int(year)}-front.jpg'
            front_file = self.get_filename(front_jpg)
            self.getpage(front_jpg, front_file, image=True)
            c2['FrontJpgURL'] = front_jpg
            c2['FrontJpgFilename'] = os.fspath(front_file)

if __name__ == '__main__':
    CIA_Gallery()
