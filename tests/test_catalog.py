"""This module provides unit tests for the internal PROBA-V MEP Python catalog client"""

import datetime
import json
from unittest import TestCase
from catalogclient import catalog


class TestCatalog(TestCase):
    """This class provides unit tests for the internal PROBA-V MEP Python catalog client"""

    def test_init_catalog(self):
        """Tests catalog constructor with default catalog base URL."""

        cat = catalog.Catalog()
        self.assertEqual(cat.baseurl, catalog.CATALOG_BASE_URL)

    def test_init_catalog_2(self):
        """Tests catalog constructor with custom catalog base URL."""

        cat = catalog.Catalog('dummy.be')
        self.assertEqual(cat.baseurl, 'dummy.be')

    def test_geotiff_unmarshalling(self): # pylint: disable=W0212
        """Tests unmarshalling of GeoTIFF products."""

        with open('testresources/probav_geotiff.json', 'r') as json_input:
            dct = json.loads(json_input.read())
            products = catalog.Catalog._build_from_json(dct)
            self.assertEqual(len(products), 2)
            self.assertEqual(products[1].producttype, 'PROBAV_L3_S10_TOC_333M')
            self.assertEqual(products[1].tilex, 0)
            self.assertEqual(products[1].tiley, 1)

    def test_get_product_parameters(self):
        """Tests parameter checks for the get_product method."""

        cat = catalog.Catalog()
        with self.assertRaises(ValueError):
            cat.get_products(None)
        with self.assertRaises(ValueError):
            cat.get_products('PROBAV_L3_S10_TOC_333M', fileformat=None)

    def test_get_products_by_daterange(self):
        """Integration test for retrieval of products by date range."""

        cat = catalog.Catalog()
        products = cat.get_products('PROBAV_L3_S10_TOC_333M', fileformat='HDF5',
                                    startdate=datetime.date(2016, 1, 1),
                                    enddate=datetime.date(2016, 1, 2))
        self.assertGreater(len(products), 0)

    def test_get_products_by_year(self):
        """Integration test for retrieval of products by year."""

        cat = catalog.Catalog()
        products = cat.get_products_for_year('PROBAV_L3_S10_TOC_333M', 2016, fileformat='HDF5')
        self.assertGreater(len(products), 0)
