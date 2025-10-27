'''
This file is the most important one, as it will replace your BaseTest.java).
'''

'''
We will convert your BaseTest.java (which uses TestNG) into its pytest equivalent. 
In pytest, we don't use a "base class" for this. 
We use a special file called conftest.py to create a "fixture". 
This fixture will automatically set up and tear down your driver.

Your (BaseTest.java) also depends on (ConfigReader.java), so we'll convert both.
'''

'''
The Base Test (Replaces BaseTest.java)
This is the most important part. We will now edit the tests/conftest.py file you created. 
This code creates a driver fixture that runs once for the entire session 
(just like your @BeforeSuite and @AfterSuite).
'''

import pytest
from selenium import webdriver
from utils.config_reader import get_property  # Import our new function


@pytest.fixture(scope="session")
def driver():
    # --- This is your @BeforeSuite setup ---

    # 1. Get URL from config
    url = get_property('settings', 'url')

    # 2. Set up the ChromeDriver
    # As mentioned, you don't need System.setProperty!
    # SeleniumManager handles it automatically.
    print("Setting up WebDriver...")
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()

    # 'yield' passes the driver object to your tests
    # The test will run at this point
    yield driver

    # --- This is your @AfterSuite teardown ---
    # This code runs after all tests are finished
    print("\nTearing down WebDriver...")
    if driver:
        driver.quit()