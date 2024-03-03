import pytest
from robot.libraries.BuiltIn import BuiltIn
import pytest_is_running 
import decorator
import sys
from robot.api import logger
import logging

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
            output = pytest.main(["--verbose",parameter], plugins=[pytest_rflog_plugin()])
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



#Interesting note to API3
#The main benefit of using the listener API is that modifications can be done dynamically based on execution results or otherwise. 
#This allows, for example, interesting possibilities for model based testing.

# for pytest import as plugin 
# It use hooks for pytest https://docs.pytest.org/en/8.0.x/reference/reference.html#id56
# https://docs.pytest.org/en/8.0.x/reference/reference.html#test-running-runtest-hooks
# intro to pytetst hooks https://pytest-with-eric.com/hooks/pytest-hooks/

#for importing to Roboto FGRamework use 
#https://robot-framework.readthedocs.io/en/master/autodoc/robot.result.html#robot.result.resultbuilder.ExecutionResult
# or listener

#use external listener - http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#taking-listeners-into-use

# RF - adding keywords

class Log_Writer_Via_RFListener:
    ROBOT_LIBRARY_SCOPE = 'SUITE'
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self

    # when is loaded this library test is probably already started 
    #maybe this whole section shoudl be callecd from decorator?
    #def start_test(data, result):
    #    data.body.create_keyword(name='Log', args=['Keyword added by listener!'])
       
    def _start_keyword(self, data, result):
        a = data.body.create_keyword(name='Pytest Setup (_start_keyword)', args=['Keyword added by listener!'])
        b = data.body.create_keyword(name='Pytest Test (_start_keyword)', args=['Keyword added by listener!'])
        c = data.body.create_keyword(name='Pytest Teardown (_start_keyword)', args=['Keyword added by listener!'])
        logging.info('Created keyword object has these methods and atributes: ' + str(dir(a))) 

    def _end_keyword(self, data, result):
        # write all data from keyword to the logs
        #running model in data https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.html#robot.running.model.Keyword
        #result model in result https://robot-framework.readthedocs.io/en/master/autodoc/robot.result.html#robot.result.model.Keyword.body
        a = data.body.create_keyword(name='Pytest Setup (_end_keyword)', args=['Keyword added by listener!'])
        b = data.body.create_keyword(name='Pytest Test (_end_keyword)', args=['Keyword added by listener!'])
        c = data.body.create_keyword(name='Pytest Teardown (_end_keyword)', args=['Keyword added by listener!'])
        logging.info('Created keyword object has these methods and atributes: ' + str(dir(a)))

class Log_Collector_From_Pytest:
    logs = []
    def __init__(self):
        self.logs.append({'level':'info', 'message':'start collecting logs from pytest','timestamp':''})

    def collect_log(self,level,message):
        print('DEBUG ' + level + ' ' + message) # DEBUG LINE
        self.logs.append({'level': level, 'message':message,'timestamp':''})

    def log_all_to_rf(self):
        for log in self.logs:
            log = {'level':'level', 'message': 'message','timestamp':''}
            if log['level'] == 'info':

                logging.info(log['message'])
            else:
                logging.info(log['message'])

class pytest_rflog_plugin:
    #@pytest.hookimpl()
    def pytest_runtest_logfinish(nodeid, location):
        print('my pytest_runtest_logfinish')
        #fixture can be resolved in hooks directly https://stackoverflow.com/questions/55413277/can-pytest-hooks-use-fixtures
        logging.info('start pytets hook pytest_runtest_logfinish')
        RFLogger = Log_Collector_From_Pytest()
        RFLogger.collect_log('info','start pytets hook pytest_runtest_logfinish')
        #feature_request = nodeid.funcargs["request"]
        #caplog = feature_request.getfixturevalue("caplog")
        #for record in caplog.records:
             #log record docu https://docs.python.org/3/library/logging.html#logging.LogRecord
        #    RFLogger.collect_log('info', 'time: ' + record.asctime + '; ' + record.levelname + ' ' + record.message)
        #RFLogger.log_all_to_rf()
        #caplog.clear()