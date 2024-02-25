# pytest-in-robotframework
*pytest-in-robotframework* enables the running of pytest within the Robot Framework, allowing users to leverage the advantages of both frameworks.

To achieve this integration, simply add the decorator '\@pytest_execute' above all the PyTest fixtures within your Python tests/keywords in Python libraries.

At present, this code serves as a proof of concept but is alrady usable.

PyTest's console logs are captured as informational messages in Robot Framework logs. If any test in PyTest fails, the entire keyword in Robot Framework fails.

It works with functions and methods too, as long as they follow the naming conventions required by pytest.

## Example

Robot Framework file:
```robotframework
#The Example of usage  - suite_name.robot file

*** Settings ***
Documentation     Proof of Concept integration PyTest under hood of Roboto Framework
Library  TestExperiment.py


*** Test Cases ***
Login User with Password
    Open Web Page  https://www.saucedemo.com/
    Test Login As  user  password  #the user and password is here only for Robot Framework checks (is not used)
```

Python File: 
```python
#The Example of usage  - TestExperiment.py file
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

import pytestinrobotframework #EXAMPLE USAGE - must import!



class TestExperiment: #EXAMPLE USAGE - must have this name!
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    def open_web_page(self,page): 
        self.driver.get(page)

    @pytest_execute #EXAMPLE USAGE - this is the new decorator that execute the keyword in PyTest instead Robot Framework!
    #@pytest.mark.parametrize("user,password", [("standard_user", "secret_sauce"),("locked_out_user", "secret_sauce"),("problem_user", "secret_sauce")]) #failing example
    @pytest.mark.parametrize("user,password", [("standard_user", "secret_sauce"),("problem_user", "secret_sauce")]) #passing example
    def test_login_as(self,user,password):
        #assert False
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
        self.driver.close()
```

## Future planed Improvments 
 Enhance pytest logging experiance within Robot Framework (similar structure to pytest_robotframework / pytest-robotframework)
 Ensure compatibility with the Hypothesis package.
 Add posibility to rename keyword for Robot Framework (RF supports this, but it may not currently work with Pytest)
