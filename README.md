## About
mist.tests is where the testing suite for the Mist.io code resides. Two types of tests are being performed:

- API tests, that use py.test
- and GUI tests that use behave and selenium

### Installation

No installation is required. mist.tests should already be under mist.io/tests/ directory. If it is not, run git submodule init && git submodule update

##### Buildout

In order to create the image that is used for tests, you need to run under the tests directory:

docker build -t mistio/tests_base .

##### Running Tests

To enter the tests container run the following command:

docker run -p 5900:5900 -it mistio/tests_base container/start_test_env.sh

You can run tests either by using Vault for obtaining sensitive data, such as cloud credentials, or by setting a test_settings.py file under tests directory.

To run tests using Vault export your Vault server's IP address as VAULT_ADDR and then run:

./run_tests.sh -api

and you will be prompted to type your Vault username and password. The above command will run the entire API tests suite.
You can run the entire API tests suite or GUI tests suite, or specify the tests you want to run.

If you want a specific suite of API tests, then you should run:

./run_tests.sh -api clouds

In order to run a suite of the gui tests you should run:

./run_tests.sh -gui machines

Run ./run_tests -h for more info.

Usage of Vault is not necessary. You can insert a test_settings.py file under tests directory, and set VAULT_ENABLED variable to True.

All the variables needed for the tests will be obtained from test_settings.py in this case.

To run tests without Vault usage flag '-t' is needed:

./run_tests -t -api



You can always run tests by invoking py.test or behave. For example, for running machines API tests you need to run:

pytest tests/api/io/machines.py

while for a GUI tests suite you should do

behave -k tests/gui/core/pr/features/

and if you want to run a specific suite, you can specify it using tags

behave -k --tags=machines tests/gui/core/pr/features/