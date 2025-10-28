import pytest
import time
import xml.etree.ElementTree as ET  # We need this to parse XML
from pages.home_page import HomePage
from utils import csv_utils  # We only need csv_utils


# We create a class to group these tests, just like in TestNG
class TestCapture:

    # This fixture replaces your @BeforeClass 'pageSetup'
    @pytest.fixture(scope="class")
    def home_page(self, driver):
        # The 'driver' fixture comes from conftest.py
        return HomePage(driver)

    # @pytest.mark.order(1) replaces @Test(priority = 1)
    @pytest.mark.order(1)
    def test_initial_device_setup(self, home_page):
        # 'home_page' is injected from the fixture above
        home_page.click_discover_avdm()
        home_page.click_device_info()

    @pytest.mark.order(2)
    def test_configure_capture_settings(self, home_page):
        home_page.select_environment("PP")
        home_page.select_data_type("P")
        home_page.select_finger_type("BOTH")  # Your code had "FMR", so I kept it

    # @pytest.mark.order(3) replaces @Test(priority = 3)
    # This is the final, correct version of your test
    @pytest.mark.order(3)
    @pytest.mark.parametrize("iteration", range(1, 11))
    def test_perform_capture_and_log(self, home_page, iteration):

        capture_count = iteration
        print(f"\n--- Starting Capture: {capture_count} ---")

        start_time = time.time()

        home_page.click_capture()
        pid_data_xml = home_page.get_pid_data()  # This is the FULL, multi-line XML

        end_time = time.time()
        seconds_taken = end_time - start_time
        print(f"Capture Time duration: {seconds_taken:.2f} seconds")

        # Get data from the page for logging
        data_type_for_log = home_page.get_selected_data_type()
        finger_type_for_log = home_page.get_selected_finger_type()

        try:
            root = ET.fromstring(pid_data_xml)
            resp_element = root.find(".//Resp")

            if resp_element is not None:
                # This builds the clean string using the REAL data
                # Using .get(..., "") prevents "None" from appearing
                resp_data_string = (
                    f' <Resp errCode="{resp_element.get("errCode", "")}" '
                    f'errInfo="{resp_element.get("errInfo", "")}" '
                    f'fCount="{resp_element.get("fCount", "")}" '
                    f'fType="{resp_element.get("fType", "")}" '
                    f'nmPoints="{resp_element.get("nmPoints", "")}" '
                    f'qScore="{resp_element.get("qScore", "")}" '
                    f'dataType="{data_type_for_log}" />'
                )
            else:
                resp_data_string = "Error: <Resp> tag not found in XML"

        except ET.ParseError:
            resp_data_string = "Error: Could not parse invalid XML"

        print(f"Extracted Resp Data: {resp_data_string}")

        # --- UPDATED CSV WRITING ---
        # This uses the new "smart" csv_util that takes a dictionary
        log_data = {
            "Capture_Count": capture_count,
            "RespData": resp_data_string,
            "DurationInSeconds": f"{seconds_taken:.2f}",
            "DataType": data_type_for_log,
            "FingerType": finger_type_for_log  # Logs the finger type
        }

        csv_utils.write_data(log_data)
