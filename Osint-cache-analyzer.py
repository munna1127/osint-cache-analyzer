import os
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import unquote
import time
import urllib.parse
import socket
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys
import subprocess

print("""
====================================================================
        OSINT METADATA EXTRACTION & RESIDUAL CACHE ANALYZER
====================================================================
[Description]: Research tool for analyzing public CDN data retention.
[Author]: Aryan Kacher
[Disclaimer]: For Educational and Defensive Security Research Only.
====================================================================
""")

def get_headers():
    return {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-GB,en;q=0.9',
        'dpr': '1',
        'priority': 'u=0, i',
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36'
    }

def fetch_instagram_profile(username):
    url = f'https://www.instagram.com/{username}/'
    headers = get_headers()
    print(f"[i] Sending unauthenticated request to target profile: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            print(f"[-] Target endpoint returned HTTP Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"[-] Connection Error: {str(e)}")
        return None

def extract_timeline_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    script_tags = soup.find_all('script', {'type': 'application/json'})
    print(f"[i] Scanning {len(script_tags)} JSON blocks for polaris metadata nodes...")
    
    for script in script_tags:
        content = script.string
        if content and 'polaris_timeline_connection' in content:
            try:
                data = json.loads(content)
                return data
            except json.JSONDecodeError:
                continue
    return None

def extract_highest_resolution_urls(obj, urls=None, post_id=None):
    if urls is None: 
        urls = {}
    try:
        if isinstance(obj, dict):
            if 'pk' in obj: 
                post_id = obj['pk']
            if 'image_versions2' in obj:
                candidates = obj['image_versions2'].get('candidates', [])
                if candidates:
                    highest_res = max(candidates, key=lambda x: x.get('width', 0) * x.get('height', 0))
                    url = highest_res.get('url', '')
                    if url and post_id and post_id not in urls:
                        urls[post_id] = unquote(url.encode('utf-8').decode('unicode_escape'))
            for value in obj.values():
                extract_highest_resolution_urls(value, urls, post_id)
        elif isinstance(obj, list):
            for item in obj:
                extract_highest_resolution_urls(item, urls, post_id)
    except Exception:
        pass
    return urls

def generate_unsuccessful_html(username):
    return f"""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Audit Status: Restricted</title>
        <style>
            body {{ background-color: #121212; color: #ff5555; text-align: center; font-family: Arial, sans-serif; padding-top: 50px; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ff5555; border-radius: 8px; background-color: #1e1e1e; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>[-] Data Extraction Audit Unsuccessful</h2>
            <p>No public endpoints or residual cached media arrays were exposed for account: @{username}</p>
        </div>
    </body>
    </html>"""

def save_urls_to_file(image_urls, username, successful=True):
    if not successful:
        return generate_unsuccessful_html(username)
        
    html_template = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OSINT Extraction Audit Report: @{username}</title>
        <style>
            body {{
                background-color: #121212;
                color: #ffffff;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 1px solid #333;
            }}
            .header h1 {{
                color: #00ff66;
                margin-bottom: 5px;
            }}
            .header p {{
                color: #aaa;
                margin: 0;
            }}
            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                gap: 20px;
                padding: 10px;
            }}
            .card {{
                background-color: #1e1e1e;
                border: 1px solid #333;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            }}
            .card img {{
                width: 100%;
                height: 250px;
                object-fit: cover;
                display: block;
            }}
            .card-body {{
                padding: 12px;
                font-size: 14px;
                border-top: 1px solid #333;
                background-color: #1a1a1a;
            }}
            .card-body strong {{
                color: #00ff66;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>[+] OSINT Audit Control Dashboard</h1>
            <p>Target Profile: @{username} | Mapped Residual Media Nodes</p>
            <p style="font-size: 12px; color: #555; margin-top: 10px;">Analyst: Aryan Kacher</p>
        </div>
        <div class="grid">
    """
    for pk, url in image_urls.items():
        html_template += f"""
            <div class="card">
                <img src="{url}" alt="Exposed Post Artifact" referrerpolicy="no-referrer">
                <div class="card-body">
                    <strong>Node ID (PK):</strong> {pk}
                </div>
            </div>
        """
    html_template += """
        </div>
    </body>
    </html>
    """
    return html_template

class CustomHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

def run_server(html_content):
    class DynamicHandler(CustomHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
            
    server = HTTPServer(('localhost', 8080), DynamicHandler)
    server.serve_forever()

def start_local_server(html_content):
    t = threading.Thread(target=run_server, args=(html_content,))
    t.daemon = True
    t.start()
    return t

def main():
    username = input("[?] Enter Instagram username to audit: ").strip()
    if not username:
        print("[-] Target username cannot be empty.")
        return
        
    html_response = fetch_instagram_profile(username)
    if not html_response:
        print("[-] Failed to retrieve data from endpoint.")
        return
        
    timeline_data = extract_timeline_data(html_response)
    if not timeline_data:
        print("[-] No valid JSON metadata arrays detected. Account might be restricted or strictly authenticated.")
        html_content = generate_unsuccessful_html(username)
        start_local_server(html_content)
        print("[*] Local server hosted at http://localhost:8080 to display results page. Press Ctrl+C to terminate.")
        try:
            while True: time.sleep(1)
        except KeyboardInterrupt:
            print("\n[!] Server stopped.")
        return
        
    image_urls = extract_highest_resolution_urls(timeline_data)
    
    if not image_urls:
        print("[-] Verification failed. Metadata structured was present but empty.")
        html_content = generate_unsuccessful_html(username)
        start_local_server(html_content)
        try:
            while True: time.sleep(1)
        except KeyboardInterrupt:
            print("\n[!] Server stopped.")
        return
        
    print(f"\n[+] SUCCESS: Extracted {len(image_urls)} public-facing residual CDN assets!")
    html_content = save_urls_to_file(image_urls, username, successful=True)
    
    print("[*] Launching Local Audit Server at: http://localhost:8080")
    start_local_server(html_content)
    
    try:
        print("[!] Live Server Running. Press Ctrl+C to exit.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Server stopped.")

if __name__ == "__main__":
    main()
