# copyright (c) 2018  Larz60+
# Comparison data is found in the data/CIA/library/publications/resources/the-world-factbook/fields directory
# Each file is arranged by country, and contains comparison data on one subject
# The fact_link entries will be self.fact_links['Country Comparisons'][comparison_type][country][info]
# example comparison type: GDP (PURCHASING POWER PARITY)
# There will also be a comparison type description field at the comparison_type level
# If missing pages are found, they will be downloaded as encountered
import ScraperPaths
import CIA_ScanTools
import GetPage
import codecs
from bs4 import BeautifulSoup
import os
import sys


class CIA_ExtractComparisons:
    def __init__(self):
        self.spath = ScraperPaths.ScraperPaths()
        self.gp = GetPage.GetPage()
        self.getpage = self.gp.get_page
        self.get_filename = self.gp.get_filename
        self.cst = CIA_ScanTools.CIA_Scan_Tools()

        self.fact_links = self.cst.fact_links

        self.extract_comparison_data()
        self.cst.save_fact_links()

    def extract_comparison_data(self):
        baseurl = 'https://www.cia.gov/library/publications/resources/the-world-factbook'
        field_path = self.spath.cia_lprt_fields
        field_file_list = [filename for filename in field_path.iterdir() if filename.is_file()]
        c1 = self.fact_links['Country Comparisons'] = {}
        for filename in field_file_list:
            print(f'processing file: {filename.name}')
            file_name = filename.resolve()
            with codecs.open(file_name, "r", encoding='utf-8', errors='ignore') as fp:
                page = fp.read()
            soup = BeautifulSoup(page, 'lxml')
            maindiv = soup.find('div', {'class': 'wfb-text-box'})
            titlediv = maindiv.find('div', {'class': 'fbTitleRankOrder'})
            fulltitle = self.cst.fluffinutter(titlediv.text.strip())
            t_parts = fulltitle.split('::')
            title = t_parts[1].strip()
            c2 = c1[title] = {}
            tdesc = maindiv.find('div', {'class': 'rankOrderDesc'})
            if tdesc is None:
                description = ''
            else:
                description = self.cst.fluffinutter(tdesc.text.strip())
            c2['Description'] = description
            c3 = c2['By Country'] = {}
            country_data = maindiv.find('table', {'id': 'fieldListing'})
            country_trs = country_data.find_all('tr')
            for n, tr in enumerate(country_trs):
                if tr is None:
                    break
                if n == 0:
                    continue
                tds = tr.find_all('td')
                data = []
                note = None
                for n1, td in enumerate(tds):
                    if n1 == 0:
                        clink = td.find('a')
                        curl = clink.get('href')[2:]
                        url = f'{baseurl}{curl}'
                        filename = self.get_filename(url)
                        country_name = clink.text.strip()
                        c4 = c3[country_name] = {}
                        c4['URL'] = url
                        c4['Filename'] = os.fspath(filename)
                    elif n1 == 1:
                        txt = td.text.split('\n')
                        for item in txt:
                            if item == '':
                                continue
                            if 'note:' in item:
                                item = item.split(':')
                                note = item[1].strip()
                                continue
                            data.append(item)
                        # print(f'\nnote: {note}, data: {data}')
                        seq = 0
                        c5 = c4['Data'] = {}
                        # print(f'\ncountry: {country_name}\n    data: {data}\n    note: {note}')
                        for item in data:
                            c5[str(seq)] = item
                            seq += 1
                        if note is not None:
                            c5['Note'] = note


if __name__ == '__main__':
    CIA_ExtractComparisons()
