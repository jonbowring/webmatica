import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Global variables

# Map the URL to be scraped
dev_mode = True
if dev_mode:
    scrape_url = 'https://www.abc.net.au/news/2025-10-22/climate-trigger-formally-ruled-out-of-environment-laws/105919546'

url = scrape_url

# Function for converting the scraped response into a format readable by our agent
def element_to_dict(element):
    if element.name is None:
        text = element.strip()
        if text:
            return text
        else:
            return None
    
    result = {}
    result['tag'] = element.name
    children = []
    for child in element.children:
        child_dict = element_to_dict(child)
        if child_dict is not None:
            children.append(child_dict)
    
    if children:
        result['children'] = children
    
    return result

# Scrape the URL
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get(url)
content = driver.page_source
driver.quit()

# Parse the response
soup = BeautifulSoup(content, 'html.parser')
root = soup.body or soup  # if no body, use soup root

# Convert to scraped pages dict
result = []
for element in root.children:
    if element.name is not None:
        dict_rep = element_to_dict(element)
        result.append(dict_rep)

# If in development print the response to console
if dev_mode:
    print(json.dumps(result, indent=4))

# Return the result
response = result