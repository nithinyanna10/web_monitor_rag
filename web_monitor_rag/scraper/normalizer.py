import json
import sys
import os
import re

def normalize_price(price):
    if isinstance(price, str):
        return float(re.sub(r'[^0-9.]', '', price))
    return price

def normalize_text(text):
    return text.strip() if isinstance(text, str) else text

def normalize_site1(data):
    return {
        'product': normalize_text(data.get('product', '')),
        'price': normalize_price(data.get('price', '')),
        'description': normalize_text(data.get('description', '')),
        'features': [normalize_text(f) for f in data.get('features', [])],
        'review': normalize_text(data.get('review', '')),
    }

def normalize_site2(data):
    return {
        'headline': normalize_text(data.get('headline', '')),
        'author_and_date': normalize_text(data.get('author_and_date', '')),
        'body': normalize_text(data.get('body', '')),
        'tags': [normalize_text(tag) for tag in data.get('tags', '').split(',') if tag.strip()],
    }

def normalize_site3(data):
    return {
        'city': normalize_text(data.get('city', '')),
        'temperature': normalize_text(data.get('temperature', '')),
        'forecast': normalize_text(data.get('forecast', '')),
        'hourly': [
            {
                'hour': normalize_text(h.get('hour', '')),
                'temperature': normalize_text(h.get('temperature', '')),
            } for h in data.get('hourly', [])
        ]
    }

def normalize_site4(data):
    return {
        'company_and_ticker': normalize_text(data.get('company_and_ticker', '')),
        'price': normalize_price(data.get('price', '')),
        'analysis': normalize_text(data.get('analysis', '')),
        'recent_prices': [
            {
                'day': normalize_text(p.get('day', '')),
                'price': normalize_price(p.get('price', '')),
            } for p in data.get('recent_prices', [])
        ]
    }

def normalize_site5(data):
    return {
        'event': normalize_text(data.get('event', '')),
        'meta': normalize_text(data.get('meta', '')),
        'description': normalize_text(data.get('description', '')),
        'speakers': [normalize_text(s) for s in data.get('speakers', [])],
    }

NORMALIZERS = [normalize_site1, normalize_site2, normalize_site3, normalize_site4, normalize_site5]

SITE_KEYS = ['site1', 'site2', 'site3', 'site4', 'site5']

def main(input_path, output_path=None):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    normalized = {}
    for key, normalizer in zip(SITE_KEYS, NORMALIZERS):
        if key in data:
            normalized[key] = normalizer(data[key])
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(normalized, f, indent=2, ensure_ascii=False)
        print(f"Normalized data written to {output_path}")
    else:
        print(json.dumps(normalized, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python normalizer.py <input_json> [output_json]")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    main(input_path, output_path)
