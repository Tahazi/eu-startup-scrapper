import requests
from bs4 import BeautifulSoup
import os

# Function to scrape company data from a single page
def scrape_company_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    all_data = {}
    if response.status_code == 200:
    # Extract company data points using selectors
        company_name = soup.find("h1", class_="entry-title td-page-title").text.strip()
        logo_element = soup.find("div", class_="listing-thumbnail")
        if logo_element:
            logo_url = logo_element.find("a").get("href")
        label_elements = soup.find_all("span", class_="field-label")

        # Create an empty dictionary to store data
        
        # Insert name and logo to the dictionary
        all_data["name"] = company_name
        all_data["logo"] = logo_url

        # Loop through each label element
        for label in label_elements:
        # Get the label text
            label_text = label.text.strip()

        # Find the next sibling value element (assuming they're consecutive)
            next_sibling = label.find_next_sibling("div", class_="value")
            if next_sibling:
                # Get the value text and add it to the dictionary with label as key
                value_text = next_sibling.text.strip()
                all_data[label_text] = value_text



    # return the final JSON object
    return(transform_company_data(all_data))


def transform_company_data(data):
  """
  Transforms a company data JSON object to a desired output format.

  Args:
      data: A dictionary containing eu-startup labeled company data.

  Returns:
      A dictionary with the transformed company data.
  """
  if data == {}:
     return {}
  output_data = {
      "name": data["name"].upper(),
      "original_name": data["name"],
      "source": {
          "name": "eu-startups",
          "id": f"eu-startups.com-{data['name'].lower().replace(' ', '-')}",
          "uri": f"https://www.eu-startups.com/directory/{data['name'].lower().replace(' ', '-')}/"
      },
      "location": {
          "country": data["Category"],
          "city": data["Based in"]
      },
    #   "blurb": data["Business Description"],
    #   "description": data["Long Business Description"],
      "tag": [
          {"type": "tag", "label": tag.strip()} for tag in data["Tags"].split(",")
      ],
      "founded": data["Founded"] + "-01-01",
      "website": {
          "url": data["Website"]
      },
      "logo": data["logo"]
  }

  return output_data

# Function to scrape company links from the directory page
def scrape_directory_page(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.content, "html.parser")
  # Find all company links on the page (modify selector as needed)
  company_links = []
  for h3 in soup.find_all("div", class_="listing-title"):
    for a in h3("a"):
      company_links.append(a.get('href'))

  # Loop through each link and call scrape_company_page
  company_data = []
  for link in company_links:
    company_data.append(scrape_company_page(link))
    print(f"{link.split('/')[-2]} complete")
  return company_data

def write_companies_to_files(company_data, file_prefix="companies_", max_companies_per_file=5):
  """Writes company data to multiple files with a maximum number of companies per file.

  Args:
      company_data: A list of dictionaries containing company data.
      file_prefix: A string prefix for the filenames (default: "companies_").
      max_companies_per_file: The maximum number of companies to store in each file (default: 1000).
  """

  # Number of files needed (rounded up)
  num_files = (len(company_data) + max_companies_per_file - 1) // max_companies_per_file
  data_folder = "data"
  if not os.path.exists(data_folder):
    os.makedirs(data_folder)
  # Loop through the files
  for file_num in range(num_files):
    # Create filename with sequential numbering
    filename = f"data/{file_prefix}{file_num + 1}.json"

    # Slice the company data for this file
    companies_to_write = company_data[file_num * max_companies_per_file:(file_num + 1) * max_companies_per_file]

    # Write data to JSON file
    with open(filename, "w") as f:
      import json
      json.dump(companies_to_write, f, indent=4)  # Add indentation for readability (optional)