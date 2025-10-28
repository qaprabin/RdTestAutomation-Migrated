from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.config_reader import get_property


class HomePage:
    # --- Locators (as class variables) ---
    # Python convention is to use UPPER_SNAKE_CASE for constants
    DISCOVER_AVDM_BUTTON = (By.XPATH, "//button[contains(text(),'Discover AVDM')]")
    DEVICE_INFO_BUTTON = (By.XPATH, "//button[contains(text(),'Device Info')]")
    CAPTURE_BUTTON = (By.XPATH, "//button[contains(text(),'Capture')]")
    ENV_DROPDOWN = (By.ID, "Env")
    DATA_TYPE_DROPDOWN = (By.ID, "Dtype")
    FINGER_TYPE_DROPDOWN = (By.ID, "Ftype")
    PID_DATA_TEXT_AREA = (By.ID, "txtPidData")

    # --- New Iris Locators ---
    FINGER_COUNT_DROPDOWN = (By.ID, "Fcount")
    IRIS_TYPE_DROPDOWN = (By.ID, "Itype")
    IRIS_COUNT_DROPDOWN = (By.ID, "Icount")

    # --- Constructor (replaces public HomePage) ---
    def __init__(self, driver):
        self.driver = driver
        # Read timeout from config and convert to integer
        timeout = int(get_property('settings', 'default_timeout'))
        self.wait = WebDriverWait(self.driver, timeout)

    # --- Page Methods (replaces public void ...) ---
    # Note: 'self' is the Python equivalent of 'this'

    def click_discover_avdm(self):
        self.driver.find_element(*self.DISCOVER_AVDM_BUTTON).click()
        # Use EC for ExpectedConditions
        alert = self.wait.until(EC.alert_is_present())
        print(f"\nAlert Text: {alert.text}")
        alert.accept()

    def click_device_info(self):
        element = self.wait.until(EC.element_to_be_clickable(self.DEVICE_INFO_BUTTON))
        element.click()

    def select_environment(self, text):
        select_element = self.driver.find_element(*self.ENV_DROPDOWN)
        select = Select(select_element)
        select.select_by_visible_text(text)
        print(f"Environment selected: {text}")

    def select_data_type(self, text):
        select_element = self.driver.find_element(*self.DATA_TYPE_DROPDOWN)
        select = Select(select_element)
        select.select_by_visible_text(text)
        print(f"Data Type selected: {text}")

    def select_finger_type(self, text):
        select_element = self.driver.find_element(*self.FINGER_TYPE_DROPDOWN)
        select = Select(select_element)
        select.select_by_visible_text(text)
        print(f"Finger Type selected: {text}")

    def get_selected_data_type(self):
        select_element = self.driver.find_element(*self.DATA_TYPE_DROPDOWN)
        select = Select(select_element)
        return select.first_selected_option.text

    def click_capture(self):
        self.wait.until(EC.element_to_be_clickable(self.CAPTURE_BUTTON)).click()
        try:
            alert = self.wait.until(EC.alert_is_present())
            print(f"Capture Alert: {alert.text}")
            alert.accept()
        except TimeoutException:
            print("No alert present after capture.")

    def get_pid_data(self):
        element = self.wait.until(EC.presence_of_element_located(self.PID_DATA_TEXT_AREA))
        # Use .get_attribute("value") and .strip()
        return element.get_attribute("value").strip()
    """
    Prabin this part is your iris part just do remember for now its both Finger and Iris.
    Remember it ok.
    """
    # --- New Iris Methods ---

    def select_finger_count(self, text):
        select_element = self.driver.find_element(*self.FINGER_COUNT_DROPDOWN)
        select = Select(select_element)
        select.select_by_visible_text(text)
        print(f"Finger Count selected: {text}")

    def select_iris_type(self, text):
        select_element = self.driver.find_element(*self.IRIS_TYPE_DROPDOWN)
        select = Select(select_element)
        select.select_by_visible_text(text)
        print(f"Iris Type selected: {text}")

    def select_iris_count(self, text):
        select_element = self.driver.find_element(*self.IRIS_COUNT_DROPDOWN)
        select = Select(select_element)
        select.select_by_visible_text(text)
        print(f"Iris Count selected: {text}")

    # --- New Helper Methods to Get Data ---
    # We need these to build the final XML string, just like your Java code

    def get_selected_iris_type(self):
        select_element = self.driver.find_element(*self.IRIS_TYPE_DROPDOWN)
        select = Select(select_element)
        return select.first_selected_option.text

    def get_selected_iris_count(self):
        select_element = self.driver.find_element(*self.IRIS_COUNT_DROPDOWN)
        select = Select(select_element)
        return select.first_selected_option.text

    def get_selected_data_type_value(self):
        # Your Java code gets the "value" (0 or 1), not the text (X or P)
        select_element = self.driver.find_element(*self.DATA_TYPE_DROPDOWN)
        select = Select(select_element)
        return select.first_selected_option.get_attribute("value")

    def get_selected_finger_type(self):
        select_element = self.driver.find_element(*self.FINGER_TYPE_DROPDOWN)
        select = Select(select_element)
        return select.first_selected_option.text
