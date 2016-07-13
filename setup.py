from setuptools import setup, find_packages

setup(name='mist.tests',
      version='1.0',
      description='Tests for mist.core and mist.io',
      long_description='',
      classifiers=["Programming Language :: Python"],
      author='mist.io',
      packages=find_packages('.'),
      package_dir={'': '.'},
      namespace_packages=['tests'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
      )
