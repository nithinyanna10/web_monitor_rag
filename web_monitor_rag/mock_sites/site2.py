from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

ARTICLES = [
    {
        "headline": "Breakthrough in Renewable Energy Announced",
        "author": "Jane Smith",
        "body": "Scientists at the National Institute of Clean Energy have developed a new solar panel that is 50% more efficient than current models. This breakthrough could revolutionize the energy industry and significantly reduce carbon emissions worldwide.",
        "tags": ["Energy", "Science", "Innovation"]
    },
    {
        "headline": "City Council Approves New Park Downtown",
        "author": "Michael Lee",
        "body": "The city council has unanimously approved the construction of a new public park in the downtown area. The park will feature walking trails, playgrounds, and a community garden, providing much-needed green space for residents.",
        "tags": ["Local", "Community", "Environment"]
    },
    {
        "headline": "Tech Company Releases Next-Gen Smartphone",
        "author": "Alex Johnson",
        "body": "Tech giant FutureMobile has unveiled its latest smartphone, featuring an AI-powered camera, foldable display, and all-day battery life. Early reviews praise its innovative design and powerful performance.",
        "tags": ["Technology", "Gadgets", "AI"]
    }
]

@app.route('/')
def index():
    article = random.choice(ARTICLES)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    tags_html = ', '.join(article['tags'])
    html = f'''
    <html>
    <head>
        <title>{article['headline']} - Site 2 News</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #f0f4f8; margin: 0; padding: 0; }}
            .container {{ max-width: 700px; margin: 60px auto; background: #fff; border-radius: 10px; box-shadow: 0 2px 8px #bbb; padding: 30px; }}
            h1 {{ color: #e67e22; }}
            .meta {{ color: #888; font-size: 0.95em; margin-bottom: 20px; }}
            .body {{ margin: 20px 0; font-size: 1.15em; }}
            .tags {{ margin-top: 20px; color: #1976d2; }}
            .timestamp {{ color: #888; font-size: 0.9em; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{article['headline']}</h1>
            <div class="meta">By {article['author']} | {timestamp}</div>
            <div class="body">{article['body']}</div>
            <div class="tags"><strong>Tags:</strong> {tags_html}</div>
            <div class="timestamp">Last updated: {timestamp}</div>
        </div>
    </body>
    </html>
    '''
    return html

@app.route('/api')
def api():
    article = random.choice(ARTICLES)
    return jsonify({
        'site': 'site2',
        'headline': article['headline'],
        'author': article['author'],
        'body': article['body'],
        'tags': article['tags'],
        'timestamp': time.time()
    })

if __name__ == '__main__':
    app.run(port=5002)
