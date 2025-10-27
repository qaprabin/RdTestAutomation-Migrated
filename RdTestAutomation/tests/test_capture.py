import pytest
import time  # Replaces System.currentTimeMillis()
from pages.home_page import HomePage
from utils import xml_utils, csv_utils  # Import our new utils
import xml.etree.ElementTree as ET


# We create a class to group these tests, just like in TestNG
class TestCapture:

    # This fixture replaces your @BeforeClass 'pageSetup'
    # It runs once for this class and creates the home_page object
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
        home_page.select_data_type("X")
        home_page.select_finger_type("FMR")

    # @pytest.mark.order(3) replaces @Test(priority = 3)
    # @pytest.mark.order(3)
    # def test_perform_capture_and_log(self, home_page):
    #     # We replace 'invocationCount = 10' with a simple 'for' loop.
    #     # This is much cleaner and easier to read.
    #
    #     for i in range(1, 11):  # This will run 10 times (1 through 10)
    #         capture_count = i  # This replaces your 'static captureCount'
    #
    #         print(f"\n--- Starting Capture: {capture_count} ---")
    #
    #         # Use time.time() which returns seconds (as a float)
    #         start_time = time.time()
    #
    #         home_page.click_capture()
    #         pid_data_xml = home_page.get_pid_data()
    #
    #         end_time = time.time()
    #
    #         # The calculation is simpler, as time is already in seconds
    #         seconds_taken = end_time - start_time
    #         print(f"Capture Time duration: {seconds_taken:.2f} seconds")
    #
    #         data_type_for_log = home_page.get_selected_data_type()
    #
    #         # Use our new Python utils
    #         resp_output = xml_utils.extract_resp_attributes(pid_data_xml, data_type_for_log)
    #         print(f"Extracted Resp Data: {resp_output}")
    #
    #         csv_utils.write_data(capture_count, resp_output, seconds_taken, data_type_for_log)




    # @pytest.mark.order(3)
    # def test_perform_capture_and_log(self, home_page):
    #     # We replace 'invocationCount = 10' with a simple 'for' loop.
    #
    #     for i in range(1, 11):  # This will run 10 times (1 through 10)
    #         capture_count = i
    #
    #         print(f"\n--- Starting Capture: {capture_count} ---")
    #
    #         start_time = time.time()
    #
    #         home_page.click_capture()
    #         pid_data_xml = home_page.get_pid_data()  # This is the raw XML string
    #
    #         end_time = time.time()
    #
    #         seconds_taken = end_time - start_time
    #         print(f"Capture Time duration: {seconds_taken:.2f} seconds")
    #
    #         data_type_for_log = home_page.get_selected_data_type()
    #
    #         # --- THIS IS THE FIX ---
    #         # Based on your image, you want to log the raw XML, not the parsed data.
    #         # We can skip the xml_utils part completely.
    #
    #         print(f"Raw Resp Data: {pid_data_xml}")
    #
    #         # Write the raw data to the CSV
    #         csv_utils.write_data(
    #             capture_count=capture_count,
    #             resp_data=pid_data_xml,  # Pass the raw XML string
    #             duration_seconds=f"{seconds_taken:.2f}",  # Format to 2 decimal places
    #             data_type=data_type_for_log
    #         )

    @pytest.mark.order(3)
    @pytest.mark.parametrize("iteration", range(1, 11))
    def test_perform_capture_and_log(self, home_page, iteration):
        # The loop is GONE. Pytest handles the looping.

        capture_count = iteration  # Use the iteration number

        print(f"\n--- Starting Capture: {capture_count} ---")

        start_time = time.time()

        home_page.click_capture()
        pid_data_xml = home_page.get_pid_data()  # This is the FULL, multi-line XML

        end_time = time.time()

        seconds_taken = end_time - start_time
        print(f"Capture Time duration: {seconds_taken:.2f} seconds")

        data_type_for_log = home_page.get_selected_data_type()

        # --- THIS IS THE FIX ---
        # We will parse the giant XML string to find the one line we want.
        try:
            # Parse the XML string
            root = ET.fromstring(pid_data_xml)

            # Find the <Resp> tag inside the XML
            # The .// means "find at any level"
            resp_element = root.find(".//Resp")

            if resp_element is not None:
                # Convert just that <Resp> tag back into a clean, single string
                resp_data_string = ET.tostring(resp_element, encoding='unicode').strip()
            else:
                resp_data_string = "Error: <Resp> tag not found in XML"

        except ET.ParseError:
            resp_data_string = "Error: Could not parse invalid XML"
        # --- END OF FIX ---

        print(f"Extracted Resp Data: {resp_data_string}")

        # Write the NEW, CLEAN string to the CSV
        csv_utils.write_data(
            capture_count=capture_count,
            resp_data=resp_data_string,  # Pass the clean <Resp ... /> string
            duration_seconds=f"{seconds_taken:.2f}",  # Format to 2 decimal places
            data_type=data_type_for_log
        )