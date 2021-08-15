import os
from setuptools import setup

REQS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        'requirements.txt')
with open(REQS_DIR) as reqs:
    REQUIRES = [l.strip() for l in [l for l in reqs if not l.startswith('#')]]

setup(name='misttests',
      version='1.0',
      description='Tests for Mist, the open-source multicloud management platform',
      long_description='',
      classifiers=["Programming Language :: Python"],
      author='mist.io',
      packages=['misttests'],
      include_package_data=True,
      zip_safe=False,
      install_requires=REQUIRES
      )
