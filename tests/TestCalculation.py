import pytest
import sys
sys.path.append('../pytest_in_robotframework')
from pytest_in_robotframework import pytest_execute
import time


def calculation(a,operator,b):
    return eval(str(a)+str(operator)+str(b))

class TestCalculation:
    @pytest_execute
    @pytest.mark.parametrize("a,operator,b,result", [(1,"+",1,2),(2,"-", 1,1),(2,"-", 1,1),(4,"/", 2,2),(4,"*", 4,16),(282,"-", 282,0),(3.14,"-",1.57,1.57),(2,"-", 1,1)])
    def test_calculations(self,a,operator,b,result):
        print("vykonal jsem prvni radek test_login_as...")
        time.sleep(0.2)
        assert calculation(a,operator,b) == result
