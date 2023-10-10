import requests
from bs4 import BeautifulSoup
import re

SITEMAP_URL = "https://www.akitaonrails.com/sitemap.xml"

def fetch_sitemap(sitemap_url):
    response = requests.get(sitemap_url)
    return BeautifulSoup(response.content, 'xml')

def extract_article_urls_from_sitemap(soup):
    # Extract article URLs only
    pattern = re.compile(r'^http://www\.akitaonrails\.com/\d{4}/\d{2}/\d{2}/.*$')
    return [loc_tag.text for loc_tag in soup.find_all('loc') if pattern.match(loc_tag.text)]

def construct_filename_from_url(url):
    parts = url.split('/')
    # Extract the date and the rest of the URL parts
    date = '-'.join(parts[3:6])  # Extract the date components (year, month, day)
    slug = parts[6]  # The rest of the URL after the date
    return f"{date} {slug}.txt"

def get_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    excerpt = soup.find('div', class_='excerpt')
    text = soup.find('div', class_='text')
    
    combined_text = ""
    
    # Append excerpt text if it exists
    if excerpt:
        combined_text += excerpt.get_text() + '\n'
    
    # Append text content if it exists
    if text:
        combined_text += text.get_text() + '\n'
    
    # Save combined text content
    filename = construct_filename_from_url(url)
    with open(filename, 'w') as file:
        file.write(combined_text)

def process_articles(article_urls):
    for url in article_urls:
        print('> Processing article: ' + url)
        get_article_content(url)

def main():
    soup = fetch_sitemap(SITEMAP_URL)
    article_urls = extract_article_urls_from_sitemap(soup)
    process_articles(article_urls)

if __name__ == '__main__':
    main()
