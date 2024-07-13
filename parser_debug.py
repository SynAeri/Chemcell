import bs4
import pandas as pd
from urllib.request import urlopen

class TableExtractor:
    def __init__(self, url):
        """
        Initialize the TableExtractor with a URL to fetch the HTML content.
        :param url: URL of the web page containing the search results table. Format: str
        """
        self.url = url
        self.soup = None
        self.reaction_table = None

    def fetch_html(self):
        """
        Fetch the HTML content from the URL and create a BeautifulSoup object.
        :return: None
        """
        try:
            response = urlopen(self.url)
            html_data = response.read().decode('utf-8')
            self.soup = bs4.BeautifulSoup(html_data, "html5lib")
            print("HTML data fetched and soup created.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def extract_table(self):
        """
        Extract the search results table from the BeautifulSoup object.
        :return: None
        """
        try:
            # Locate the search results table
            self.reaction_table = self.soup.find('table', {"border": "0", "cellpadding": "0", "cellspacing": "0"})
            print("Search results table extracted.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def parse_table(self):
        """
        Parse the search results table and return it as a Pandas DataFrame.
        :return: DataFrame containing the search results.
        """
        try:
            rows = self.reaction_table.find_all('tr')
            data = []
            headers = [header.text for header in rows[0].find_all('th')]

            for row in rows[1:]:
                cells = row.find_all('td')
                record = {
                    headers[0]: cells[0].text.strip(),
                    headers[1]: cells[1].text.strip(),
                    headers[2]: cells[2].text.strip()
                }
                data.append(record)

            df = pd.DataFrame(data)
            return df
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

# Usage example
url = 'http://kinetics.nist.gov/kinetics/Search.jsp'
table_extractor = TableExtractor(url)
table_extractor.fetch_html()
table_extractor.extract_table()
results_df = table_extractor.parse_table()

# Display the DataFrame
print(results_df)
