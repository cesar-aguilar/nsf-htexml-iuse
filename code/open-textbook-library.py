# %%
import csv
import time
import json

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


# %%
base_url = 'https://open.umn.edu'
url = 'https://open.umn.edu/opentextbooks/subjects/'

disciplines = {
    'mathematics': [
        'algebra', 'analysis', 'calculus', 
        'geometry-and-trigonometry', 'statistics', 'applied', 'pure'],

    'engineering': ['civil', 'electrical', 'mechanical'],

    'cs': ['databases', 'information-systems', 'programming-languages'],

    'sciences': ['biology', 'chemistry', 'geology', 'physics'],
}

my_headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

#%%

# Create a new instance of the Chrome driver
browser = webdriver.Chrome()
book_titles = []

summary_data = {}

for discipline, subjects in disciplines.items():

    disc = discipline.replace('-', '_')

    summary_data[disc] = {
        'count': 0,
        'formats': {},
        'licenses': {},
    }

    for subject in subjects:

        sub = subject.replace('-', '_')

        subject_url = url + subject
        browser.get(subject_url)
        time.sleep(2)

        # Get the body
        body = browser.find_element(By.TAG_NAME, 'body')

        no_of_pagedowns = 200

        while no_of_pagedowns:
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
            no_of_pagedowns -= 1

        # Get the list of books
        book_web_elements = browser.find_elements(
            By.CSS_SELECTOR, 'div.ShortDescription')

        book_file = discipline + '-textbooks.csv'

        with open(book_file, 'a') as f:

            csv = ''

            for book in book_web_elements:

                div = BeautifulSoup(book.get_attribute(
                    'innerHTML'), 'html.parser')
                href = div.find('h2').find('a')['href']
                page_url = base_url + href

                book_page = requests.get(page_url, headers=my_headers)

                book_soup = BeautifulSoup(book_page.content, 'html.parser')

                title = book_soup.find('h1').text.strip()

                if title in book_titles:
                    continue
                else:
                    book_titles.append(title)

                license = book_soup.find(
                    id='Badge-Condition').find('span').text.strip()

                formats = book_soup.find(id='BookTypes').find_all('a')

                formats = [a.text.strip() for a in formats]

                row = f"\"{subject.title()}\", \"{title}\", \"{license}\", \"{formats}\"\n"

                csv += row

                f.write(row)

                print(row)

                summary_data[disc]['count'] += 1
                summary_data[disc]['licenses'][license] = summary_data[disc]['licenses'].get(
                    license, 0) + 1
                for format in formats:
                    summary_data[disc]['formats'][format] = summary_data[disc]['formats'].get(
                        format, 0) + 1

                time.sleep(1)

        summary_file = discipline + '-open-textbooks-library-summary.csv'

        with open(summary_file, 'a') as f2:
            json.dump(summary_data[disc], f2)
            f2.write('\n')

        print(f"Finished {subject.title()}")


# %%
# Open csv and keep only rows with unique second field
import csv

for discipline in disciplines:

    unique_titles = []

    book_file = discipline + '-textbooks.csv'
    unique_book_file = discipline + '-textbooks-unique.csv'

    with open(book_file, 'r') as f, open(unique_book_file, 'w') as f2:

        reader = csv.reader(f, quotechar='"')

        for line in reader:

            subject, title, *other = line
            if title in unique_titles:
                continue
            else:
                unique_titles.append(title)
                f2.write(','.join(line) + "\n")

    print(f'Total books {discipline} is {len(unique_titles)}')

# %%
import numpy as np
import matplotlib.pyplot as plt

math = {"count": 119, "formats": {"PDF": 118, "Online": 47, "Hardcopy": 43, "LaTeX": 21, "eBook": 16, "MS Word": 4, "XML": 3}, "licenses": {"CC BY-NC-SA": 38, "CC BY-SA": 29, "Free Documentation License (GNU)": 9, "CC BY-NC": 10, "CC BY": 28, "CC BY-NC-ND": 3, "CC0": 1, "CC BY-ND": 1}}
sciences = {"count": 145, "formats": {"Online": 83, "eBook": 57, "PDF": 142, "XML": 26, "ODF": 16, "MS Word": 6, "Hardcopy": 30, "Google Doc": 1, "LaTeX": 1}, "licenses": {"CC BY-SA": 10, "CC BY-NC-SA": 55, "CC BY": 49, "CC BY-NC": 24, "CC BY-NC-ND": 7}}
engineering = {"count": 39, "formats": {"Online": 14, "eBook": 12, "PDF": 38, "XML": 6, "Hardcopy": 15, "LaTeX": 1, "ODF": 6, "MS Word": 2}, "licenses": {"CC BY": 8, "CC BY-NC": 10, "CC BY-NC-SA": 14, "CC BY-SA": 4, "Free Documentation License (GNU)": 3}}
cs = {"count": 35, "formats": {"PDF": 35, "Hardcopy": 10, "eBook": 11, "Online": 18, "MS Word": 2, "XML": 1, "LaTeX": 5}, "licenses": {"CC BY-SA": 4, "CC BY-NC": 7, "CC BY-NC-SA": 17, "CC BY": 7}}























