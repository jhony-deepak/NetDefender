import csv
import os
import threading
from scapy.all import sniff
from flask import Flask, render_template, request, redirect, session
from datetime import timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.permanent_session_lifetime = timedelta(minutes=10)

USERNAME = 'admin'
PASSWORD = 'admin123'

# Email Alert Config (User must fill these)
EMAIL_USER = ''  # Your Gmail address
EMAIL_PASS = ''  # Your Gmail App Password
EMAIL_TO = ''    # Recipient email

def send_email_alert(subject, message):
    if not all([EMAIL_USER, EMAIL_PASS, EMAIL_TO]):
        print("⚠️ Email not configured. Skipping alert email.")
        return
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_TO
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        print(f"📧 Alert email sent: {subject}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session.permanent = True
            session['user'] = USERNAME
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user' not in session:
        return redirect('/')
    alerts = []
    try:
        with open("alerts.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                alerts.append(row)
    except Exception as e:
        print("Failed to load alerts.csv:", e)
    return render_template("index.html", alerts=alerts)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# --- Real-time Dashboard API Routes ---
from flask import jsonify
import random

@app.route('/api/stats')
def api_stats():
    try:
        timestamps = []
        rates = []
        with open("traffic_log.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in list(reader)[-6:]:  # last 6 entries
                timestamps.append(row[0])
                rates.append(int(row[1]))
        data = {
            "timestamps": timestamps,
            "rates": rates
        }
    except Exception as e:
        print("Failed to load traffic_log.csv:", e)
        data = {
            "timestamps": [],
            "rates": []
        }
    return jsonify(data)

@app.route('/api/geo-alerts')
def api_geo_alerts():
    geo_alerts = []
    try:
        with open("alerts.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                src_ip = row[1]
                geo_alerts.append({"ip": src_ip})
    except:
        pass
    return jsonify(geo_alerts)


# Port scanning detection logic
PORT_SCAN_THRESHOLD = 10  # Number of ports accessed in time window
SCAN_TIME_WINDOW = 5      # Time window in seconds

connection_log = defaultdict(list)

# --- Background thread to auto-update traffic_log.csv with real packet stats ---
def update_traffic_log():
    from collections import deque

    packet_window = deque(maxlen=60)
    def count_packet(pkt):
        packet_window.append(time.time())

    # Start sniffing in background
    threading.Thread(target=lambda: sniff(prn=count_packet, store=0), daemon=True).start()

    while True:
        try:
            current_time = time.time()
            packets_last_minute = [t for t in packet_window if current_time - t <= 60]
            timestamp = time.strftime('%H:%M')
            pps = len(packets_last_minute)

            if not os.path.exists("traffic_log.csv"):
                with open("traffic_log.csv", "w", newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["timestamp", "packets_per_sec"])

            with open("traffic_log.csv", "a", newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, pps])

            time.sleep(60)
        except Exception as e:
            print("Traffic log update error:", e)

def detect_port_scan(ip, dst_port):
    current_time = time.time()
    connection_log[ip] = [t for t in connection_log[ip] if current_time - t < SCAN_TIME_WINDOW]
    connection_log[ip].append(current_time)

    if len(connection_log[ip]) >= PORT_SCAN_THRESHOLD:
        alert = [time.strftime('%Y-%m-%d %H:%M:%S'), ip, 'Multiple Ports', 'TCP', 'Port Scanning Detected']
        with open("alerts.csv", "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(alert)
        with open("alerts.txt", "a") as f:
            f.write("⚠️ Port scanning detected from IP: {}\n".format(ip))
        with open("blocked_ips.txt", "a") as f:
            f.write(f"{ip}\n")
        print("🚨 Port scanning detected from", ip)
        send_email_alert("NetDefender Alert: Port Scan", f"Port scanning activity detected from IP: {ip}")
        connection_log[ip].clear()

if __name__ == '__main__':
    threading.Thread(target=update_traffic_log, daemon=True).start()
    print("🚨 NetDefender is live and watching your network...")
    app.run(debug=True, host='0.0.0.0', port=5050, use_reloader=False)