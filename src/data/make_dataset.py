# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

# Web scraping libraries
import requests
import urllib.request
from bs4 import BeautifulSoup
import webbrowser
from time import sleep
import shutil
import os
from zipfile import ZipFile
import wget
def get_urls_soup_for_citibike(url: str = 'https://s3.amazonaws.com/tripdata/'):
    '''
    Parse XML website as soup for further processing.
    '''
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    return soup
def filter_citibike_urls_with_zip_data(soup):
    '''
    Build list of links containing zip files.
    '''
    data_files = soup.find_all('key')
    # Instantiate empty list
    zip_files = []  # Populate list with zip file names
    for file in range(len(data_files) - 1):
        zip_files.append(data_files[file].get_text())
    return zip_files

def download_files_from_url_list(file_list: list,
                                output_filepath: str,
                                base_url: str="https://s3.amazonaws.com/tripdata/",
                                filter_for_year: str="2018"
                                ):
    '''
    Download files from url list.
    '''
    for file in file_list:
        if filter_for_year in file:
            wget.download(url=base_url+file, out=output_filepath)
            sleep(8)

def unzip_files_and_delete_zip(output_filepath: str="data/raw/",
                               delete_zip_file_after_unzip: bool=True):
    '''
    Looks in output filepath for zip files and unzips them.
    Deletes the zip file afterwards.
    '''
    # Unzip files and clean up data folder
    for item in os.listdir(output_filepath):
        if item.endswith('.zip'):
            file_name = output_filepath + item
            zip_ref = ZipFile(file_name)
            zip_ref.extractall(output_filepath)
            zip_ref.close()
            if delete_zip_file_after_unzip:
                os.remove(file_name)

def main(output_filepath: str="data/raw/"):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Writing raw data to {output_filepath}")
    logger.info('making final data set from raw data')
    soup = get_urls_soup_for_citibike()
    zip_files = filter_citibike_urls_with_zip_data(soup)
    download_files_from_url_list(zip_files,output_filepath=output_filepath)
    unzip_files_and_delete_zip()

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
