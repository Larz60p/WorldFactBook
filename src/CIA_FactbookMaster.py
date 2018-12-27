# copyright (c) 2018  Larz60+
import ScraperPaths
import CIA_Abbreviations
import CIA_CountryComparisons
import CIA_CountryDetail
import CIA_CountryProfiles
import CIA_Definitions
import CIA_EnvironmentalAgreements
import CIA_ExtractComparisons
import CIA_Faqs
import CIA_FlagsOfTheWorld
import CIA_Gallery
import CIA_History
import CIA_InternationalOrgnizationsAndGroups
import CIA_RefMaps
import CIA_UsersGuide
import CIA_WeightsAndMeasures
import CIA_XrefCountryCodes
import CIA_XrefGeographicNames
import CIA_XrefHydrographicDataCodes
import os


class CIA_FactbookMaster:
    def __init__(self):
        os.chdir(os.path.dirname(__file__))
        self.spath = ScraperPaths.ScraperPaths()
        self.create_CIA_abbreviations()
        self.create_CIA_country_comparisons()
        self.create_CIA_country_detail()
        self.create_CIA_country_profiles()
        self.create_CIA_definitions()
        self.create_CIA_environmental_agreements()
        self.create_CIA_extract_comparisons()
        self.create_CIA_faqs()
        self.create_CIA_flags_of_the_world()
        self.create_CIA_gallery()
        self.create_CIA_history()
        self.create_CIA_international_orgnizations_and_groups()
        self.create_CIA_ref_maps
        self.create_CIA_users_guide()
        self.create_CIA_weights_and_measures()
        self.create_CIA_xref_country_codes()
        self.create_CIA_xref_geographic_names()
        self.create_CIA_xref_hydrographic_data_codes()

    def create_CIA_abbreviations(self):
        print(f'\nCIA_abbreviations')
        CIA_Abbreviations.CIA_Abbreviations()

    def create_CIA_country_comparisons(self):
        print('\nCIA_country_comparisons')
        CIA_CountryComparisons.CIA_CountryComparisons()

    def create_CIA_country_detail(self):
        print('\nCIA_country_detail')
        CIA_CountryDetail.CIA_CountryDetail()

    def create_CIA_country_profiles(self):
        print('\nCIA_country_profiles')
        CIA_CountryProfiles.CIA_CountryProfiles()

    def create_CIA_definitions(self):
        print('\nCIA_definitions')
        CIA_Definitions.CIA_Definitions()

    def create_CIA_environmental_agreements(self):
        print('\nCIA_environmental_agreements')
        CIA_EnvironmentalAgreements.CIA_EnvironmentalAgreements()

    def create_CIA_extract_comparisons(self):
        print('\nCIA_extract_comparisons')
        CIA_ExtractComparisons.CIA_ExtractComparisons()

    def create_CIA_faqs(self):
        print('\nCIA_faqs')
        CIA_Faqs.CIA_Faqs()

    def create_CIA_flags_of_the_world(self):
        print('CIA_flags_of_the_world')
        CIA_FlagsOfTheWorld.CIA_FlagsOfTheWorld()

    def create_CIA_gallery(self):
        print('\nCIA_gallery')
        CIA_Gallery.CIA_Gallery()

    def create_CIA_history(self):
        print('\nCIA_history')
        CIA_History.CIA_History()

    def create_CIA_international_orgnizations_and_groups(self):
        print('\nCIA_InternationalOrgnizationsAndGroups')
        CIA_InternationalOrgnizationsAndGroups.CIA_InternationalOrgnizationsAndGroups()

    def create_CIA_ref_maps(self):
        print('\nCIA_ref_maps')
        CIA_RefMaps.CIA_RefMaps()
        
    def create_CIA_users_guide(self):
        print('\nCIA_users_guide')
        CIA_UsersGuide.CIA_UsersGuide()
    
    def create_CIA_weights_and_measures(self):
        print('\nCIA_weights_and_measures')
        CIA_WeightsAndMeasures.CIA_WeightsAndMeasures()

    def create_CIA_xref_country_codes(self):
        print('\nCIA_xref_country_codes')
        CIA_XrefCountryCodes.CIA_XrefCountryCodes()

    def create_CIA_xref_geographic_names(self):
        print('\nCIA_geographic_names')
        CIA_XrefGeographicNames.CIA_XrefGeographicNames()

    def create_CIA_xref_hydrographic_data_codes(self):
        print('\nCIA_xref_hydrographic_data_codes')
        CIA_XrefHydrographicDataCodes.CIA_XrefHydrographicDataCodes()

if __name__ == '__main__':
    CIA_FactbookMaster()
