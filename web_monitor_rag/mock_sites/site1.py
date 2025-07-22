from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

PRODUCTS = [
    {
        "name": "Smartphone X200",
        "desc": "The Smartphone X200 features a stunning 6.5-inch OLED display, 128GB storage, and a powerful octa-core processor. Perfect for multitasking and gaming.",
        "features": ["6.5-inch OLED Display", "128GB Storage", "Octa-core Processor", "Triple-lens Camera", "5G Connectivity"],
        "review": "An outstanding device with exceptional battery life and a crystal-clear display. Highly recommended for tech enthusiasts!"
    },
    {
        "name": "UltraBook Pro 15",
        "desc": "UltraBook Pro 15 is a lightweight laptop with a 15-inch Retina display, 16GB RAM, and 1TB SSD. Ideal for professionals on the go.",
        "features": ["15-inch Retina Display", "16GB RAM", "1TB SSD", "Aluminum Body", "Thunderbolt 4"],
        "review": "Sleek design and blazing-fast performance. The best choice for productivity and travel."
    },
    {
        "name": "NoiseCancel 700 Headphones",
        "desc": "Experience immersive sound with NoiseCancel 700. Active noise cancellation, 30-hour battery, and comfortable fit.",
        "features": ["Active Noise Cancellation", "30-hour Battery", "Bluetooth 5.2", "Touch Controls", "Lightweight Design"],
        "review": "Superb sound quality and comfort. Blocks out all distractions."
    }
]

@app.route('/')
def index():
    product = random.choice(PRODUCTS)
    price = round(random.uniform(199, 1299), 2)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    features_html = ''.join(f'<li>{f}</li>' for f in product['features'])
    html = f'''
    <html>
    <head>
        <title>{product['name']} - Site 1 Product Page</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #f7f7f7; margin: 0; padding: 0; }}
            .container {{ max-width: 600px; margin: 60px auto; background: #fff; border-radius: 10px; box-shadow: 0 2px 8px #ccc; padding: 30px; }}
            h1 {{ color: #2a7ae2; }}
            .price {{ font-size: 2em; color: #27ae60; }}
            .desc {{ margin: 20px 0; }}
            .features {{ margin: 20px 0; }}
            .review {{ background: #f1f8e9; padding: 15px; border-radius: 6px; margin-top: 20px; font-style: italic; }}
            .timestamp {{ color: #888; font-size: 0.9em; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{product['name']}</h1>
            <div class="price">${price}</div>
            <div class="desc">{product['desc']}</div>
            <div class="features">
                <strong>Key Features:</strong>
                <ul>{features_html}</ul>
            </div>
            <div class="review">"{product['review']}"</div>
            <div class="timestamp">Last updated: {timestamp}</div>
        </div>
    </body>
    </html>
    '''
    return html

@app.route('/api')
def api():
    product = random.choice(PRODUCTS)
    price = round(random.uniform(199, 1299), 2)
    return jsonify({
        'site': 'site1',
        'product': product['name'],
        'description': product['desc'],
        'features': product['features'],
        'review': product['review'],
        'price': price,
        'timestamp': time.time()
    })

if __name__ == '__main__':
    app.run(port=5001)
