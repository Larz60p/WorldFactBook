# Relative pathlib path list (base path is Scraper/src)
# Includes common files.
#
# Author: Larz60+ (c) 2018
from pathlib import Path
import os
import sys


class ScraperPaths:
    def __init__(self):
        self.homepath = self.get_root_dir(rootnode='src')
        self.rootpath = self.homepath / '..'
        self.basepath = self.homepath / 'BaseFiles'

        # self.virtualbin = self.rootpath / 'venv' /  'bin'
        self.geckopath = Path('/usr/local/bin') / 'geckodriver'
        self.chromepath = Path('/usr/local/bin') / 'chromedriver'

        self.document_path = self.rootpath / 'doc'
        self.document_path.mkdir(exist_ok=True)

        self.datapath = self.rootpath / 'data'
        self.datapath.mkdir(exist_ok=True)

        self.RawDatapath = self.datapath / 'RawData'
        self.RawDatapath.mkdir(exist_ok=True)

        self.codespath = self.RawDatapath / 'Codes'
        self.codespath.mkdir(exist_ok=True)

        self.datalogpath = self.datapath / 'logs'
        self.datalogpath.mkdir(exist_ok=True)

        self.scrapedatapath = self.datapath / 'scrapedata'
        self.scrapedatapath.mkdir(exist_ok=True)

        self.jsonpath = self.scrapedatapath / 'json'
        self.jsonpath.mkdir(exist_ok=True)

        self.htmlpath = self.scrapedatapath / 'html'
        self.htmlpath.mkdir(exist_ok=True)

        self.countryhtmlpath = self.htmlpath / 'Country-Html'
        self.countryhtmlpath.mkdir(exist_ok=True)

        self.sitefilepath = self.htmlpath / 'Site-html'
        self.sitefilepath.mkdir(exist_ok=True)

        self.phonehtmlpath = self.htmlpath / 'PhoneNumbers'
        self.phonehtmlpath.mkdir(exist_ok=True)

        self.image_path = self.scrapedatapath / 'images'
        self.image_path.mkdir(exist_ok=True)

        self.seeddatapath = self.scrapedatapath / 'seeds'
        self.seeddatapath.mkdir(exist_ok=True)

        self.seedlogpath = self.seeddatapath / 'Logfiles'
        self.seedlogpath.mkdir(exist_ok=True)

        self.tmppath = self.datapath / 'tmp'
        self.tmppath.mkdir(exist_ok=True)

        self.seed_extraction_path = self.scrapedatapath / 'seed_extraction'
        self.seed_extraction_path.mkdir(exist_ok=True)

        self.rawdatapath = self.datapath / 'RawData'
        self.rawdatapath.mkdir(exist_ok=True)

        self.codepath = self.rawdatapath / 'Codes'
        self.codepath.mkdir(exist_ok=True)

        self.national_names = self.codepath / 'NationalFileDomesticNames.txt'
        self.national_names_json = self.jsonpath / 'DomesticNames.json'

        self.native_american = self.codepath / 'AIAlist.txt'
        self.native_american_json = self.jsonpath / 'NativeAmericanPlaces.json'

        self.county = self.codepath / 'RawCountyData.txt'
        self.county_json = self.jsonpath / 'County.json'

        self.county_fips_json = self.jsonpath / 'CountyFIPS.json'

        self.county_sub = self.codepath / 'RawCountySub.txt'
        self.county_sub_json = self.jsonpath / 'CountySub.json'

        self.places = self.codepath / 'national_places.txt'
        self.places_json = self.jsonpath / 'Places.json'

        self.newplaces = self.codepath / 'newplace.txt'
        self.newplace_json = self.jsonpath / 'NewPlaces.json'

        self.place_types_json = self.jsonpath / 'PlaceTypes.json'

        self.state_cd = self.codepath / 'national_state_codes.txt'
        self.state_json = self.jsonpath / 'State.json'

        self.school_districts = self.codepath / 'national_schdist.txt'
        self.school_districts_json = self.jsonpath / 'SchoolDistricts.json'

        self.voting_districts = self.codepath / 'national_vtd.txt'
        self.voting_districts_json = self.jsonpath / 'VotingDistricts.json'

        self.congressional_districts = self.codepath / 'national_cd115.csv'
        self.congressional_districts_json = self.jsonpath / 'CongressionalDistricts.json'

        self.places_scraped_json = self.jsonpath / 'PlacesScraped.json'

        self.business_master_json = self.jsonpath / 'BusinessMaster.json'
        self.processed_files_json = self.jsonpath / 'Processed_files.json'

        self.tempfile = self.tmppath / 'tempfile.txt'

        self.millbrook_home_html = self.htmlpath / 'MillbrookHome.html'
        self.millbrook_directory_html = self.htmlpath / 'MillbrookDirectory.html'

        self.phone_urls = self.codespath / 'phone_urls.txt'

        self.cia_homepath = self.datapath / 'CIA'
        self.cia_homepath.mkdir(exist_ok=True)

        self.cia_dup_workarea = self.cia_homepath / 'dup_workarea'
        self.cia_dup_workarea.mkdir(exist_ok=True)

        self.cia_created_files = self.cia_homepath / 'CreatedFiles'
        self.cia_created_files.mkdir(exist_ok=True)

        self.cia_library = self.cia_homepath / 'library'
        self.cia_library.mkdir(exist_ok=True)

        self.cia_l_publications = self.cia_library / 'publications'
        self.cia_l_publications.mkdir(exist_ok=True)

        self.cia_lpr_world_leaders_1 = self.cia_l_publications / 'world-leaders-1'
        self.cia_lpr_world_leaders_1.mkdir(exist_ok=True)

        self.cia_lp_resources = self.cia_l_publications / 'resources'
        self.cia_lp_resources.mkdir(exist_ok=True)

        self.cia_lpr_world_leaders_1 = self.cia_lp_resources / 'world-leaders-1'
        self.cia_lpr_world_leaders_1.mkdir(exist_ok=True)

        self.cia_lpr_cia_map_publications = self.cia_lp_resources / 'cia-maps-publications'
        self.cia_lpr_cia_map_publications.mkdir(exist_ok=True)

        self.cia_lprc_map_thumbs = self.cia_lpr_cia_map_publications / 'map-thumbs'
        self.cia_lprc_map_thumbs.mkdir(exist_ok=True)

        self.cia_lprc_map_downloads = self.cia_lpr_cia_map_publications / 'map-downloads'
        self.cia_lprc_map_downloads.mkdir(exist_ok=True)

        self.cia_lpr_the_world_factbook = self.cia_lp_resources / 'the-world-factbook'
        self.cia_lpr_the_world_factbook.mkdir(exist_ok=True)

        self.cia_lprt_fields = self.cia_lpr_the_world_factbook / 'fields'
        self.cia_lprt_fields.mkdir(exist_ok=True)

        self.cia_lprt_rankorder = self.cia_lpr_the_world_factbook / 'rankorder'
        self.cia_lprt_rankorder.mkdir(exist_ok=True)

        self.cia_lprt_appendix = self.cia_lpr_the_world_factbook / 'appendix'
        self.cia_lprt_appendix.mkdir(exist_ok=True)

        self.cia_lprt_docs = self.cia_lpr_the_world_factbook / 'docs'
        self.cia_lprt_docs.mkdir(exist_ok=True)

        self.cia_lpwg_ref_maps_docs = self.cia_lprt_docs / 'ref_maps'
        self.cia_lpwg_ref_maps_docs.mkdir(exist_ok=True)

        self.cia_lpwg_docs_political = self.cia_lpwg_ref_maps_docs / 'political'
        self.cia_lpwg_docs_political.mkdir(exist_ok=True)

        self.cia_lpwg_docs_political_jpg = self.cia_lpwg_docs_political / 'jpg'
        self.cia_lpwg_docs_political_jpg.mkdir(exist_ok=True)

        self.cia_lpwg_docs_political_pdf = self.cia_lpwg_docs_political / 'pdf'
        self.cia_lpwg_docs_political_pdf.mkdir(exist_ok=True)

        self.cia_lpwg_docs_physical = self.cia_lpwg_ref_maps_docs / 'physical'
        self.cia_lpwg_docs_physical.mkdir(exist_ok=True)

        self.cia_lpwg_docs_physical_jpg = self.cia_lpwg_docs_physical / 'jpg'
        self.cia_lpwg_docs_physical_jpg.mkdir(exist_ok=True)

        self.cia_lpwg_docs_physical_pdf = self.cia_lpwg_docs_physical / 'pdf'
        self.cia_lpwg_docs_physical_pdf.mkdir(exist_ok=True)

        self.cia_graphics = self.cia_lpr_the_world_factbook / 'graphics'
        self.cia_graphics.mkdir(exist_ok=True)

        self.cia_graphics_population = self.cia_graphics / 'population'
        self.cia_graphics_population.mkdir(exist_ok=True)
        
        self.cia_covers = self.cia_graphics / 'covers'
        self.cia_covers.mkdir(exist_ok=True)

        self.cia_covers_thumbs = self.cia_covers / 'thumbnails'
        self.cia_covers_thumbs.mkdir(exist_ok=True)
        
        self.cia_lpwg_ref_maps_graphics = self.cia_graphics / 'ref_maps'
        self.cia_lpwg_ref_maps_graphics.mkdir(exist_ok=True)

        self.cia_lpwg_graphics_political = self.cia_lpwg_ref_maps_graphics / 'political'
        self.cia_lpwg_graphics_political.mkdir(exist_ok=True)

        self.cia_lpwg_graphics_political_jpg = self.cia_lpwg_graphics_political / 'jpg'
        self.cia_lpwg_graphics_political_jpg.mkdir(exist_ok=True)

        self.cia_lpwg_graphics_political_pdf = self.cia_lpwg_graphics_political / 'pdf'
        self.cia_lpwg_graphics_political_pdf.mkdir(exist_ok=True)

        self.cia_lpwg_graphics_physical = self.cia_lpwg_ref_maps_graphics / 'physical'
        self.cia_lpwg_graphics_physical.mkdir(exist_ok=True)

        self.cia_lpwg_graphics_physical_jpg = self.cia_lpwg_graphics_physical / 'jpg'
        self.cia_lpwg_graphics_physical_jpg.mkdir(exist_ok=True)

        self.cia_lpwg_graphics_physical_pdf = self.cia_lpwg_graphics_physical / 'pdf'
        self.cia_lpwg_graphics_physical_pdf.mkdir(exist_ok=True)

        self.cia_flags = self.cia_graphics / 'flags'
        self.cia_flags.mkdir(exist_ok=True)

        self.cia_large_flags = self.cia_flags / 'large'
        self.cia_large_flags.mkdir(exist_ok=True)

        self.cia_lprt_geos = self.cia_lpr_the_world_factbook / 'geos'
        self.cia_lprt_geos.mkdir(exist_ok=True)

        self.cia_json = self.cia_homepath / 'json'
        self.cia_json.mkdir(exist_ok=True)

        self.CIA_country_fact_links_json = self.cia_json / 'CIA_CountryFactLinks.json'

    def get_root_dir(self, rootnode):
        home = Path('.')
        pp = list(Path(os.path.dirname(__file__)).parts)
        if pp[-1] != rootnode:
            pp.pop(-1)
        np = Path('/')
        for n, xp in enumerate(pp):
            if n == 0:
                continue
            np = Path(np).joinpath(xp)
        os.chdir(np.resolve())
        return np

    def display_dict(self, thedict):
        for key, value in thedict.items():
            if isinstance(value, dict):
                print(f'{key}:')
                self.display_dict(value)
            else:
                print(f'    {key}: {value}')


def testit():
    sp = ScraperPaths()
    print(os.getcwd())
    # get contents of directory for test
    print(f'jsonpath: {sp.jsonpath.resolve()}')
    p = sp.jsonpath
    print([x for x in p.iterdir() if x.is_file()])


if __name__ == '__main__':
    testit()
