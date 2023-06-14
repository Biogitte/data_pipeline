#!/usr/bin/env python3
import os
import time
import zipfile
import requests
import shutil


import requests

def download_file(url: str, destination: str, filename: str = None):
    try:
        os.makedirs(destination, exist_ok=True)

        if filename:
            timestamp = time.strftime("%Y%m%d")
            file_extension = os.path.splitext(url)[1]
            filename_with_extension = f"{timestamp}_{filename}{file_extension}"
            file_path = os.path.join(destination, filename_with_extension)
        else:
            filename = os.path.basename(url)
            file_path = os.path.join(destination, filename)

        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"\nFile downloaded successfully to: {file_path}")

    except FileNotFoundError:
        print(f"Error: The specified directory '{destination}' does not exist.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")


def download_files(url_dict: dict, destination: str):
    """
    Download files from the given URLs and save them to the specified directory.

    Args:
        url_dict (dict): A dictionary containing the URL as key and the desired filename as value.
        destination (str): The path where the downloaded files should be saved.
    """
    for url, filename in url_dict.items():
        download_file(url, destination, filename)


def download_zipfile(url: str, destination: str):
    """
    Download a ZIP file from the given URL to the specified directory.

    Args:
        url (str): The URL of the ZIP file to download.
        destination (str): The path where the downloaded ZIP file should be saved.

    Returns:
        str: The path to the downloaded ZIP file.
    """
    try:
        os.makedirs(destination, exist_ok=True)

        timestamp = time.strftime("%Y%m%d")
        filename = os.path.basename(url)
        if not filename.endswith(".zip"):
            filename += ".zip"
        filename_with_extension = f"{timestamp}_{filename}"
        file_path = os.path.join(destination, filename_with_extension)

        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"\nFile downloaded successfully to: {file_path}")

        return file_path

    except FileNotFoundError:
        print(f"Error: The specified directory '{destination}' does not exist.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return None


def unzip_csv_file(url: str, destination: str):
    """
    Unzip a file to the specified destination path.

    Args:
        file_path (str): The path of the ZIP file to unzip.
        destination (str): The path where the extracted files should be saved.
        :param url:
    """
    file_path = download_zipfile(url, destination)
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            # Extract the files to the zip_ref directory
            zip_ref.extractall(path='zip_ref')

        # Move the files from the zip_ref directory to the destination folder
        for root, dirs, files in os.walk('zip_ref'):
            for file in files:
                if file.endswith(".csv"):
                    source_path = os.path.join(root, file)
                    target_path = os.path.join(destination, file)
                    shutil.move(source_path, target_path)
        # Remove the empty zip_ref directory
        shutil.rmtree('zip_ref')

    except Exception as e:
        print(f"Error unzipping file: {e}")
