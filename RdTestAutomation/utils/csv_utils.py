# -----------------------------Start finger---------------------------------------
# import csv
# import os
# from utils.config_reader import get_property
#
#
# def write_data(data_to_write):
#     """
#     Writes a dictionary of data to the CSV file.
#     It will automatically add new columns if they don't exist.
#     """
#     file_path = get_property('settings', 'csv_log_path')
#     file_exists = os.path.isfile(file_path)
#
#     # --- New logic to remove specific columns ---
#     # We check if these keys exist in the dictionary and remove them.
#     if "DataType" in data_to_write:
#         del data_to_write["DataType"]
#     if "FingerType" in data_to_write:
#         del data_to_write["FingerType"]
#     # --- End of new logic ---
#
#     # We use 'a' (append) mode to add to the file
#     with open(file_path, 'a', newline='') as csvfile:
#
#         # --- New Smart Logic ---
#         # 1. Get the headers from the dictionary keys
#         fieldnames = list(data_to_write.keys())
#
#         # 2. Use DictWriter to write based on dictionary keys
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
#                                 extrasaction='ignore')
#
#         # 3. Write the header only if the file is new
#         if not file_exists:
#             writer.writeheader()
#
#         # 4. Write the data row
#         writer.writerow(data_to_write)
# --------------------------------End Finger------------------------------------------------


# # -----------------------------Start Iris----------------------------------------------------
# import csv
# import os
# from utils.config_reader import get_property
#
#
# # We update the function arguments to be clearer
# def write_data(capture_count, resp_data, duration_seconds, data_type):
#     # Get the file path from config.ini
#     file_path = get_property('settings', 'csv_log_path')
#
#     # Check if file exists to write header
#     file_exists = os.path.isfile(file_path)
#
#     with open(file_path, 'a', newline='') as csvfile:
#         # Define column headers TO MATCH YOUR IMAGE
#         fieldnames = ['Capture_Count', 'RespData', 'DurationInSeconds', 'DataType']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#         if not file_exists:
#             writer.writeheader()  # Write header only if file is new
#
#         writer.writerow({
#             'Capture_Count': capture_count,
#             'RespData': resp_data,
#             'DurationInSeconds': duration_seconds,
#             'DataType': data_type
#         })
# # -------------------------------------------End Iris_______________________

# ---------------------------------------Mobile Finger Capture-----------------------------

import csv
import os
from utils.config_reader import get_property

# This is the MASTER list of ALL possible columns from ALL your tests
# We remove the last three columns as requested
ALL_FIELDNAMES = [
    "Capture_Count",
    "RespData",
    "DurationInSeconds"
    # "DataType",      # Removed
    # "FingerType",    # Removed
    # "IrisType"       # Removed
]


def write_data(data_to_write):
    """
    Writes a dictionary of data to the CSV file using a predefined
    set of headers to ensure consistency across different tests.
    """
    file_path = get_property('settings', 'csv_log_path')
    file_exists = os.path.isfile(file_path)

    # Use 'a' (append) mode
    with open(file_path, 'a', newline='') as csvfile:
        # Use the master list of fieldnames
        # extrasaction='ignore' means it won't complain if data is missing a column
        # restval='' means it will write an empty string for missing columns
        writer = csv.DictWriter(csvfile, fieldnames=ALL_FIELDNAMES,
                                extrasaction='ignore', restval='')

        # Write the header ONLY if the file is new
        if not file_exists:
            writer.writeheader()

        # Write the data row (only columns present in data_to_write
        # that are also in ALL_FIELDNAMES will be written)
        writer.writerow(data_to_write)
# --------------------------------Mobile Finger Capture End----------------------------