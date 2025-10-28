from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time


class MobileRdPage:
    """Page Object for the RdSample Mobile App."""

    # --- Locators ---
    FINGER_COUNT_DROPDOWN = (AppiumBy.ID, "com.mantra.rdsample:id/spinnerTotalIrisCount")
    FINGER_TYPE_DROPDOWN = (AppiumBy.ID, "com.mantra.rdsample:id/spinnerTotalIrisType")
    FORMAT_DROPDOWN = (AppiumBy.ID, "com.mantra.rdsample:id/spinnerTotalFingerFormat")
    ENV_DROPDOWN = (AppiumBy.ID, "com.mantra.rdsample:id/spinnerEnv")
    DEVICE_INFO_BUTTON = (AppiumBy.ID, "com.mantra.rdsample:id/btnDeviceInfo")
    CAPTURE_BUTTON = (AppiumBy.ID, "com.mantra.rdsample:id/btnCapture")
    OUTPUT_TEXT = (AppiumBy.ID, "com.mantra.rdsample:id/txtOutput")
    DROPDOWN_OPTION_BY_TEXT = (AppiumBy.XPATH, '//android.widget.TextView[@text="{}"]')
    DROPDOWN_OPTION_BY_INDEX = (AppiumBy.XPATH, '//android.widget.TextView[@index="{}"]')

    # --- Constructor ---
    def __init__(self, driver):
        self.driver = driver
        # Default wait time increased slightly for stability
        self.default_timeout = 25
        self.wait = WebDriverWait(self.driver, self.default_timeout)

        # --- Helper Methods ---

    def _find_element(self, locator, timeout=None):
        """Finds an element using a specified wait, defaults to class timeout."""
        if timeout is None:
            timeout = self.default_timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def _click(self, locator, timeout=None):
        """Finds and clicks an element using a specified wait."""
        if timeout is None:
            timeout = self.default_timeout
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def _select_dropdown_option(self, dropdown_locator, option_index):
        """Clicks the dropdown, then clicks the option by its index."""
        print(f"Selecting option {option_index} from dropdown...")
        self._click(dropdown_locator)
        time.sleep(0.5)  # Small pause for dropdown to open
        option_locator = (self.DROPDOWN_OPTION_BY_INDEX[0], self.DROPDOWN_OPTION_BY_INDEX[1].format(option_index))
        # Use a shorter timeout for clicking the option as it should appear quickly
        self._click(option_locator, timeout=5)

        # --- Page Actions ---

    def select_finger_count(self, option_index):
        self._select_dropdown_option(self.FINGER_COUNT_DROPDOWN, option_index)

    def select_finger_type(self, option_index):
        self._select_dropdown_option(self.FINGER_TYPE_DROPDOWN, option_index)

    def select_format(self, option_index):
        self._select_dropdown_option(self.FORMAT_DROPDOWN, option_index)

    def select_env(self, option_index):
        self._select_dropdown_option(self.ENV_DROPDOWN, option_index)

    def click_device_info(self):
        print("Device Info button clicked.")
        self._click(self.DEVICE_INFO_BUTTON)

    def click_capture(self):
        self._click(self.CAPTURE_BUTTON)

    def get_output_text(self):
        """
        Gets the text from the output field, waiting up to the default timeout.
        Includes retries for StaleElementReferenceException.
        """
        end_time = time.time() + self.default_timeout  # Max wait time based on class default
        last_exception = None
        while time.time() < end_time:
            try:
                # Wait for the element to be present first (use short wait in loop)
                output_element = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located(self.OUTPUT_TEXT)
                )
                # Now try to get the text. Re-finds implicitly if stale.
                # Adding a small sleep *after* finding but *before* getting text
                # can sometimes help if the text content updates slightly after presence.
                time.sleep(0.2)
                text_value = output_element.text
                if text_value:  # Check if text is not empty
                    return text_value.strip()
                # If text is empty, maybe it hasn't loaded yet, continue loop

            except StaleElementReferenceException as e:
                last_exception = e
                print("Stale element encountered getting output text, retrying...")
                # No need to sleep here, the loop will retry quickly
            except TimeoutException as e:
                last_exception = e
                # Element not even present within 2s, maybe capture is just slow
                print("Output element not present yet, retrying...")
                # Continue loop, wait will handle timeout overall

            # Brief pause before next loop iteration if element wasn't found or text empty
            time.sleep(0.5)

            # If loop finishes without returning, raise the last error or a TimeoutException
        if last_exception:
            raise last_exception
        else:
            raise TimeoutException(f"Could not get non-empty output text within {self.default_timeout} seconds.")

    def get_selected_format(self):
        """Gets the currently selected text from the Format dropdown."""
        # Use a short wait to ensure element is ready
        element = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.FORMAT_DROPDOWN)
        )
        return element.text

