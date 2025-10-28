import pytest
import time
import xml.etree.ElementTree as ET
from pages.mobile_rd_page import MobileRdPage  # Ensure correct import
from utils import csv_utils
# Added imports for Selenium/Appium specifics needed for waits/exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TestMobileRdCapture:

    @pytest.fixture(scope="class")
    def mobile_rd_page(self, mobile_driver):  # Use mobile_driver fixture from conftest.py
        """Creates the MobileRdPage object once for this test class."""
        return MobileRdPage(mobile_driver)

    @pytest.mark.order(1)
    def test_setup_options(self, mobile_rd_page):
        """Sets up the initial dropdown options on the device."""
        print("\n--- Setting up device options ---")
        # Select options by index based on my Java project code
        # need to adjust indices if the dropdown options change
        mobile_rd_page.select_finger_count(1)  # Selects index 1 (likely "1" finger)
        mobile_rd_page.select_finger_type(2)  # Selects index 2 (e.g., "FMR", "FIR", "BOTH")
        mobile_rd_page.select_format(1)  # Selects index 1 (e.g., "PROTOBUF" / "XML")
        mobile_rd_page.select_env(1)  # Selects index 1 (e.g., "S", "PP", "P")
        mobile_rd_page.click_device_info()

    @pytest.mark.order(2)
    @pytest.mark.parametrize("iteration", range(1, 7))  # Replaces invocationCount = 6
    def test_perform_capture_and_log(self, mobile_rd_page, iteration):
        """Performs the capture action multiple times and logs results."""

        capture_count = iteration
        print(f"\n--- Starting Mobile Capture: {capture_count} ---")

        # --- Check if main screen is visible before proceeding ---
        try:
            # Use a short wait to check if the capture button is clickable
            WebDriverWait(mobile_rd_page.driver, 5).until(
                EC.element_to_be_clickable(mobile_rd_page.CAPTURE_BUTTON)
            )
        except TimeoutException:
            print("ERROR: Main screen elements not found before starting next capture.")
            # Optional: Add code here to try and navigate back (e.g., driver.back())
            pytest.fail("App did not return to the main screen after previous capture.")
        # --- End of check ---

        # --- Get the selected format BEFORE capturing ---
        selected_format = "Unknown"  # Default value
        try:
            selected_format = mobile_rd_page.get_selected_format()
            # Assuming "ISO" format corresponds to "X" and others to "P" (adjust if needed)
            # This logic might need refinement based on actual Format dropdown text values
            data_type_based_on_selection = "X" if "ISO" in selected_format else "P"
        except Exception as e:
            print(f"WARN: Could not get selected format before capture: {e}")
            data_type_based_on_selection = "P"  # Default if getting format fails

        start_time = time.time()
        mobile_rd_page.click_capture()

        result_text = ""  # Initialize result_text
        try:
            # get_output_text now includes robust waits and retries
            result_text = mobile_rd_page.get_output_text()
        except Exception as e:
            # Catch potential errors during get_output_text (like timeout)
            print(f"ERROR: Failed to get output text: {e}")
            result_text = f"Error getting output: {e}"  # Store error message
            # We will still log this attempt but mark it clearly

        end_time = time.time()
        seconds_taken = end_time - start_time

        # Initialize variables used in logging/parsing
        resp_data_string = ""
        # Check if capture likely succeeded based on PidData presence
        capture_successful = "<PidData" in result_text and "Error" not in result_text

        if not capture_successful:
            print(f"Capture failed or PidData missing:\n{result_text}\n")
            # Format the failure message for logging
            resp_data_string = f"Capture Failed: {result_text}"
            # Use the data type determined before capture attempt even on failure
            dataType_for_log = data_type_based_on_selection
        else:
            # --- XML Parsing Logic ---
            try:
                # Attempt to parse the XML only if capture seemed successful
                root = ET.fromstring(result_text)
                resp_element = root.find(".//Resp")

                if resp_element is not None:
                    fType_from_xml = resp_element.get("fType", "")
                    # Always use the data type determined BEFORE capture
                    dataType_for_log = data_type_based_on_selection

                    resp_data_string = (
                        f' <Resp errCode="{resp_element.get("errCode", "")}" '
                        f'errInfo="{resp_element.get("errInfo", "")}" '
                        f'fCount="{resp_element.get("fCount", "")}" '
                        f'fType="{fType_from_xml}" '
                        f'nmPoints="{resp_element.get("nmPoints", "")}" '
                        f'qScore="{resp_element.get("qScore", "")}" '
                        # Use the correct attribute name 'type' as per your Java code's output
                        f'type="{dataType_for_log}" />'
                    )
                else:
                    # This case handles valid XML but missing <Resp> tag
                    resp_data_string = "Error: <Resp> tag not found in XML"
                    dataType_for_log = "Unknown"  # Fallback if Resp tag missing

            except ET.ParseError:
                # This case handles completely invalid XML
                resp_data_string = f"Error: Could not parse invalid XML: {result_text}"
                dataType_for_log = "Invalid XML"  # Fallback if XML broken

        print(f"Capture [{capture_count}] completed in {seconds_taken:.2f} seconds")
        if capture_successful:
            print(f"{resp_data_string}\n")

        # --- CSV WRITING ---
        log_data = {
            "Capture_Count": capture_count,
            "RespData": resp_data_string,
            "DurationInSeconds": f"{seconds_taken:.2f}",
            # DataType/FingerType/IrisType columns removed as per previous request
        }
        csv_utils.write_data(log_data)

        # If capture failed based on initial check, explicitly fail the test iteration
        # This ensures pytest reports the failure even if no exception occurred during parsing/logging
        if not capture_successful:
            pytest.fail(f"Capture {capture_count} failed or PidData missing.")

