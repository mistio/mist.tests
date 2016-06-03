## About
mist.tests is where the testing suite for the Mist.io code resides. Two types of tests are being performed:

- API tests, that use py.test
- and GUI tests that use behave and selenium

### Installation

No installation is required. mist.tests should already be in your core's tests/ directory. If it is not, run git submodule init && git submodule update

### Setting up the environment

TODO

### Running the tests

##### Buildout

Assuming you already have a core installation up and running, to run a specific API test suite, e.g. the machine tests, you need to run

./bin/py.test tests/api/core/machine_test.py

while for a GUI tests suite you should do

./bin/behave -k tests/gui/core/pr/features/

and if you want to run a specific suite, you can specify it using tags

./bin/behave -k --tags=machines tests/gui/core/pr/features/

##### Docker

...
