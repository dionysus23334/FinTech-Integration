
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

class SimpleSpider:

    def __init__(self):
        pass

    # Function to scrape website and return data as JSON
    def scrape_website(self, url):
        # Send a GET request to the website
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the main text content (e.g., <p> tags)
        text_content = ' '.join([p.get_text() for p in soup.find_all('p')])

        # Extract all links from <a> tags
        links = [a['href'] for a in soup.find_all('a', href=True)]

        # Extract all images from <img> tags
        image_links = [img['src'] for img in soup.find_all('img', src=True)]

        # Extract tables and convert to DataFrame
        tables = soup.find_all('table')
        tables_data = []
        
        for table in tables:
            # Create a pandas DataFrame from each table
            df = pd.read_html(str(table))[0]  # Get the first table from the HTML
            tables_data.append(df.to_dict(orient='records'))  # Convert to list of dicts for JSON format

        # Prepare the JSON structure
        data = {
            'text': text_content,
            'links': links,
            'images': image_links,
            'tables': tables_data
        }
        
        return json.dumps(data, ensure_ascii=False, indent=4)




