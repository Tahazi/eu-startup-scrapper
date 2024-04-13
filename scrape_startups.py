"""
Scrape company data from a directory website.

This script extracts company information from a directory website and writes it
to JSON files.

Usage:
  python scrape_company_directory.py <base_url> [--max_pages MAX_PAGES]

Arguments:
  <base_url> (str): The base URL of the company directory website.
  --max_pages (int, optional): The maximum number of directory pages to scrape
                               (default: 1).
"""

import argparse
from bs4 import BeautifulSoup
import requests
from utils_functions import scrape_directory_page, write_companies_to_files


def main():
  """
  The main function that parses arguments, scrapes data, and writes to files.
  """

  parser = argparse.ArgumentParser(description="Scrape company data from a directory website.")
  parser.add_argument("base_url", type=str, help="Base URL of the company directory website.")
  parser.add_argument(
      "--max_pages",
      type=int,
      help="Maximum number of directory pages to scrape (default: 1)",
      default=1,
  )
  args = parser.parse_args()

  base_url = args.base_url
  max_pages = args.max_pages

  all_company_data = []

  for page_number in range(1, max_pages + 1):
    print(f"------- Scraping page {page_number} -------")
    directory_url = f"{base_url}/page/{page_number}"

    response = requests.get(directory_url)
    soup = BeautifulSoup(response.content, "html.parser")

    next_page_button = soup.find("span", class_="next")
    if not next_page_button:
      break

    company_data = scrape_directory_page(directory_url)
    all_company_data.extend(company_data)

  write_companies_to_files(all_company_data)
  print("Company data written to files successfully!")


if __name__ == "__main__":
  main()