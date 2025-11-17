---

## 🧠 How It Works (System Architecture)

NetDefender runs a real-time packet sniffer (`sniffer.py`) using `scapy` to monitor all incoming/outgoing packets. Detection rules for common network attacks trigger alerts when specific behaviors are observed:

- **ICMP Floods**: Excessive ping requests per second from the same IP
- **SYN Floods**: TCP SYN packets without ACKs — indicates DoS tools
- **ARP Spoofing**: Multiple MACs seen for one IP in ARP replies
- **DNS Spoofing**: Fake DNS replies mismatched to real IPs
- **Port Scanning**: SYN/NULL/Xmas flags to multiple ports (Nmap-like behavior)

🧠 It also:
- Logs packet rate per minute in `traffic_log.csv`
- Displays it live in the dashboard using Chart.js
- Tracks all alerts in both `alerts.csv` and `alerts.txt`

---

## 🧬 NetDefender Architecture (With Network & Security Layers)

```
                           🌐 External/Local Network
                                   │
                ┌──────────────────┴──────────────────┐
                │             Incoming Packets        │
                │        (e.g., TCP, ICMP, DNS...)     │
                └──────────────────┬──────────────────┘
                                   ▼
               ┌───────────────────────────────┐
               │  🔍 Packet Sniffer (Scapy)     │  ←─── Network Monitoring Layer
               └────────────┬──────────────────┘
                            ▼
             ┌───────────────────────────────┐
             │  🧠 Detection Engine           │  ←─── Security Analysis Layer
             │  - SYN/ICMP Flood             │
             │  - ARP/DNS Spoof              │
             │  - Port Scanning              │
             └────┬────────────┬─────────────┘
                  │            │
         ┌────────▼───┐   ┌────▼────────┐
         │ Alert Logs │   │ Rate Logger │         ←── Logging Layer
         │ alerts.csv │   │ traffic.csv│
         └─────┬──────┘   └────┬────────┘
               │               │
               ▼               ▼
       ┌──────────────┐   ┌───────────────┐
       │ IP AutoBlock │   │  📊 Flask UI  │  ←─── User Access + UX Layer
       │iptables rules│   │ + Chart.js    │
       └─────┬────────┘   └────┬──────────┘
             │                 │
             ▼                 ▼
   ┌────────────────┐   ┌─────────────────────┐
   │ blacklist.txt   │   │  Auth System (Login)│
   └────────────────┘   └─────────────────────┘
```

---

## 🔐 Authentication

- Session-based login (`admin:admin123`)
- Auto logout after 10 mins of inactivity
- Logout button and forced re-login if inactive

---

## 📈 Real-Time Dashboard

Built with Flask and Chart.js, the dashboard displays:

- 📊 Traffic Overview Chart (live packets/sec)
- 🧠 Threat Stats (SYN Flood, Port Scans, DNS Spoof)
- 📄 Real-Time Alerts Panel
- 📋 Detected Threats Table (IP, Protocol, Type, Timestamp)
- 🔐 Login session management

---

## ⚠️ Email Alerts

You can configure email alerts by editing:

```python
EMAIL_USER = 'your_gmail@gmail.com'
EMAIL_PASS = 'your_app_password'
EMAIL_TO   = 'receiver@gmail.com'
```

---

## 🌐 Deployment Options

Supports both:
- 🔧 **Native Python Run** (recommended)
- 🐳 **Dockerized Build** (optional)

---

## 🧾 Logs + Files

- `alerts.csv` — used by dashboard
- `alerts.txt` — full alert log
- `blocked_ips.txt` — IPs auto-blocked by rules
- `traffic_log.csv` — real-time packet rate data
- `blacklist.txt` — optional manual blacklisted IPs/domains

---

## 🧑‍💼 Real-World Use Cases

### 1. **Enterprise Network Threat Detection System** 🏢  
NetDefender can be deployed within corporate LANs to monitor internal traffic for common attack patterns like port scanning, spoofing, and DoS behavior. It acts as a lightweight, real-time IDS that integrates with existing firewall systems for automated IP blocking and alert escalation.

### 2. **Security Operations Center (SOC) Simulation Tool** 🖥️  
Useful for cybersecurity students, bootcamps, or red/blue team training, NetDefender provides a realistic simulation of how SOC teams detect and respond to threats. It includes real-time dashboards, automated responses, and full alert logging — mimicking core functions of a professional SOC.

### 3. **Home & Small Office Security Gateway** 🛡️  
Can be deployed on a Raspberry Pi or mini-PC at the network perimeter of a home/office setup to detect and mitigate threats like ARP spoofing, ICMP floods, or external scans. Acts as a personal firewall supplement with live alerts and visual threat statistics.

### 4. **Cybersecurity Research & ML Dataset Generator** 📊  
With detailed logs, real-time packet sniffing, and exportable CSVs, NetDefender can be used to collect labeled datasets for machine learning research in intrusion detection, anomaly detection, and network forensics.

### 5. **Legacy & Air-Gapped Network Defender** 🛰️  
In environments where modern endpoint agents (EDR/XDR) are not viable (e.g., air-gapped military or industrial systems), NetDefender provides passive monitoring without disrupting sensitive infrastructure. It can detect scans, spoofing, and unauthorized DNS activity silently.

---

## 📝 License

This project is licensed under the **MIT License**.

You are free to:
- ✅ Use this code commercially or personally
- ✅ Modify or distribute it as part of your own tools
- ✅ Learn from it and build upon it

Just include the original copyright:
```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

To read the full license text, refer to the included `LICENSE` file.