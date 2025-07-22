import requests
import os
from datetime import datetime
from bs4 import BeautifulSoup
import json

MOCK_SITES = [
    'http://localhost:5001',
    'http://localhost:5002',
    'http://localhost:5003',
    'http://localhost:5004',
    'http://localhost:5005',
]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../data/run_logs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_site1(soup):
    return {
        'product': soup.find('h1').text,
        'price': soup.find('div', class_='price').text,
        'description': soup.find('div', class_='desc').text,
        'features': [li.text for li in soup.select('.features ul li')],
        'review': soup.find('div', class_='review').text
    }

def extract_site2(soup):
    return {
        'headline': soup.find('h1').text,
        'author_and_date': soup.find('div', class_='meta').text,
        'body': soup.find('div', class_='body').text,
        'tags': soup.find('div', class_='tags').text.replace('Tags:', '').strip()
    }

def extract_site3(soup):
    table = soup.find('table')
    rows = table.find_all('tr')[1:] if table else []
    hourly = [{
        'hour': row.find_all('td')[0].text,
        'temperature': row.find_all('td')[1].text
    } for row in rows]
    return {
        'city': soup.find('h1').text.replace('Weather in ', ''),
        'temperature': soup.find('div', class_='temp').text,
        'forecast': soup.find('div', class_='forecast').text,
        'hourly': hourly
    }

def extract_site4(soup):
    table = soup.find('table')
    rows = table.find_all('tr')[1:] if table else []
    recent_prices = [{
        'day': row.find_all('td')[0].text,
        'price': row.find_all('td')[1].text
    } for row in rows]
    return {
        'company_and_ticker': soup.find('h1').text,
        'price': soup.find('div', class_='price').text,
        'analysis': soup.find('div', class_='analysis').text,
        'recent_prices': recent_prices
    }

def extract_site5(soup):
    return {
        'event': soup.find('h1').text,
        'meta': soup.find('div', class_='meta').text,
        'description': soup.find('div', class_='desc').text,
        'speakers': [li.text for li in soup.select('.speakers ul li')]
    }

EXTRACTORS = [extract_site1, extract_site2, extract_site3, extract_site4, extract_site5]

def scrape_and_save():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    all_data = {}
    for idx, (url, extractor) in enumerate(zip(MOCK_SITES, EXTRACTORS), 1):
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            data = extractor(soup)
            all_data[f'site{idx}'] = data
            print(f'Extracted data from {url}')
        except Exception as e:
            print(f'Error scraping {url}: {e}')
            all_data[f'site{idx}'] = {'error': str(e)}
    filename = f'sites_{timestamp}.json'
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    print(f'Saved extracted data to {filepath}')

if __name__ == '__main__':
    scrape_and_save()
