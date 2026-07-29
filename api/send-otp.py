from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/send-email', methods=['GET'])
def send_email_otp():
    target_email = request.args.get('email')
    
    if not target_email:
        return jsonify({
            "success": False,
            "error": "Email parameter missing! Usage: /send-email?email=user@example.com"
        }), 400

    target_url = "https://ffmconnect.live.gop.garenanow.com/game/account_security/swap:send_otp"
    
    headers = {
        "User-Agent": "GarenaMSDK/4.0.19P9 (Android 9; en; US)",
        "Content-Type": "application/json",
        "Connection": "keep-alive"
    }
    
    payload = {
        "email": target_email,
        "channel": "email"
    }

    try:
        response = requests.post(target_url, json=payload, headers=headers, timeout=10)
        
        try:
            resp_data = response.json()
        except Exception:
            resp_data = response.text

        return jsonify({
            "success": response.status_code == 200,
            "http_code": response.status_code,
            "target_email": target_email,
            "response": resp_data
        }), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({
            "success": False,
            "error": "Failed to connect to target server",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
