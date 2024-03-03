*** Settings ***
Documentation     Basic Tests for pytest-in-robotframewrok library 
Library  ../pytest_in_robotframework/pytest_in_robotframework.py
Library  TestCalculation.py


*** Test Cases ***
Test Pytest parametrization feature
    test calculations  4  +  5  9
    