#!/usr/bin/env python3
"""
Simple web server for Genomic Twin platform
Provides both Streamlit app and basic web endpoints
"""

import os
import sys
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import subprocess

class GenomicTwinHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        # Health check endpoint
        if parsed_path.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'healthy',
                'platform': 'Genomic Twin - Adaptive Genomic Insights',
                'version': '1.0.0'
            }
            self.wfile.write(json.dumps(response).encode())
            return
        
        # API status endpoint
        elif parsed_path.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'api_status': 'operational',
                'endpoints': [
                    '/health',
                    '/api/status',
                    '/lineage',
                    '/'
                ],
                'services': {
                    'genomic_analysis': 'available',
                    'clinical_trials': 'available',
                    'ai_chatbot': 'available',
                    'digital_twin': 'available'
                }
            }
            self.wfile.write(json.dumps(response).encode())
            return
        
        # Serve lineage visualizer
        elif parsed_path.path == '/lineage':
            try:
                with open('lineage_visualizer.html', 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f.read())
                return
            except FileNotFoundError:
                pass
        
        # Default behavior for other paths
        super().do_GET()

def run_server():
    """Run the simple web server"""
    port = int(os.environ.get('PORT', 8000))
    server_address = ('', port)
    httpd = HTTPServer(server_address, GenomicTwinHandler)
    print(f"Genomic Twin server running on port {port}")
    print(f"Visit: http://localhost:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    # Check if we should run streamlit instead
    if len(sys.argv) > 1 and sys.argv[1] == '--streamlit':
        os.system('streamlit run app.py')
    else:
        run_server()