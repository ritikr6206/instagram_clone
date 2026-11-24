"""
Instagram Login Clone - Python Backend Server
Uses only Python standard library (no pip install needed!)
"""

import http.server
import json
import os
import socketserver

PORT = int(os.environ.get('PORT', 3000))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'users.json')
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')

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


class MyHandler(http.server.BaseHTTPRequestHandler):
    """Custom handler that serves static files and handles API routes."""

    # MIME types for static files
    MIME_TYPES = {
        '.html': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.json': 'application/json',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.svg': 'image/svg+xml',
        '.ico': 'image/x-icon',
    }

    def do_GET(self):
        # API: Get all users
        if self.path == '/api/users':
            self.send_json(get_users())
            return

        # Route: /admin -> serve admin.html
        if self.path == '/admin' or self.path == '/admin/':
            self.serve_file('admin.html')
            return

        # Route: / -> serve index.html
        path = self.path.strip('/')
        if path == '':
            path = 'index.html'

        self.serve_file(path)

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

    def serve_file(self, filename):
        """Serve a static file from the public directory."""
        filepath = os.path.join(PUBLIC_DIR, filename)

        if not os.path.isfile(filepath):
            self.send_error(404, 'Not Found')
            return

        ext = os.path.splitext(filename)[1].lower()
        mime_type = self.MIME_TYPES.get(ext, 'application/octet-stream')

        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', mime_type)
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, str(e))

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

        # New user - auto-register
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

    def send_json(self, data):
        response = json.dumps(data).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(response))
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]}")


if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"")
        print(f"  Instagram Login Clone Server Running!")
        print(f"  Login Page  -> http://localhost:{PORT}")
        print(f"  Admin Panel -> http://localhost:{PORT}/admin")
        print(f"")
        httpd.serve_forever()
