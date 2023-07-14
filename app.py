from flask import Flask, render_template
import re

app = Flask(__name__)

def parse_nginx_logs(log_file):
    pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"'

    logs = []
    with open(log_file, 'r') as f:
        for line in f:
            match = re.match(pattern, line)
            if match:
                log = {
                    'ip': match.group(1),
                    'timestamp': match.group(2),
                    'request': match.group(3),
                    'status': match.group(4),
                    'size': match.group(5),
                    'referrer': match.group(6),
                    'user_agent': match.group(7)
                }
                logs.append(log)
    return logs

@app.route('/')
def index():
    logs = parse_nginx_logs('/var/log/nginx/access.log')
    return render_template('index.html', logs=logs)

if __name__ == '__main__':
    app.run()
