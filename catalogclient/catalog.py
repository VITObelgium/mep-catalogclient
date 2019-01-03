"""This module provides a Python catalog client for the internal PROBA-V MEP
 and Copernicus Global Land catalogs"""

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
from datetime import datetime as dt
from datetime import timezone
from dateutil import parser
import requests
from shapely.geometry import shape

CATALOG_BASE_URL = 'https://proba-v-mep.esa.int/api/catalog/v2/'


class EOProduct(object):
    """This class represents an EO product returned from a catalog search."""

    def __init__(self, producttype=None, tilex=0, tiley=0, files=None, geometry=None,
                 timestamp=None):

        self.producttype = producttype
        self.tilex = tilex
        self.tiley = tiley
        self.files = files
        self.geometry = geometry
        self._timestamp = timestamp

    @property
    def timestamp(self):
        """
        The timestamp corresponding to this EO Product
        :return: A datetime object
        """
        return self._timestamp

    def bands(self):
        """
        Retrieves all available band names in this product.
        :return: A list of bands.
        """
        bands = []
        for file in self.files:
            bands.extend(file.bands)
        return bands

    def file(self,band):
        """
        Returns the filename for a given products band.

        :param band: A valid band name.
        :return: A filename, as a string.
        """
        for file in self.files:
            if band in file.bands:
                return file.filename
        raise RuntimeError("Band not found in this product: " + band + ", available bands: " +str(self.bands()))

    def __str__(self):

        return "{0}_{1}_{2}_{3}".format(self.producttype, self.tilex, self.tiley,
                                        self.timestamp)


class EOProductFile(object):
    """This class represents an EO product file returned from a catalog search."""

    def __init__(self, filename, bands):

        self.filename = filename
        self.bands = bands

    def __str__(self):

        return self.filename


class Catalog(object):
    """This class allows searching the catalog."""

    def __init__(self, baseurl=CATALOG_BASE_URL):

        self.baseurl = baseurl


    @staticmethod
    def _build_products(json):
        """Builds EOProduct objects from a dict."""

        return list(map(
            lambda a: EOProduct(a['productType'],
                                a['tileX'],
                                a['tileY'],
                                list(map(lambda b: EOProductFile(b['filename'],
                                                            b['bands']), a['files'])),
                                shape(a['geometry']) if 'geometry' in a else None,
                                dt.strptime(a['timestamp'],
                                            '%Y-%m-%dT%H:%M:%SZ') if 'timestamp' in a else None),
            json))

    @staticmethod
    def _build_times(json):
        """Builds datetime objects from a dict."""

        return list(map(
            lambda a: dt.strptime(a, '%Y-%m-%dT%H:%M:%SZ'), json))


    def get_producttypes(self):
        """Returns the list of available product types."""

        headers = {'Accept': 'application/json'}
        response = requests.get(self.baseurl, headers=headers)
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            response.raise_for_status()


    def get_products(self, producttype, fileformat='HDF5', startdate=None, enddate=None,
                     min_lon=-180, max_lon=180, min_lat=-90, max_lat=90):
        """Returns EOProducts for specified product type, file format, region of interest
        and date range."""

        if producttype is None:
            raise ValueError("producttype is mandatory")
        if fileformat is None:
            raise ValueError("fileformat is mandatory")

        url = urljoin(self.baseurl, producttype)

        params = {
            'format': str(fileformat),
        }

        if startdate != None:
            params['startDate'] = Catalog.convert_date(startdate).strftime('%Y%m%d')
        if enddate != None:
            params['endDate'] = Catalog.convert_date(enddate).strftime('%Y%m%d')
        if min_lon != None:
            params['minLon'] = min_lon
        if max_lon != None:
            params['maxLon'] = max_lon
        if min_lat != None:
            params['minLat'] = min_lat
        if max_lat != None:
            params['maxLat'] = max_lat

        response = requests.get(url, params=params)
        if response.status_code == requests.codes.ok:
            return self._build_products(response.json())
        else:
            response.raise_for_status()

    def get_products_for_year(self, producttype, year, fileformat='HDF5',
                              min_lon=-180, max_lon=180, min_lat=-90, max_lat=90):
        """Returns EOProducts for specified product type, file format,
        region of interest and year."""

        if producttype is None:
            raise ValueError("producttype is mandatory")
        if fileformat is None:
            raise ValueError("fileformat is mandatory")

        url = urljoin(self.baseurl, producttype)

        params = {
            'format': str(fileformat),
            'year': str(year)
        }

        if min_lon != None:
            params['minLon'] = min_lon
        if max_lon != None:
            params['maxLon'] = max_lon
        if min_lat != None:
            params['minLat'] = min_lat
        if max_lat != None:
            params['maxLat'] = max_lat

        response = requests.get(url, params=params)
        if response.status_code == requests.codes.ok:
            return self._build_products(response.json())
        else:
            response.raise_for_status()

    @classmethod
    def convert_date(cls, date):
        if type(date) is str:
            return parser.parse(date).replace(tzinfo=timezone.utc)
        return date

    def get_times(self, producttype):
        """Returns a list of dates at which a product is available in the catalog."""

        if producttype is None:
            raise ValueError("producttype is mandatory")

        url = urljoin(self.baseurl, producttype + '/times')

        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            return self._build_times(response.json())
        else:
            response.raise_for_status()
