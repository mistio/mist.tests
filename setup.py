import os
from setuptools import setup, find_packages

REQS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        'requirements.txt')
with open(REQS_DIR) as reqs:
    REQUIRES = map(lambda l: l.strip(),
                   filter(lambda l: not l.startswith('#'), reqs))

setup(name='tests',
      version='1.0',
      description='Tests for mist.core and mist.io',
      long_description='',
      classifiers=["Programming Language :: Python"],
      author='mist.io',
      packages=find_packages('.'),
      package_dir={'': '.'},
      include_package_data=True,
      zip_safe=False,
      install_requires=REQUIRES
      )
