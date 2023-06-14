#!/usr/bin/env python3
import os
import time
import wget
import argparse


def download_file(url: str, destination: str, filename: str = None):
    """
    Download a file from the specified URL to the destination path with the filename.

    Args:
        url (str): The URL of the file to download.
        destination (str): The path where the downloaded file should be saved.
        filename (str, optional): The desired filename for the downloaded file.
            If not provided, the original filename from the URL will be used.
    """
    try:
        os.makedirs(destination, exist_ok=True)

        if filename:
            timestamp = time.strftime("%Y%m%d")
            file_extension = os.path.splitext(url)[1]
            filename_with_extension = f"{timestamp}_{filename}{file_extension}"
            file_path = os.path.join(destination, filename_with_extension)
            wget.download(url, file_path)
            print(f"\nFile downloaded successfully to: {file_path}")
        else:
            wget.download(url, destination)
            print(f"\nFile downloaded successfully to: {destination}")

    except FileNotFoundError:
        print(f"Error: The specified directory '{destination}' does not exist.")
    except Exception as e:
        print(f"Error downloading file: {e}")


def download_files(url_dict: dict, destination: str):
    """
    Download files from the given URLs and save them to the specified directory.

    Args:
        url_dict (dict): A dictionary containing the URL as key and the desired filename as value.
        destination (str): The path to save the downloaded files.
    """
    for url, filename in url_dict.items():
        download_file(url, destination, filename)


def main():
    """
    Main function to handle command-line arguments and initiate file downloads.
    """
    parser = argparse.ArgumentParser(description="File Downloader")
    parser.add_argument("destination", type=str, help="Path where the downloaded files should be saved")
    parser.add_argument("-u", "--urls", nargs='+', metavar=("URL", "FILENAME"), action="append",
                        help="URLs and corresponding filenames (optional) to download")
    args = parser.parse_args()

    url_dict = {}
    if args.urls:
        for url, filename in args.urls:
            url_dict[url] = filename

    if url_dict:
        download_files(url_dict, args.destination)
    else:
        print("No files to download.")


if __name__ == "__main__":
    main()
