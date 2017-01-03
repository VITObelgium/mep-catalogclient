"""This module provides a Python catalog client for the internal PROBA-V MEP
 and Copernicus Global Land catalogs"""

import urlparse
import requests

CATALOG_BASE_URL = 'http://pdfcatalog.vgt.vito.be:8080/develop/catalog/v2/'


class EOProduct(object):
    """This class represents an EO product returned from a catalog search."""

    def __init__(self, producttype=None, tilex=0, tiley=0, files=None):

        self.producttype = producttype
        self.tilex = tilex
        self.tiley = tiley
        self.files = files

    def __str__(self):

        return "{0}_{1}_{2}".format(self.producttype, self.tilex, self.tiley)


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
    def _build_from_json(json):
        """Builds EOProduct objects from a dict."""

        return map(
            lambda a: EOProduct(a['productType'],
                                a['tileX'],
                                a['tileY'],
                                map(lambda b: EOProductFile(b['filename'],
                                                            b['bands']), a['files'])),
            json)

    @staticmethod
    def _check_mandatory(producttype, fileformat):
        """Check mandatory parameters."""

        if producttype is None:
            raise ValueError("producttype is mandatory")
        if fileformat is None:
            raise ValueError("fileformat is mandatory")

    def get_products(self, producttype, fileformat='HDF5', startdate=None, enddate=None,
                     min_lon=-180, max_lon=180, min_lat=-90, max_lat=90):
        """Returns EOProducts for specified product type, file format, region of interest
        and date range."""

        self._check_mandatory(producttype, fileformat)

        url = urlparse.urljoin(self.baseurl, producttype)

        params = {
            'format': str(fileformat),
        }

        if startdate != None:
            params['startDate'] = startdate.strftime('%Y%m%d')
        if enddate != None:
            params['endDate'] = enddate.strftime('%Y%m%d')
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
            return self._build_from_json(response.json())
        else:
            response.raise_for_status()

    def get_products_for_year(self, producttype, year, fileformat='HDF5',
                              min_lon=-180, max_lon=180, min_lat=-90, max_lat=90):
        """Returns EOProducts for specified product type, file format,
        region of interest and year."""

        self._check_mandatory(producttype, fileformat)

        url = urlparse.urljoin(self.baseurl, producttype)

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
            return self._build_from_json(response.json())
        else:
            response.raise_for_status()
