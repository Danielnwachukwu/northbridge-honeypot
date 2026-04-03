# 🚨 Northbridge Fintech Honeypot

A Python-based web honeypot that simulates a secure login portal to detect and analyze malicious activity such as SQL injection and brute-force attacks.

---

## 🔍 Features

- SQL Injection detection (e.g. `' OR 1=1 --`, `UNION SELECT`)
- Brute-force attack detection
- Real-time Telegram alerts
- Attack logging (IP, username, password payload, threat level)
- GeoIP enrichment (demo mode)
- Interactive dashboard with charts (Chart.js)

---

## 🧠 How It Works

The application mimics a login portal and captures all login attempts.  
Suspicious inputs are analyzed and classified as attacks, logged, and optionally sent as real-time alerts.
---

## 📊 Dashboard

Access the dashboard at:

http://127.0.0.1:5000/dashboard

Displays:
- Attack counts (SQLi vs Brute Force)
- Threat level distribution
- Logged attack activity

---

## ⚙️ Setup

### 1. Clone repository
```bash

---

## 📸 Screenshots

### 🔐 Login Portal
![Login](login.png)

### 🚨 Telegram Alert
![Alert](alert.png)


git clone https://github.com/Danielnwachukwu/northbridge-honeypot.git
cd northbridge-honeypot
