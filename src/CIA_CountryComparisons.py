import ScraperPaths
import GetPage
import CIA_ScanTools
from lxml import html
from lxml.cssselect import CSSSelector
from lxml.html.clean import clean_html
from lxml import etree
import sys
import os


class CIA_CountryComparisons:
    def __init__(self):
        self.spath = ScraperPaths.ScraperPaths()
        self.gp = GetPage.GetPage()
        self.getpage = self.gp.get_page
        self.get_filename = self.gp.get_filename
        self.cst = CIA_ScanTools.CIA_Scan_Tools()

        self.fact_links = self.cst.fact_links

        self.mainurl = 'https://www.cia.gov/library/publications/resources/the-world-factbook/rankorder/rankorderguide.html'
        self.filename = self.get_filename(self.mainurl)

        self.mainpage = self.getpage(self.mainurl, self.filename)

        self.scrape_page_etree()
        self.cst.save_fact_links()

    def scrape_page_etree(self):
        page = clean_html(self.mainpage)
        tree = etree.HTML(page)
        # Uncomment following during development to fetch select base
        # html.open_in_browser(tree)
        title_no = -1
        element = 0
        c1 = self.fact_links['CountryComparisons'] = {}
        while True:
            baseurl = 'https://www.cia.gov/library/publications/resources/the-world-factbook'
            title_no += 2
            element  += 2
            selector = f'h2.question:nth-child({title_no}) > a:nth-child(1) > strong:nth-child(1)'
            #           h2.question:nth-child(1) > a:nth-child(1) > strong:nth-child(1)
            h2 = tree.cssselect(selector)
            if len(h2) == 0:
                break
            title = h2[0].text.strip()[:-2]
            print(f'Title: {title}')
            inner_element = 1
            c2 = c1[title] = {}
            while(True):
                # Geography - Area
                selector = f'div.answer:nth-child({element}) > div:nth-child({inner_element}) > a:nth-child(1)'
                category = tree.cssselect(selector)
                if len(category) == 0:
                    break
                link = category[0].cssselect('a')
                purl = link[0].get('href')[2:]
                # https://www.cia.gov/library/publications/resources/the-world-factbook/rankorder/2147rank.html
                print(f'purl: {purl}')
                url = f'{baseurl}{purl}'
                link_name = link[0].text.strip()[:-1]
                filename = self.get_filename(url)
                print(f'filename: {filename}')
                self.getpage(url, filename)
                c3 = c2[link_name] = {}
                c3['URL'] = url
                c3['Filename'] = os.fspath(filename)
                inner_element += 1

if __name__ == '__main__':
    CIA_CountryComparisons()
