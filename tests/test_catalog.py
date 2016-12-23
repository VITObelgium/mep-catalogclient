import datetime
import json
from unittest import TestCase
from catalogclient import catalog


class TestCatalog(TestCase):

    def test_InitCatalog(self):

        cat = catalog.Catalog()
        self.assertEqual(cat.baseurl, catalog.CATALOG_BASE_URL)

    def test_InitCatalog2(self):

        cat = catalog.Catalog('dummy.be')
        self.assertEqual(cat.baseurl, 'dummy.be')

    def test_ProbaVGeoTiffUnMarshalling(self):

        with open('testresources/probav_geotiff.json', 'r') as json_input:
            dct = json.loads(json_input.read())
            products = catalog.Catalog._build_from_json(dct)
            self.assertEqual(len(products), 2)
            self.assertEqual(products[1].producttype, 'PROBAV_L3_S10_TOC_333M')
            self.assertEqual(products[1].tilex, 0)
            self.assertEqual(products[1].tiley, 1)

    def test_MandatoryParameters(self):

        cat = catalog.Catalog()
        with self.assertRaises(ValueError):
            cat.get_products(None)
        with self.assertRaises(ValueError):
            cat.get_products('PROBAV_L3_S10_TOC_333M', fileformat=None)

    def test_GetProductsByDateRange(self):

        cat = catalog.Catalog()
        products = cat.get_products('PROBAV_L3_S10_TOC_333M', fileformat='HDF5',
                         startdate=datetime.date(2016, 1, 1), enddate=datetime.date(2016, 1, 2))
        self.assertGreater(len(products), 0)

    def test_GetProductsByYear(self):

        cat = catalog.Catalog()
        products = cat.get_products_for_year('PROBAV_L3_S10_TOC_333M', 2016, fileformat='HDF5')
        self.assertGreater(len(products), 0)
