from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

STOCKS = [
    {
        "company": "Apple Inc.",
        "ticker": "AAPL",
        "analysis": "Apple's stock remains resilient amid market volatility, driven by strong iPhone sales and expanding services revenue. Analysts predict continued growth in the next quarter."
    },
    {
        "company": "Tesla, Inc.",
        "ticker": "TSLA",
        "analysis": "Tesla's innovative approach to electric vehicles and energy storage keeps it at the forefront of the industry. Recent developments in autonomous driving technology have boosted investor confidence."
    },
    {
        "company": "Amazon.com, Inc.",
        "ticker": "AMZN",
        "analysis": "Amazon's dominance in e-commerce and cloud computing continues to drive revenue growth. The company's focus on logistics and AI integration sets it apart from competitors."
    }
]

@app.route('/')
def index():
    stock = random.choice(STOCKS)
    price = round(random.uniform(100, 2000), 2)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    prices = [round(price + random.uniform(-10, 10), 2) for _ in range(5)]
    table_rows = ''.join(f'<tr><td>Day {i+1}</td><td>${p}</td></tr>' for i, p in enumerate(prices))
    html = f'''
    <html>
    <head>
        <title>{stock['company']} ({stock['ticker']}) - Site 4 Stocks</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #f3e5f5; margin: 0; padding: 0; }}
            .container {{ max-width: 600px; margin: 60px auto; background: #fff; border-radius: 10px; box-shadow: 0 2px 8px #ce93d8; padding: 30px; }}
            h1 {{ color: #8e24aa; }}
            .ticker {{ font-size: 1.2em; color: #3949ab; }}
            .price {{ font-size: 2em; color: #43a047; }}
            .analysis {{ margin: 20px 0; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #bbb; padding: 8px; text-align: center; }}
            th {{ background: #e1bee7; }}
            .timestamp {{ color: #888; font-size: 0.9em; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{stock['company']} <span class="ticker">({stock['ticker']})</span></h1>
            <div class="price">${price}</div>
            <div class="analysis">{stock['analysis']}</div>
            <table>
                <tr><th>Day</th><th>Price</th></tr>
                {table_rows}
            </table>
            <div class="timestamp">Last updated: {timestamp}</div>
        </div>
    </body>
    </html>
    '''
    return html

@app.route('/api')
def api():
    stock = random.choice(STOCKS)
    price = round(random.uniform(100, 2000), 2)
    prices = [round(price + random.uniform(-10, 10), 2) for _ in range(5)]
    return jsonify({
        'site': 'site4',
        'company': stock['company'],
        'ticker': stock['ticker'],
        'price': price,
        'analysis': stock['analysis'],
        'recent_prices': prices,
        'timestamp': time.time()
    })

if __name__ == '__main__':
    app.run(port=5004)
