"""This module provides unit tests for the internal PROBA-V MEP Python catalog client"""

import datetime
import json
from unittest import TestCase
from requests.exceptions import HTTPError
from mock import mock
from catalogclient import catalog


def probav_geotiff_response(*args, **kwargs):
    with open('testresources/probav_geotiff.json', 'r') as json_input:
        dct = json.loads(json_input.read())
        return MockedResponse(200, dct)

def producttypes_response(*args, **kwargs):
    with open('testresources/producttypes.json', 'r') as json_input:
        dct = json.loads(json_input.read())
        return MockedResponse(200, dct)

def times_response(*args, **kwargs):
    with open('testresources/times.json', 'r') as json_input:
        dct = json.loads(json_input.read())
        return MockedResponse(200, dct)

def error_response(*args, **kwargs):
    return MockedResponse(500, None)


class MockedResponse(object):
    """This class represents a mocked requests.Response object"""

    def __init__(self, status_code, json_data):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        raise HTTPError()


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

        with open('../testresources/probav_geotiff.json', 'r') as json_input:
            dct = json.loads(json_input.read())
            products = catalog.Catalog._build_products(dct)
            self.assertEqual(len(products), 2)
            self.assertEqual(products[1].producttype, 'PROBAV_L3_S10_TOC_333M')
            self.assertEqual(products[1].tilex, 0)
            self.assertEqual(products[1].tiley, 1)
            self.assertEqual(products[1].files[0].filename, "file:/data/MTDA/TIFFDERIVED/PROBAV_L3_S10_TOC_333M/20160101/PROBAV_S10_TOC_20160101_333M_V001/PROBAV_S10_TOC_X00Y01_20160101_333M_V001_SM.tif")
            self.assertEqual(products[1].bands(), ['PROBAV:SM',
                                                   'PROBAV:NIR/TOC',
                                                   'PROBAV:SWIR/TOC',
                                                   'PROBAV:RED/TOC',
                                                   'PROBAV:BLUE/TOC',
                                                   'PROBAV:TIME',
                                                   'PROBAV:NDVI',
                                                   'PROBAV:SAA',
                                                   'PROBAV:VNIR/VAA',
                                                   'PROBAV:SZA',
                                                   'PROBAV:SWIR/VAA',
                                                   'PROBAV:SWIR/VZA',
                                                   'PROBAV:VNIR/VZA'])

            self.assertEqual(products[1].file("PROBAV:SZA"), "file:/data/MTDA/TIFFDERIVED/PROBAV_L3_S10_TOC_333M/20160101/PROBAV_S10_TOC_20160101_333M_V001/PROBAV_S10_TOC_X00Y01_20160101_333M_V001_GEOMETRY.tif")
            try:
                products[1].file("blabla")
                self.fail("Method should have thrown an exception.")
            except RuntimeError as e:
                pass




    def test_get_product_parameters(self):
        """Tests parameter checks for the get_product method."""

        cat = catalog.Catalog()
        with self.assertRaises(ValueError):
            cat.get_products(None)
        with self.assertRaises(ValueError):
            cat.get_products('PROBAV_L3_S10_TOC_333M', fileformat=None)

    @mock.patch('requests.get', side_effect=producttypes_response)
    def test_get_producttypes(self, mock_get):
        """Unit test for retrieval of producttypes."""

        cat = catalog.Catalog()
        producttypes = cat.get_producttypes()
        self.assertEquals(len(producttypes), 49)

    @mock.patch('requests.get', side_effect=probav_geotiff_response)
    def test_get_products_by_daterange(self, mock_get):
        """Unit test for retrieval of products by date range."""

        cat = catalog.Catalog()
        products = cat.get_products('PROBAV_L3_S10_TOC_333M', fileformat='GEOTIFF',
                                    startdate=datetime.date(2016, 1, 1),
                                    enddate=datetime.date(2016, 1, 2))
        self.assertEquals(len(products), 2)

        self.assertEquals(products[0].geometry.geom_type, 'Polygon')
        self.assertEquals(products[0].geometry.exterior.coords[0], (0.0, 65.0))
        self.assertEquals(products[0].geometry.exterior.coords[1], (0.0, 55.0))
        self.assertEquals(products[0].geometry.exterior.coords[2], (10.0, 55.0))
        self.assertEquals(products[0].geometry.exterior.coords[3], (10.0, 65.0))
        self.assertEquals(products[0].geometry.exterior.coords[4], (0.0, 65.0))

        self.assertIsNone(products[1].geometry)

    @mock.patch('requests.get', side_effect=times_response)
    def test_get_times(self, mock_get):
        """Unit test for retrieval of times for a producttype."""

        cat = catalog.Catalog()
        times = cat.get_times('PROBAV_L3_S10_TOC_333M')
        self.assertEquals(len(times), 116)

    @mock.patch('requests.get', side_effect=error_response)
    def test_get_producttypes_error(self, mock_get):
        """Unit test to test error handling behaviour for retrieval of producttypes."""

        with self.assertRaises(HTTPError):
            cat = catalog.Catalog()
            cat.get_producttypes()

    @mock.patch('requests.get', side_effect=error_response)
    def test_get_products_error(self, mock_get):
        """Unit test to test error handling behaviour for retrieval of products."""

        with self.assertRaises(HTTPError):
            cat = catalog.Catalog()
            cat.get_products('PROBAV_L3_S10_TOC_333M', fileformat='GEOTIFF',
                             startdate=datetime.date(2016, 1, 1),
                             enddate=datetime.date(2016, 1, 2))

    @mock.patch('requests.get', side_effect=error_response)
    def test_get_times_error(self, mock_get):
        """Unit test to test error handling behaviour for retrieval of times."""

        with self.assertRaises(HTTPError):
            cat = catalog.Catalog()
            cat.get_times('PROBAV_L3_S10_TOC_333M')
