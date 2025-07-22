from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

CITIES = ["New York", "London", "Tokyo", "Sydney", "Paris"]
FORECASTS = [
    "Sunny with a few clouds. Perfect weather for outdoor activities.",
    "Light rain expected in the afternoon. Carry an umbrella!",
    "Cloudy with a chance of thunderstorms in the evening.",
    "Clear skies throughout the day. Mild temperatures.",
    "Heavy showers in the morning, clearing up by late afternoon."
]

@app.route('/')
def index():
    city = random.choice(CITIES)
    temp = round(random.uniform(-10, 35), 1)
    forecast = random.choice(FORECASTS)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    hours = [f"{h}:00" for h in range(8, 21, 2)]
    temps = [round(temp + random.uniform(-3, 3), 1) for _ in hours]
    table_rows = ''.join(f'<tr><td>{h}</td><td>{t}&deg;C</td></tr>' for h, t in zip(hours, temps))
    html = f'''
    <html>
    <head>
        <title>Weather in {city} - Site 3</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #e3f2fd; margin: 0; padding: 0; }}
            .container {{ max-width: 500px; margin: 60px auto; background: #fff; border-radius: 10px; box-shadow: 0 2px 8px #90caf9; padding: 30px; }}
            h1 {{ color: #1565c0; }}
            .temp {{ font-size: 2em; color: #ef5350; }}
            .forecast {{ margin: 20px 0; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #bbb; padding: 8px; text-align: center; }}
            th {{ background: #bbdefb; }}
            .timestamp {{ color: #888; font-size: 0.9em; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Weather in {city}</h1>
            <div class="temp">{temp}&deg;C</div>
            <div class="forecast">{forecast}</div>
            <table>
                <tr><th>Hour</th><th>Temperature</th></tr>
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
    city = random.choice(CITIES)
    temp = round(random.uniform(-10, 35), 1)
    forecast = random.choice(FORECASTS)
    hours = [f"{h}:00" for h in range(8, 21, 2)]
    temps = [round(temp + random.uniform(-3, 3), 1) for _ in hours]
    hourly = dict(zip(hours, temps))
    return jsonify({
        'site': 'site3',
        'city': city,
        'temperature': temp,
        'forecast': forecast,
        'hourly': hourly,
        'timestamp': time.time()
    })

if __name__ == '__main__':
    app.run(port=5003)
