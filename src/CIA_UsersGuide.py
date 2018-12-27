# copyright (c) 2018  Larz60+
import ScraperPaths
import GetPage
import CIA_ScanTools
from bs4 import BeautifulSoup
import sys
import os


class CIA_UsersGuide:
    def __init__(self):
        self.spath = ScraperPaths.ScraperPaths()
        self.gp = GetPage.GetPage()
        self.getpage = self.gp.get_page
        self.get_filename = self.gp.get_filename
        self.cst = CIA_ScanTools.CIA_Scan_Tools()

        self.fact_links = self.cst.fact_links

        self.mainurl = 'https://www.cia.gov/library/publications/resources/the-world-factbook/docs/guidetowfbook.html'
        self.filename = self.get_filename(self.mainurl)

        self.mainpage = self.getpage(self.mainurl, self.filename)

        self.scrape_page()
        self.cst.save_fact_links()
    
    def get_categories(self, soup):
        cats = []
        h2s = soup.find_all('h2')
        for n, h2 in enumerate(h2s):
            if n < 2:
                continue
            h2 = h2.text.strip()[:-3]
            cats.append(h2)
            # print(f'\n{h2}')
        return cats

    def scrape_page(self):
        baseurl = 'https://www.cia.gov/library/publications/resources/the-world-factbook/graphics/'
        prettify = self.cst.prettify

        soup = BeautifulSoup(self.mainpage, 'lxml')
        maintable = soup.find('table')
        # tmpfile = self.spath.tmppath / 'maintable.html'
        # with tmpfile.open('w') as fp:
        #     fp.write(f'===========================================================================\n')
        #     fp.write(f'maintable:{prettify(maintable, indent=4)}\n')
        firsttrs = maintable.find_all('tr')
        # tmpfile = self.spath.tmppath / 'firsttrs.html'
        # with tmpfile.open('w') as fp:
        #     for n, tr in enumerate(firsttrs):
        #         fp.write(f'===========================================================================\n')
        #         fp.write(f'firsttrs_{n}: {prettify(tr, indent=4)}\n\n')


        #narrow down to profileguide div
        profilediv = firsttrs[5].find('div', {'id': 'profileguide'})
        # tmpfile = self.spath.tmppath / 'profilediv.html'
        # with tmpfile.open('w') as fp:
        #     fp.write(f'===========================================================================\n')
        #     fp.write(f'profilediv: {prettify(profilediv, 2)}\n')
        
        # insert new tags to help split html. These will go just before each <h2> tag
        all_h2_tags = profilediv.find_all('h2')
        tmpfile = self.spath.tmppath / 'h2_parent_child.html'
        with tmpfile.open('w') as fp:
            fp.write(f'\n===========================================================================\n')
            fp.write(f'===========================================================================\n')
            for n, h2 in enumerate(all_h2_tags):
                parent = h2.findParent()
                child = h2.findChild()
                fp.write(f'\nParent_{n}:\n    {parent}')
                fp.write(f'\n===========================================================================\n')
                fp.write(f'\nh2_{n}:\n    {h2}')
                fp.write(f'\n===========================================================================\n')
                fp.write(f'\nChild{n}:\n    {child}')
            fp.write(f'\n===========================================================================\n')
            fp.write(f'===========================================================================\n')
        #     for n, tr in enumerate(firsttrs):
        #         fp.write(f'firsttrs_{n}: {prettify(tr, 2)}\n\n')






        sys.exit(0)
        # before tables, find major td
        first_trs = table.find_all('tr')
        # for n, tr in enumerate(first_trs):
        #     print(f'\n===========================================================================')
        #     print(f'tr_{n}\n{prettify(tr, 2)}')
        divs = first_trs[5].find_all('div')
        categories = self.get_categories(soup)
        c1 = self.fact_links['FactbookGuide'] = {}
        for n, div in enumerate(divs):
            # category = categories[n]
            print(f'\n===========================================================================')
            # print(f'Category: {category}')
            print(f'table_0, tr_5, div_{n}\n{prettify(div, 2)}')
            # trs = div.find_all('tr')
            # for n1, tr in enumerate(trs):
            #     # print(f'\ndiv_{n} category: {category}, tr_{n1}:\n{prettify(tr, 2)}')
            #     tds = tr.find_all('td')
            #     print(f'\n=================================================================================')
            #     if tds is None:
            #         print(f"\ndiv_{n} category: {category}, tr_{n1}: No td's")
            #         continue
            #     for n2, td in enumerate(tds):
            #         print(f'\ndiv_{n} category: {category}, tr_{n1}, td_{n2}:\n{prettify(td, 2)}')
            #         images = td.find_all('img')
            #         if images is not None:
            #             for n3, image in enumerate(images):
            #                 if n3 > 0:
            #                     print()
            #                 alt = image.get('alt')
            #                 height = image.get('height')
            #                 width = image.get('width')
            #                 style = image.get('style')
            #                 iurl = image.get('src')
            #                 ims = iurl.split('/')
            #                 url = f'{baseurl}{ims[1]}'
            #                 filename = self.get_filename(url)
            #                 caption = image.text.strip()
            #                 print(f'    image_{n3}: alt: {alt}, height: {height}, width: {width}, style: {style}, caption: {caption}\n    url: {url}\n    filename: {filename.resolve()}')
            #                 self.getpage(url, filename, image=True)
            #             if isinstance(tds, list):
            #                 for n3, td in enumerate(tds):
            #                     print(f'\n    div_{n} category: {category}, tr_{n1}, td_{n2}, td_{n3}:\n{td}')
            #             else:
            #                 print(f'\n    single td: {td}')

if __name__ == '__main__':
    CIA_UsersGuide()
