import pytest
from robot.libraries.BuiltIn import BuiltIn
import pytest_is_running 
import decorator
from robot.api import logger

def  frameworks_info():
        if BuiltIn.robot_running:
            print("RobotFramework is Running")
        else: 
            print("RobotFramework is not Running")

        if pytest_is_running.is_running():
            print("Pytest is Running")
        else: 
            print("Pytest is not Running")
            
#Decorator Definition 
def pytest_execute(function):
    def wrapper(function,*args, **kwargs):
        print('Execution of @pytest_execute wrapper')
        frameworks_info()
        if not pytest_is_running.is_running(): 
            function_name = str(function.__name__)
            function_qualname = str(function.__qualname__).replace('.','::')
            path_to_module = sys.modules[function.__module__].__file__
            parameter = "::".join([path_to_module,function_qualname])
            print("pytest execution parameter is: '" + parameter + "'")
            output = pytest.main(["--verbose",parameter])
            error_codes=['OK - Tests Passed',
                         'TESTS_FAILED',
                         'INTERRUPTED - pytest was interrupted',
                         'INTERNAL_ERROR - An internal error got in the way',
                         'USAGE_ERROR - pytest was misused',
                         'NO_TESTS_COLLECTED - pytest couldn’t find tests']
            if output == 0:
                logger.info("Pytest test '" + function_name + "' succesfully passed " + str(output) + ' = ' + error_codes[output])
            else:
                logger.error("Pytest test '" + function_name + "' failed with error " + str(output) + ' = ' + error_codes[output])
                raise  Exception("Pytest test '" + function_name + "' failed with error " + str(output) + ' = ' + error_codes[output])
        else: 
            return function(*args, **kwargs)
    return decorator.decorator(wrapper, function)