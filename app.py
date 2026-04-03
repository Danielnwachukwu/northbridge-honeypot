from flask import Flask, request, render_template_string
import datetime
import json
import requests
from dotenv import load_dotenv
import os

# 🔐 LOAD ENV VARIABLES
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = "6595994168"

app = Flask(__name__)

ip_attempts = {}

# 💎 LOGIN PAGE
login_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Northbridge Fintech - Secure Login</title>
</head>
<body style="background:#0f172a;color:white;text-align:center;margin-top:100px;">
    <h1>NORTHBRIDGE FINTECH</h1>
    <h2>Secure Access Portal</h2>

    <form method="POST">
        <input name="username" placeholder="Username"><br><br>
        <input type="password" name="password" placeholder="Password"><br><br>
        <button>Login</button>
    </form>

    {% if error %}
        <p style="color:red;">{{ error }}</p>
    {% endif %}
</body>
</html>
"""

# 🔍 DETECTION
def detect_attack(username, password):
    combined = f"{username} {password}".lower()

    patterns = [
        "' or", '" or', "or 1=1", "or '1'='1",
        "--", "union select", "drop table",
        "information_schema"
    ]

    for p in patterns:
        if p in combined:
            return "SQL Injection"

    return "Normal"

# 🧠 THREAT LEVEL
def threat_level(attack, attempts):
    if attack == "SQL Injection":
        return "High"
    elif attack == "Brute Force":
        return "Medium"
    return "Low"

# 🌍 GEOIP (DEMO IP)
def get_ip_info():
    ip = "8.8.8.8"
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}")
        data = r.json()
        return ip, data.get("country"), data.get("city")
    except:
        return ip, "Unknown", "Unknown"

# 📲 TELEGRAM ALERT
def alert(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


@app.route('/', methods=['GET','POST'])
def login():
    error = None

    if request.method == 'POST':
        user = request.form.get('username')
        pwd = request.form.get('password')

        ip, country, city = get_ip_info()
        time = datetime.datetime.now().isoformat()

        ip_attempts[ip] = ip_attempts.get(ip, 0) + 1

        attack = detect_attack(user, pwd)

        if ip_attempts[ip] >= 5:
            attack = "Brute Force"

        threat = threat_level(attack, ip_attempts[ip])

        # 🚨 ALERT WITH PAYLOAD
        if attack != "Normal":
            alert_message = f"""🚨 ALERT: {attack}
Threat: {threat}
IP: {ip}
Country: {country}
Attempts: {ip_attempts[ip]}
Username: {user}
Password: {pwd}
"""
            alert(alert_message)

        # 🧾 LOG
        log = {
            "time": time,
            "ip": ip,
            "country": country,
            "username": user,
            "password": pwd,
            "attack_type": attack,
            "attempts": ip_attempts[ip],
            "threat": threat
        }

        with open("logs.json","a") as f:
            json.dump(log,f)
            f.write("\n")

        error = "Login failed"

    return render_template_string(login_page, error=error)


# 📊 DASHBOARD WITH CHARTS
@app.route('/dashboard')
def dashboard():
    logs=[]
    sqli=0
    brute=0
    high=0
    medium=0

    try:
        with open("logs.json") as f:
            for line in f:
                d=json.loads(line)
                logs.append(d)

                if d["attack_type"]=="SQL Injection":
                    sqli+=1
                if d["attack_type"]=="Brute Force":
                    brute+=1
                if d["threat"]=="High":
                    high+=1
                if d["threat"]=="Medium":
                    medium+=1
    except:
        pass

    return render_template_string("""
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body{background:#0f172a;color:white;font-family:Arial;}
            canvas{max-width:500px;margin:20px;}
        </style>
    </head>
    <body>

    <h1>📊 SOC Dashboard</h1>

    <canvas id="attackChart"></canvas>
    <canvas id="threatChart"></canvas>

    <script>
    new Chart(document.getElementById('attackChart'),{
        type:'bar',
        data:{
            labels:['SQL Injection','Brute Force'],
            datasets:[{
                label:'Attacks',
                data:[{{sqli}},{{brute}}],
            }]
        }
    });

    new Chart(document.getElementById('threatChart'),{
        type:'pie',
        data:{
            labels:['High','Medium'],
            datasets:[{
                data:[{{high}},{{medium}}],
            }]
        }
    });
    </script>

    </body>
    </html>
    """, sqli=sqli, brute=brute, high=high, medium=medium)


if __name__ == '__main__':
    print("🚀 NORTHBRIDGE FINTECH HONEYPOT RUNNING")
    app.run(debug=True)