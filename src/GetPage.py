# copyright (c) 2018  Larz60+
import ScraperPaths
import requests
import os
import time
import sys
import codecs

class GetPage:
    def __init__(self):
        os.chdir(os.path.dirname(__file__))
        self.spath = ScraperPaths.ScraperPaths()
        self.user_agent = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) '
            'Gecko/20100101 Firefox/60.0 AppleWebKit/537.36 (KHTML, '
            'like Gecko)  Chrome/68.0.3440.75 Safari/537.36'}

    def get_filename(self, url, abbr=None):
        # problem with 'https://www.cia.gov/library/publications/resources/the-world-factbook/docs/notesanddefs.html#2028'
        # filename should be modified (last entry in urlpart) to notesanddefs_2028.html
        urlpart = url.split('/')
        name = urlpart[-1]
        if '#' in name:
            name = name.split('.')
            name2 = name[1].split('#')
            urlpart[-1] = f'{name[0]}_{name2[1]}.{name2[0]}'
        filename = self.spath.cia_homepath
        for n in range (3, len(urlpart)):
            filename = filename / urlpart[n]
        return filename

    def get_page(self, url, filename, verbose=False, image=False, encoding='utf-8'):
        htmlpage = None
        if verbose:
            print(f'\nget url: {url}')
        if not filename.exists():
            response = requests.get(url, headers=self.user_agent)
            time.sleep(5)
            if response.status_code == 200:
                if verbose:
                    print('success')
                if len(response.content) > 0:
                    if image:
                        with filename.open('wb') as zp:
                            zp.write(response.content)
                    else:
                        if encoding is None:
                            with filename.open('wb') as zp:
                                zp.write(response.content)
                        else:
                            with filename.open('wb', encoding=encoding) as zp:
                                zp.write(response.content)
                    htmlpage = response.content
                else:
                    print('length is zero')
            else:
                print(f'Problem fetching {url}\n')
        else:
            file_name = filename.resolve()
            with codecs.open(file_name, "r",encoding='utf-8', errors='ignore') as fp:
            # with filename.open() as fp:
                htmlpage = fp.read()
        return htmlpage

def testit():
    os.chdir(os.path.dirname(__file__))
    gp = GetPage()
    url = '/run/media/larz60p/Data-2TB/Scraper/data/CIA/library/publications/resources/cia-maps-publications/Cameroon.html'
    filename = gp.get_filename(url)
    gp.get_page(url, filename)

if __name__ == '__main__':
    testit()
