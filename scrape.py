import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import json

def fetch_article_content(article_url):
    """Fetch and return the content of the given article."""
    try:
        response = requests.get(article_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            content_sections = soup.find_all('p')  # Potentially adjust based on actual content containers
            content = '\n'.join(section.get_text(strip=True) for section in content_sections)
            return content
        else:
            print(f"Failed to fetch article content: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching article content: {e}")
        return None

def get_article_links(title_url):
    """Retrieve all article links from the title detail page."""
    response = requests.get(title_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        article_links = []
        for link in soup.find_all('a', class_='stat'):  # Make sure this correctly matches the class of relevant <a> tags
            href = link.get('href')
            if href.startswith('/'):
                href = href[1:]  # Removing the leading slash if present
            full_url = urljoin(title_url, href)  # Ensure full URL formation
            article_name = link.text.strip()
            map_title = title_url.split('=')[-1]
            article_links.append((full_url, article_name, map_title))
        return article_links
    return []

def save_article_content(article_name, title, content):
    """Save the article content to a text file."""
    directory = os.path.join('files', f'Title_{title}')
    os.makedirs(directory, exist_ok=True)
    filename = f"{article_name.replace(' ', '_').replace('/', '_')}.txt"  # Replace slashes to avoid path issues
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(f"Title: {title}\nArticle: {article_name}\n\nContent:\n{content}")
"""
def save_article_content(article_name, title, content):
    directory = os.path.join('files', f'Title_{title}')
    os.makedirs(directory, exist_ok=True)
    filename = f"{article_name.replace(' ', '_').replace('/', '_')}.json"  # Replace slashes to avoid path issues
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump({'title': title, 'article': article_name, 'content': content}, file, ensure_ascii=False, indent=4)
"""
# Ensure the base URL is correctly used
BASE_URL = 'https://www.azleg.gov'
DETAILS_BASE_URL = f'{BASE_URL}/arsDetail/?title='

# Iterate through each title
for title_number in range(1, 50):  # Assuming Titles 1 to 49 exist
    title_url = f"{DETAILS_BASE_URL}{title_number}"
    articles = get_article_links(title_url)
    
    for article_url, article_name, title in articles:
        content = fetch_article_content(article_url)
        if content:
            save_article_content(article_name, title, content)
        else:
            print(f"No content retrieved for {article_name}.")

    # Remove the break in the loop for full operation across all titles
    break