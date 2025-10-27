import csv
import os
from utils.config_reader import get_property


# We update the function arguments to be clearer
def write_data(capture_count, resp_data, duration_seconds, data_type):
    # Get the file path from config.ini
    file_path = get_property('settings', 'csv_log_path')

    # Check if file exists to write header
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='') as csvfile:
        # Define column headers TO MATCH YOUR IMAGE
        fieldnames = ['Capture_Count', 'RespData', 'DurationInSeconds', 'DataType']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()  # Write header only if file is new

        writer.writerow({
            'Capture_Count': capture_count,
            'RespData': resp_data,
            'DurationInSeconds': duration_seconds,
            'DataType': data_type
        })