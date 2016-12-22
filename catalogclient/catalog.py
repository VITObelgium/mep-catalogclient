import requests
import urlparse

CATALOG_BASE_URL = 'http://pdfcatalog.vgt.vito.be:8080/develop/catalog/v2/'


class EOProduct(object):

    def __init__(self, producttype=None, tilex=0, tiley=0, files=None):

        self.producttype = producttype
        self.tilex = tilex
        self.tiley = tiley
        self.files = files


class EOProductFile(object):

    def __init__(self, filename, bands):

        self.filename = filename
        self.bands = bands


class Catalog(object):

    def __init__(self, baseurl=CATALOG_BASE_URL):

        self.baseurl = baseurl

    @staticmethod
    def build_from_json(json):

        products = map(lambda a:EOProduct(a['productType'], a['tileX'], a['tileY'],
                                          map(lambda b:EOProductFile(b['filename'], b['bands']), a['files'])),
                       json)

        return products

    def get_products(self, producttype, format='HDF5', startdate=None, enddate=None):

        url = urlparse.urljoin(self.baseurl, producttype)

        params = {
            'format': str(format),
        }

        if startdate != None:
            params['startDate'] = startdate.strftime('%Y%m%d')
        if enddate != None:
            params['endDate'] = enddate.strftime('%Y%m%d')

        response = requests.get(url, params=params)

        return self.build_from_json(response.json())
