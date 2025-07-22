from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

EVENTS = [
    {
        "name": "Music Concert at Central Park",
        "date": "2024-07-15",
        "location": "Central Park, New York",
        "desc": "Join us for an unforgettable night of live music featuring top artists from around the world. Food trucks and merchandise stalls available.",
        "speakers": ["DJ Sonic", "The Jazz Cats", "MC Melody"]
    },
    {
        "name": "Tech Meetup at Innovation Hub",
        "date": "2024-08-02",
        "location": "Innovation Hub, San Francisco",
        "desc": "A gathering of tech enthusiasts, developers, and entrepreneurs. Keynotes, networking, and hands-on workshops throughout the day.",
        "speakers": ["Elena Torres", "Samir Patel", "Dr. Lin Wei"]
    },
    {
        "name": "Food Festival at City Square",
        "date": "2024-09-10",
        "location": "City Square, Chicago",
        "desc": "Taste culinary delights from over 50 local vendors. Live cooking demos, contests, and family-friendly activities all day long.",
        "speakers": ["Chef Antonio", "Baker Mia", "Grillmaster Lee"]
    }
]

@app.route('/')
def index():
    event = random.choice(EVENTS)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    speakers_html = ''.join(f'<li>{s}</li>' for s in event['speakers'])
    html = f'''
    <html>
    <head>
        <title>{event['name']} - Site 5 Events</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #fffde7; margin: 0; padding: 0; }}
            .container {{ max-width: 600px; margin: 60px auto; background: #fff; border-radius: 10px; box-shadow: 0 2px 8px #ffe082; padding: 30px; }}
            h1 {{ color: #fbc02d; }}
            .meta {{ color: #888; font-size: 0.95em; margin-bottom: 20px; }}
            .desc {{ margin: 20px 0; }}
            .speakers {{ margin: 20px 0; }}
            .timestamp {{ color: #888; font-size: 0.9em; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{event['name']}</h1>
            <div class="meta">{event['date']} | {event['location']}</div>
            <div class="desc">{event['desc']}</div>
            <div class="speakers">
                <strong>Speakers/Performers:</strong>
                <ul>{speakers_html}</ul>
            </div>
            <div class="timestamp">Last updated: {timestamp}</div>
        </div>
    </body>
    </html>
    '''
    return html

@app.route('/api')
def api():
    event = random.choice(EVENTS)
    return jsonify({
        'site': 'site5',
        'name': event['name'],
        'date': event['date'],
        'location': event['location'],
        'description': event['desc'],
        'speakers': event['speakers'],
        'timestamp': time.time()
    })

if __name__ == '__main__':
    app.run(port=5005)
