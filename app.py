import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Different responses for different paths
            if self.path == '/health':
                response = {'status': 'healthy', 'uptime': 'ok'}
            elif self.path == '/api/':
                response = {
                    'message': 'Sittirat Tourism API',
                    'status': 'working',
                    'endpoints': ['/', '/api/', '/health']
                }
            else:  # Default for / and other paths
                response = {
                    'message': 'Hello Railway!',
                    'status': 'working',
                    'path': self.path,
                    'port': os.environ.get('PORT', '8080'),
                    'endpoints': {
                        'home': '/',
                        'api': '/api/', 
                        'health': '/health'
                    }
                }
                
            self.wfile.write(json.dumps(response).encode())
            print(f"✅ Served request: {self.path}")
        except Exception as e:
            print(f"❌ Error serving request: {e}")

    def do_HEAD(self):
        # Respond to HEAD requests (health checks)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def log_message(self, format, *args):
        # Log all requests
        print(f"🌐 Request: {format % args}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"🚀 Starting server on 0.0.0.0:{port}")
    
    try:
        server = HTTPServer(('0.0.0.0', port), SimpleHandler)
        print(f"✅ Server successfully started on port {port}")
        print("🔄 Server is ready to accept connections...")
        print("🏥 Health check available at /health")
        server.serve_forever()
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        import sys
        sys.exit(1)