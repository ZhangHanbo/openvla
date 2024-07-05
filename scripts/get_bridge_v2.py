import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

dataset_root = "/data/home/hanbo/datasets/bridge_orig"

# Define the URL
url = "https://rail.eecs.berkeley.edu/datasets/bridge_release/data/tfds/bridge_dataset/1.0.0/"

# Fetch the HTML content of the web page
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful
webpage_html = response.text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(webpage_html, 'html.parser')

# Extract all hyperlinks
links = soup.find_all('a', href=True)

# Directory to save downloaded files
save_dir = dataset_root
os.makedirs(save_dir, exist_ok=True)

# List of names to filter out
exclude_names = ["Name", "Last modified", "Size", "Description", "Parent Directory"]

for link in links:
    link_text = link.get_text(strip=True)
    if link_text in exclude_names:
        continue

    href = link['href']
    full_url = urljoin(url, href)
    try:
        os.system(f"wget -c -P {save_dir} {full_url}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {full_url}: {e}")