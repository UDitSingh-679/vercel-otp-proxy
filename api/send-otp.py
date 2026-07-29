from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import urllib.request
import urllib.error

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Parse Query Parameters (?email=...)
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        email_list = query_params.get('email', [])
        target_email = email_list[0] if email_list else None

        if not target_email:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response_data = {
                "success": False,
                "error": "Email parameter missing! Usage: /send-email?email=user@example.com"
            }
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            return

        # 2. Target Endpoint Setup
        target_url = "https://ffmconnect.live.gop.garenanow.com/game/account_security/swap:send_otp"
        
        payload = json.dumps({
            "email": target_email,
            "channel": "email"
        }).encode('utf-8')

        headers = {
            "User-Agent": "GarenaMSDK/4.0.19P9 (Android 9; en; US)",
            "Content-Type": "application/json",
            "Connection": "keep-alive"
        }

        # 3. Request Forwarding using urllib
        req = urllib.request.Request(target_url, data=payload, headers=headers, method='POST')

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                status_code = resp.getcode()
                resp_body = resp.read().decode('utf-8')
                try:
                    resp_json = json.loads(resp_body)
                except Exception:
                    resp_json = resp_body

                self.send_response(status_code)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                res_output = {
                    "success": status_code == 200,
                    "http_code": status_code,
                    "target_email": target_email,
                    "response": resp_json
                }
                self.wfile.write(json.dumps(res_output).encode('utf-8'))

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            res_output = {
                "success": False,
                "http_code": e.code,
                "target_email": target_email,
                "error_details": error_body
            }
            self.wfile.write(json.dumps(res_output).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            res_output = {
                "success": False,
                "error": "Failed to connect to target server",
                "details": str(e)
            }
            self.wfile.write(json.dumps(res_output).encode('utf-8'))