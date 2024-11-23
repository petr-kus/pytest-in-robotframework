# pytest-in-robotframework
*pytest-in-robotframework* enables the running of pytest within the Robot Framework, allowing users to leverage the advantages of both frameworks.

To achieve this integration, simply add the decorator '\@pytest_execute' above all the pytest fixtures within your Python tests/keywords in python libraries.

The test with the '\@pytest_execute' decorator will be executed within the pytest framework in the background. All the functionalities of the pytest framework should work normally, including fixture resolution, parametrization, etc. The final result from pytest will be passed on to the Robot Framework. If the specified keyword in the Robot Framework suite/test case fails, it will be logged as a failure in the Robot Framework results, along with the pytest console output as an info-message.    

At present, this code serves as a proof of concept but is already fully usable in production.

It works with both, functions and methods, as long as they follow the naming conventions required by pytest (start or end with 'test').
The classes have to folow the naming convention of pytest (start with 'Test'). 

The decorator '\@pytest_execute' should not compromise any pytest functionality. This means that original pytest tests, where this decorator is added in the Python file and executed via pytest, should continue to function as intended.

However, to utilize this feature, it is anticipated that the test will be primarily executed by Robot Framework, with only a few keywords executed by Pytest under the hood. Additionally, this feature might serve as a step-by-step tool for transitioning tests between Robot Framework and Pytest.    

## Installation and Usage
Command line installation:
```bash
pip install pytest-in-robotframework
```
Import and usage:
```python
from pytest_in_robotframework import pytest_execute

#usage with functions
@pytest_execute
def test_my_function():
    assert  False

def rf_keyword_2():
        print('Passed')

#usage with methods 
class TestMyWorld: 

    @pytest_execute
    def test_my_method(self):
        assert  True

    def rf_keyword_1(self):
        print('Passed')
```
## Real Example
Robot Framework file:
```robotframework
#The Example of usage  - suite_name.robot file

*** Settings ***
Documentation     Proof of Concept integration pytest under the hood of Robot Framework
Library  TestExperiment.py


*** Test Cases ***
Login User with Password
    Open Web Page  https://www.saucedemo.com/ #executed by RF
    Test Login As  user  password  #executed by Pytest under the hood

    #user and password is there only for Robot Framework checks (is not used)
```

Python File: 
```python
#The Example of usage  - TestExperiment.py file
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#import of this solution
from pytest_in_robotframework import pytest_execute 

class TestExperiment:
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    #executed by RF (becouse no @pytest_execute)
    def open_web_page(self,page): 
        self.driver.get(page)

    #executed by Pytest (becouse @pytest_execute decorator)
    @pytest_execute
    #@pytest.mark.parametrize("user,password", [("standard_user", "secret_sauce"),("locked_out_user", "secret_sauce"),("problem_user", "secret_sauce")]) #failing example
    @pytest.mark.parametrize("user,password", [("standard_user", "secret_sauce"),("problem_user", "secret_sauce")]) #passing example
    def test_login_as(self,user,password):
        print("vykonal jsem prvni radek test_login_as...")
        time.sleep(1)
        username = self.driver.find_element(By.ID,'user-name')
        username.clear()
        username.send_keys(user)
        my_password = self.driver.find_element(By.ID,'password')
        my_password.clear()
        my_password.send_keys(password)
        time.sleep(1)
        login_button = self.driver.find_element(By.ID, 'login-button')
        login_button.click()
        print(__name__)
        time.sleep(1)
        button = self.driver.find_element(By.ID, 'react-burger-menu-btn')
        button.click()
        time.sleep(1)
        button = self.driver.find_element(By.ID, 'logout_sidebar_link')
        button.click()
        time.sleep(1)
```

The real example demonstrates the benefits of using a single Python instance. The instances of the TestExperiment class have one driver instance for both the Robot Framework and Pytest engines. Additionally, Pytest parametrization can be utilized, which is a significant advantage compared to Robot Framework. In Robot Framework, it is possible to use Test Templates, but the process is not as straightforward as with Pytest for small combinatoric tests (closer to property testing).

Sometimes Pytest is the appropriate choice, while at other times Robot Framework may be better suited. Now, you can seamlessly integrate both into a single Python instance with identical logging, minimal effort, and compatibility.

## Future planed Improvments 
 Enhance pytest logging experiance within Robot Framework (similar structure to pytest_robotframework / pytest-robotframework)

 Ensure compatibility with the Hypothesis package (property based testing addon for pytest).

 Add posibility to rename keyword for Robot Framework (RF supports this, but it may not currently work with Pytest)

 Add the decorator parameters to pytest execution with user parameterization.

 Introduce the ability to execute pytest in a separate process, providing added convenience for users.
 
 Enable the transfer of parameters from Robot Framework to pytest execution, such as log levels.
 
 Are there any additional tips or suggestions you would like to share? Please feel free to let me know!

## Support Me 💡

If this project has **saved you time or made your day easier, why not buy me a coffee?** ☕ Every contribution helps me **stay motivated** and keep improving the tool for users like you!

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-orange?logo=buymeacoffee&style=flat-square)](https://buymeacoffee.com/petrkus)

🙏 **With your support**, I can dedicate more time to developing new features, improving existing tools, and creating new resources—**all in my free time after regular work**. Your donations not only inspire me to continue but also show me that this **tool has real users** who want me to keep improving and supporting it.

You can also support me in the following ways:
- Directly through **GitHub Sponsors**: [GitHub Sponsors](https://github.com/sponsors/petrkus) (look for the heart on my profile).
- ⭐ Add a star to this project.
- 👀 Watch the project.
- 📝 Leave bug reports or suggestions for new features.

💖 **Thank You** for considering supporting my work!