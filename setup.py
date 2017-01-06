from setuptools import setup

test_requirements = ['requests','mock']

setup(name='catalogclient',
      version='0.2',
      author='Dirk Daems',
      author_email='dirk.daems@vito.be',
      description='Catalog client for the internal PROBA-V MEP and Copernicus Global Land catalogs',
      url='https://bitbucket.org/vitotap/catalogclient',
      packages=['catalogclient'],
      test_suite = 'tests',
      tests_require=test_requirements,
      install_requires=['requests']+test_requirements)
