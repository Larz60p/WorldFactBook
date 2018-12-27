# copyright (c) 2018  Larz60+
import lxml.etree as ET
from lxml.etree import Element
import GetPage
import pprint
import requests
from io import BytesIO
from bs4 import BeautifulSoup
from pathlib import PurePath
import ScraperPaths
import CIA_ScanTools
import os
import sys
import types


class CIA_CountryProfiles:
    def __init__(self):
        # need to set cwd to source path (will allow relative file paths)
        self.home = os.path.abspath(os.path.dirname(__file__))
        os.chdir(self.home)
        self.spath = ScraperPaths.ScraperPaths()
        self.cst = CIA_ScanTools.CIA_Scan_Tools()
        self.fact_links = self.cst.fact_links
        self.gp = GetPage.GetPage()
        self.getpage = self.gp.get_page
        self.get_filename = self.gp.get_filename

        url = 'https://www.cia.gov/library/publications/resources/' \
              'the-world-factbook/docs/profileguide.html'
        filename = self.get_filename(url)
        self.prettyfile = self.spath.tmppath / 'PrettyProfile.html'

        self.mainpage = self.getpage(url, filename)
        self.xbase = '/html/body/div[4]/section/div[2]/div[2]/article/div/' \
                     'div/table/tbody/tr[4]/td/div/div[2]'

        self.tree = None

        self.scrape_page()
        self.cst.save_fact_links()

    def get_pretty_file(self):
        soup = BeautifulSoup(self.mainpage, 'lxml')
        with self.prettyfile.open('w') as fp:
            fp.write(soup.prettify(formatter="html"))
        parser = ET.HTMLParser(remove_blank_text=True)
        return ET.parse(os.path.abspath(self.prettyfile.resolve()), parser)

    def walk_node(self, element, c2):
        for n, sibling in enumerate(element.itersiblings()):
            if sibling.tag == 'h2':
                break

            def get_children(base_element, level=0):
                for n1, child in enumerate(base_element.iterchildren()):
                    if len(child):
                        newlevel = level + 1
                        get_children(child, level=newlevel)
                        newlevel -= 1
                    else:
                        c3 = c2
                        if child.tag == 'a':
                            url = child.get('href')
                            filename = self.get_filename(url)
                            title = child.text.strip()
                            # print(f'    URL: {url}')
                            # print(f'    filename: {filename.resolve()}')
                            # print(f'    title: {title}')
                            c3 = c2[title] = {}
                            c3['URL'] = url
                            c3['Filename'] = os.fspath(filename)
                            self.getpage(url, filename)
                        elif child.tag == 'span':
                            subtitle = child.text.strip()
                            # print(f'        subtitle: {subtitle}')
                            if 'Subcat' in c3:
                                c3['Subcat'].append(subtitle)
                            else:
                                c3['Subcat'] = [subtitle]

            if len(sibling):
                get_children(sibling)

    def scrape_page(self):
        c1 = self.fact_links['CountryProfiles'] = {}
        self.tree = self.get_pretty_file()
        header_no = 1
        while True:
            cxpath = f'{self.xbase}/h2[{header_no}]'
            element = self.tree.xpath(cxpath)
            if element and len(element):
                catxpath = f'{cxpath}/a/strong'
                category = self.tree.xpath(catxpath)[0].text.strip()
                # print(f'Category: {category}')
                c2 = c1[category] = {}
                element = element[0]
                if len(element):
                    self.walk_node(element, c2)
                    header_no += 1
            else:
                break

        # while True:
        #     try:
        #         cxpath = f'{self.xbase}/h2[{header_no}]'
        #         element = self.tree.xpath(cxpath)
        #         print(f'element: {ET}')
        #         self.get_category(element[0], cxpath, c1, header_no)
        #         header_no += 1
        #     except IndexError:
        #         break
        # self.cst.display_dict(c1)


if __name__ == '__main__':
    CIA_CountryProfiles()
