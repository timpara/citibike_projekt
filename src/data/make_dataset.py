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

def get_urls_soup_for_citibike(url: str = 'https://s3.amazonaws.com/tripdata/'):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'xml')

    return soup
def filter_citibike_urls_with_zip_data(soup):
    data_files = soup.find_all('Key')
    # Instantiate empty list
    zip_files = []  # Populate list with zip file names
    for file in range(len(data_files) - 1):
        zip_files.append(data_files[file].get_text())
    return zip_files

@click.command()
@click.argument('output_filepath', type=click.Path())
def main(output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Writing raw data to {output_filepath}")
    logger.info('making final data set from raw data')
    soup = get_urls_soup_for_citibike()
    data_files = filter_citibike_urls_with_zip_data(soup)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
