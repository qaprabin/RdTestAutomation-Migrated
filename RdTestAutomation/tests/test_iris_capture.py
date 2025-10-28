"""
Hello Prabin This is your new, separate test for the Iris flow.
"""

import pytest
import time
import xml.etree.ElementTree as ET  # For parsing XML
from pages.home_page import HomePage
from utils import csv_utils


# This class will hold all tests for the Iris flow
class TestIrisCapture:

    # This fixture (from conftest) sets up the driver
    # and gives it to our home_page fixture
    @pytest.fixture(scope="class")
    def home_page(self, driver):
        # This creates the HomePage object once for this test class
        return HomePage(driver)

    @pytest.mark.order(1)
    def test_initial_device_setup(self, home_page):
        # We re-run this to ensure the page is ready
        home_page.click_discover_avdm()
        home_page.click_device_info()

    @pytest.mark.order(2)
    def test_configure_iris_settings(self, home_page):
        # This is the main setup for the Iris test
        home_page.select_environment("S")
        home_page.select_data_type("P")
        home_page.select_finger_count("0")  # Set finger to 0 for Iris
        home_page.select_iris_type("ISO")
        home_page.select_iris_count("1") # Prabin if you want to singe iris or 2 iris then, Select accordingly with your requirment

    @pytest.mark.order(3)
    @pytest.mark.parametrize("iteration", range(1, 11))  # Runs 10 times
    def test_perform_iris_capture_and_log(self, home_page, iteration):

        capture_count = iteration
        print(f"\n--- Starting Iris Capture: {capture_count} ---")

        start_time = time.time()

        home_page.click_capture()
        pid_data_xml = home_page.get_pid_data()  # This is the FULL, multi-line XML

        end_time = time.time()
        seconds_taken = end_time - start_time
        print(f"Capture Time duration: {seconds_taken:.2f} seconds")

        # --- Replicating your Java XML logic ---
        # 1. Get the values from the page *after* capture
        i_count = home_page.get_selected_iris_count()
        data_type_value = home_page.get_selected_data_type_value()

        # 2. As requested: get the "Iris Type" for the CSV log
        iris_type_for_log = home_page.get_selected_iris_type()

        # 3. Replicate Java's logic: dataTypeValue.equals("0") ? "X" : "P";
        data_type_label = "X" if data_type_value == "0" else "P"

        # 4. Parse the XML and build the final string
        try:
            root = ET.fromstring(pid_data_xml)
            resp_element = root.find(".//Resp")

            if resp_element is not None:
                # Build the exact string your Java code creates
                # resp_data_string = (
                #     f' <Resp errCode="{resp_element.get("errCode")}" '
                #     f'errInfo="{resp_element.get("errInfo")}" '
                #     f'iCount="{i_count}" '  # Inject iCount from dropdown
                #     f'fCount="{resp_element.get("fCount")}" '
                #     f'fType="{resp_element.get("fType")}" '
                #     f'nmPoints="{resp_element.get("nmPoints")}" '
                #     f'qScore="{resp_element.get("qScore")}" '
                #     f'dataType="{data_type_label}" />'  # Inject dataType from dropdown
                # )
                '''
                --- THIS IS THE FIX ---
                We added , "" to .get() to set a default value
                '''
                resp_data_string = (
                    f' <Resp errCode="{resp_element.get("errCode", "")}" '
                    f'errInfo="{resp_element.get("errInfo", "")}" '
                    f'iCount="{i_count}" '
                    f'fCount="{resp_element.get("fCount", "")}" '  # Fixed
                    f'fType="{resp_element.get("fType", "")}" '  # Fixed
                    f'nmPoints="{resp_element.get("nmPoints", "")}" '  # Fixed
                    f'qScore="{resp_element.get("qScore", "")}" '
                    f'dataType="{data_type_label}" />'
                )
            else:
                resp_data_string = "Error: <Resp> tag not found in XML"

        except ET.ParseError:
            resp_data_string = "Error: Could not parse invalid XML"

        print(f"Extracted Resp Data: {resp_data_string}")

        # 5. Write to the CSV
        csv_utils.write_data(
            capture_count=capture_count,
            resp_data=resp_data_string,
            duration_seconds=f"{seconds_taken:.2f}",
            data_type=iris_type_for_log  # Log the Iris Type, as you requested
        )