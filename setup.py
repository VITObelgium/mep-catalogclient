from setuptools import setup

setup(name='catalogclient',
      version='1.0',
      author='Dirk Daems',
      author_email='dirk.daems@vito.be',
      description='Catalog client for the internal PROBA-V MEP and Copernicus Global Land catalogs',
      url='https://bitbucket.org/vitotap/catalogclient',
      packages=['catalogclient'],
      test_suite = 'tests',
      install_requires=['requests']
      )
