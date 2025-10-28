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

# import pytest
# from selenium import webdriver
# from utils.config_reader import get_property  # Import our new function
#
#
# @pytest.fixture(scope="session")
# def driver():
#     # --- This is your @BeforeSuite setup ---
#
#     # 1. Get URL from config
#     url = get_property('settings', 'url')
#
#     # 2. Set up the ChromeDriver
#     # As mentioned, you don't need System.setProperty!
#     # SeleniumManager handles it automatically.
#     print("Setting up WebDriver...")
#     driver = webdriver.Chrome()
#     driver.get(url)
#     driver.maximize_window()
#
#     # 'yield' passes the driver object to your tests
#     # The test will run at this point
#     yield driver
#
#     # --- This is your @AfterSuite teardown ---
#     # This code runs after all tests are finished
#     print("\nTearing down WebDriver...")
#     if driver:
#         driver.quit()


import pytest
import os
from selenium import webdriver
from utils.config_reader import get_property

# --- Appium Imports ---
from appium import webdriver as appium_webdriver
from appium.options.android import UiAutomator2Options


# -----------------------------------------------------------------
# --- WEB DRIVER FIXTURE (Your existing code, no changes) ---
# -----------------------------------------------------------------
@pytest.fixture(scope="session")
def driver():
    # --- This is your @BeforeSuite setup ---

    # 1. Get URL from config
    url = get_property('settings', 'url')

    # 2. Set up the ChromeDriver
    print("Setting up WebDriver (Chrome)...")
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()

    yield driver

    # --- This is your @AfterSuite teardown ---
    print("\nTearing down WebDriver (Chrome)...")
    if driver:
        driver.quit()
# -----------------------------------------------------------------
# --- UPDATED MOBILE DRIVER FIXTURE (Using your Java settings) ---
# -----------------------------------------------------------------
@pytest.fixture(scope="session")
def mobile_driver():
    # --- This sets up your Android App ---

    print("\nSetting up Appium Driver (Android)...")

    # 2. Set Appium Capabilities from your Java file
    options = UiAutomator2Options()
    options.automation_name = "UiAutomator2"

    # --- FIX: Add deviceName back ---
    # We use the same ID as the udid, or you can put the device's model name
    options.device_name = "Realme narzo N55"
    options.udid = "192.168.6.252:5555"  # Use 'udid' for device ID

    options.auto_grant_permissions = True
    options.platform_name = "Android"
    options.platform_version = "13"  # Make sure this matches your device
    options.app_package = "com.mantra.rdsample"
    options.app_activity = "com.mantra.rdsample.MainActivityMFS"
    # options.app_activity = "com.mantra.rdsample.MainActivityIris"

    options.set_capability("adbExecTimeout", 60000)

    # 3. Start the Appium driver
    appium_server_url = 'http://127.0.0.1:4723/wd/hub'

    mobile_driver = appium_webdriver.Remote(
        command_executor=appium_server_url,
        options=options
    )

    yield mobile_driver

    # --- This tears down your Android App ---
    print("\nTearing down Appium Driver (Android)...")
    if mobile_driver:
        mobile_driver.quit()