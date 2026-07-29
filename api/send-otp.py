from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests, json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        target_email = params.get('email', [None])[0]

        if not target_email:
            self.send_json(400, {"success": False, "error": "email required"})
            return

        target_url = "https://ffmconnect.live.gop.garenanow.com/game/account_security/swap:send_otp"
        headers = {
            "User-Agent": "GarenaMSDK/4.0.19P9 (Android 9; en; US)",
            "Content-Type": "application/json"
        }
        payload = {"email": target_email, "channel": "email"}

        try:
            resp = requests.post(target_url, json=payload, headers=headers, timeout=10)
            data = resp.json() if resp.text else resp.text
            self.send_json(resp.status_code, {
                "success": resp.status_code == 200,
                "http_code": resp.status_code,
                "target_email": target_email,
                "response": data
            })
        except Exception as e:
            self.send_json(500, {"success": False, "error": str(e)})

    def send_json(self, code, data):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
