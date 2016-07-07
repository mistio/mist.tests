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

In order to run the following examples you should be inside the /mist.core directory of the fullstack container.

In order to run the api tests you should run a command like this:
/core.env/bin/py.test -s tests/api/core/machine_test.py

In order to run the gui tests you should run something like this:
/core.env/bin/behave -k --stop --tags=clouds tests/gui/core/pr/features

The -k flag will not show the features of tests that will not be executed and the --stop flag will stop
the execution if one scenario fails
 
### Test configuration

Both api tests and gui tests are using a lot of configuration variables to get for example credentials.
All these variables are located in the config.py file in the home folder of the tests. There are three ways
to override the default values:
1. Create a test_settings.py file in the mist.core directory and set the values that you want.
2. Export a variable with the name that you want to override and set the new value. The value must be in json
and the tests will pick it up when starting.
3. Finally you can use the prepare_env.py script to dynamically override whatever value you want from the 
command line. One example is the following:
/core.env/bin/ipython tests/prepare_env.py -- --gui --email bla@mist.io --tags=clouds -k --stop tests/gui/core/pr/features
As you can see the last part is the command that you would run to just execute the gui tests. If you want to 
run the api tests just replace the --gui flag with the --api flag. If no flag is submitted then the --gui is
assumed. The --email value will replace the value of EMAIL variable. If we provide for example the 
--webdriver-log /var/log/js_console.log value then the WEBDRIVER_LOG variable from config.py will be updated

The value of a variable is set always overriden by the prepare_env.py script. If the script is not involved
the environment is checked and if nothing is found then the code will check if there is a test_settings.py
module. Finally, if still nothing is found the default value will be used.

...
