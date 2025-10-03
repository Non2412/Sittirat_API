from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'Sittirat Tourism API - Working with Flask!',
        'status': 'success',
        'version': '1.0.0',
        'framework': 'Flask'
    })

@app.route('/api/')
def api_root():
    return jsonify({
        'message': 'API Root',
        'endpoints': {
            'home': '/',
            'api': '/api/',
            'health': '/health'
        }
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)