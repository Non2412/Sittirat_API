import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading

# Global health status
server_ready = True
start_time = time.time()

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Always respond quickly
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            
            uptime = int(time.time() - start_time)
            
            # Different responses for different paths
            if self.path == '/health' or self.path == '/health/':
                response = {
                    'status': 'healthy',
                    'uptime': f'{uptime}s',
                    'timestamp': int(time.time())
                }
            elif self.path == '/api' or self.path == '/api/':
                response = {
                    'message': 'Sittirat Tourism API',
                    'status': 'working',
                    'uptime': f'{uptime}s',
                    'endpoints': ['/', '/api/', '/health']
                }
            else:  # Default for / and other paths
                response = {
                    'message': 'Hello Railway!',
                    'status': 'working',
                    'path': self.path,
                    'port': os.environ.get('PORT', '8080'),
                    'uptime': f'{uptime}s',
                    'endpoints': {
                        'home': '/',
                        'api': '/api/', 
                        'health': '/health'
                    }
                }
                
            self.wfile.write(json.dumps(response, indent=2).encode())
            print(f"✅ {self.path} - OK")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            self.send_response(500)
            self.end_headers()

    def do_HEAD(self):
        # Quick response for health checks
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def log_message(self, format, *args):
        # Minimal logging
        pass

def keep_alive():
    """Keep the process alive"""
    while True:
        time.sleep(30)
        print(f"💓 Heartbeat - uptime: {int(time.time() - start_time)}s")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    
    print(f"🚀 Starting Sittirat API on 0.0.0.0:{port}")
    
    # Start heartbeat thread
    heartbeat = threading.Thread(target=keep_alive, daemon=True)
    heartbeat.start()
    
    try:
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        server.timeout = 1  # Quick timeout
        
        print(f"✅ Server ready on port {port}")
        print(f"🏥 Health check: /health")
        print(f"🌐 API ready: /api")
        print("🔄 Server is stable and ready...")
        
        server.serve_forever()
        
    except Exception as e:
        print(f"❌ Failed to start: {e}")
        import sys
        sys.exit(1)