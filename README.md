
# Startup Scraper

This project is a web scraping tool designed to extract data about startups from a specified directory website. It uses Python's `requests` and `BeautifulSoup` libraries to parse HTML content and gather detailed information about various companies listed on the site.

## Features
- Scrape detailed company information from individual pages.
- Navigate through directory listings to compile data on multiple companies efficiently.
- Output the data into structured JSON files, with customizable settings for the volume of data per file.

## Technologies
- Python 3
- BeautifulSoup
- requests

## Installation
Clone this repository and navigate into the project directory. Install the required dependencies by running:
```bash
pip install -r requirements.txt
```

## Usage
Run the script from the command line, specifying the base URL of the directory and the maximum number of pages to traverse:
```bash
python scrape_startups.py <base_url> --max_pages MAX_PAGES
```
Replace `<base_url>` with the actual URL you want to scrape and `MAX_PAGES` with the desired number of pages to process. The script will output JSON files with the data of the scraped companies.

## Configuration
The output file settings can be adjusted in the `utils_functions.py` file, where you can set the prefix and maximum number of companies per file.

## Contributing
Contributions to this project are welcome. To contribute:
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Create a new Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Output Data Schema

The JSON output for each company contains the following structure:

- **name**: String (uppercased version of the original name)
- **original_name**: String
- **source**:
  - **name**: String ("eu-startups")
  - **id**: String (derived from the company name)
  - **uri**: URL (constructed using the company name)
- **location**:
  - **country**: String (maps to the "Category" in source data)
  - **city**: String (maps to "Based in" in source data)
- **tag**: Array of objects, each containing:
  - **type**: String ("tag")
  - **label**: String (each tag derived from the "Tags" field, split by commas)
- **founded**: Date (year of founding followed by "-01-01")
- **website**:
  - **url**: URL
- **logo**: String (URL or path to the logo)
