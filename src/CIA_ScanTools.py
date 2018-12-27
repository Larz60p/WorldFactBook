# copyright (c) 2018  Larz60+
import string
import ScraperPaths
import io
import json
from collections import MutableMapping
from contextlib import suppress


class CIA_Scan_Tools:
    def __init__(self, dictionary=None, keys=None, seed=None, precision=6):
        self.spath = ScraperPaths.ScraperPaths()
        self.fact_links = {}
        self.load_fact_links()
        self.AutoId = AutoId(seed=None, precision=6)
        self.DeleteDictKeys = DeleteDictKeys()

    def load_fact_links(self):
        if self.spath.CIA_country_fact_links_json.exists():
            with self.spath.CIA_country_fact_links_json.open() as jsp:
                self.fact_links = json.load(jsp)

    def save_fact_links(self):
        with self.spath.CIA_country_fact_links_json.open('w') as jsp:
            json.dump(self.fact_links, jsp)

    def display_dict(self, thedict):
        for key, value in thedict.items():
            if isinstance(value, dict):
                print(f'{key}:')
                self.display_dict(value)
            else:
                print(f'    {key}: {value}')

    def display_list(self, thelist):
        print()
        for item in thelist:
            print(item)

    def fast_iter(self, context, func, *args, **kwargs):
        """
        fast_iter is useful if you need to free memory while iterating through a
        very large XML file.

        http://lxml.de/parsing.html#modifying-the-tree
        Based on Liza Daly's fast_iter
        http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
        See also http://effbot.org/zone/element-iterparse.htm
        """
        for event, elem in context:
            func(elem, *args, **kwargs)
            # It's safe to call clear() here because no descendants will be
            # accessed
            elem.clear()
            # Also eliminate now-empty references from the root node to elem
            for ancestor in elem.xpath('ancestor-or-self::*'):
                while ancestor.getprevious() is not None:
                    del ancestor.getparent()[0]
        del context

    def process_element(self, elt):
        print(elt.text)

    def remove_tags(self, item):
        intag = False
        oitem = ''
        for c in item:
            if c == '>':
                intag = False
                continue
            if c == '<':
                intag = True
            if intag:
                continue
            oitem += c
        return oitem

    def fluffinutter(self, text):
        newtext = ''
        intrum = text.split('\n')
        for n, item in enumerate(intrum):
            item = item.strip()
            item = item.replace('&#160;', '')
            item = item.replace('\u00a0', ' ')
            item = item.replace('\u00e0', 'à')
            if '<' in item:
                item = self.remove_tags(item)
            newtext = f'{newtext.strip()} {item.strip()}'
        return newtext
    
    def prettify(self, soup, indent):
        pretty_soup = str()
        previous_indent = 0
        for line in soup.prettify().split("\n"):
            current_indent = str(line).find("<")
            if current_indent == -1 or current_indent > previous_indent + 2:
                current_indent = previous_indent + 1
            previous_indent = current_indent
            pretty_soup += self.write_new_line(line, current_indent, indent)
        return pretty_soup

    def write_new_line(self, line, current_indent, desired_indent):
        new_line = ""
        spaces_to_add = (current_indent * desired_indent) - current_indent
        if spaces_to_add > 0:
            for i in range(spaces_to_add):
                new_line += " "		
        new_line += str(line) + "\n"
        return new_line

class AutoId:
    def __init__(self, seed=None, precision=6):
        self.seed = 1
        self.precision = precision
        if seed:
            self.seed = seed

    def next(self):
        self.seed += 1
        # number:02d
        return f'lz{self.seed - 1:0{self.precision}}'

    def no_increment(self):
        return f'lz{self.seed - 1:0{self.precision}}'


class DeleteDictKeys:
    def __init__(self):
        pass


    def delete_keys_from_dict(self, dictionary, keys):
        for key in keys:
            with suppress(KeyError):
                del dictionary[key]
        for value in dictionary.values():
            if isinstance(value, MutableMapping):
                self.delete_keys_from_dict(value, keys)


if __name__ == '__main__':
    CIA_Scan_Tools()
