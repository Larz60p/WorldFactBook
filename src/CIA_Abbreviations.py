# copyright (c) 2018  Larz60+
import ScraperPaths
import GetPage
import CIA_ScanTools
from lxml import html
from lxml.cssselect import CSSSelector
from lxml.html.clean import clean_html
from lxml import etree
import sys
import os


class CIA_Abbreviations:
    def __init__(self):
        self.spath = ScraperPaths.ScraperPaths()
        self.gp = GetPage.GetPage()
        self.getpage = self.gp.get_page
        self.get_filename = self.gp.get_filename
        self.cst = CIA_ScanTools.CIA_Scan_Tools()

        self.fact_links = self.cst.fact_links

        self.mainurl = 'https://www.cia.gov/library/publications/resources/the-world-factbook/appendix/appendix-a.html'
        self.filename = self.get_filename(self.mainurl)

        self.mainpage = self.getpage(self.mainurl, self.filename)

        self.scrape_page_etree()
        self.cst.save_fact_links()

    def scrape_page_etree(self):
        page = clean_html(self.mainpage)
        tree = etree.HTML(page)
        # Uncomment following during development to fetch select base
        # html.open_in_browser(tree)
        c1 = self.fact_links['Abbreviations'] = {}
        word_id = 1
        while True:
            word_selector = f'#GetAppendix_A > li:nth-child({word_id}) > span:nth-child(1)'
            word_tag = tree.cssselect(word_selector)
            if len(word_tag) == 0:
                break
            word = word_tag[0].text.strip()
            desc_selector = f'#GetAppendix_A > li:nth-child({word_id}) > div:nth-child(2)'            #                 #GetAppendix_A > li:nth-child(2) > div:nth-child(2)
            desc_tag = tree.cssselect(desc_selector)
            description = desc_tag[0].text.strip()
            c1[word] = description
            print(f'{word}: {description}')
            word_id += 1


if __name__ == '__main__':
    CIA_Abbreviations()
