import re

from setuptools import setup

test_requirements = ['pytest','requests','mock']

with open('catalogclient/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

setup(name='catalogclient',
      version=version,
      author='Dirk Daems',
      author_email='dirk.daems@vito.be',
      description='Catalog client for the internal PROBA-V MEP and Copernicus Global Land catalogs',
      url='https://git.vito.be/projects/BIGGEO/repos/mep-catalogclient',
      packages=['catalogclient'],
      test_suite = 'tests',
      tests_require=test_requirements,
      setup_requires=['pytest-runner'],
      install_requires=['requests','shapely>=1.5.17','python-dateutil'])
