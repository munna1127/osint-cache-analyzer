# OSINT Media Cache & Residual Data Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Topic: Cyber Security](https://img.shields.io/badge/Topic-Cyber%20Security-red.svg)](https://github.com/)

An educational and defensive cybersecurity tool developed to demonstrate the concept of **Information Disclosure via Caching and Platforms Residual Metadata Retention**. 

This research project audits target public DOM data structures to analyze whether public Content Delivery Network (CDN) links or cached metadata arrays linger after an account undergoes modifications or privacy adjustments.

---

## 🔍 Core Security Concept Analyzed

Modern web platforms implement strict access controls on user profiles. However, historical data distribution architectures (like distributed CDNs and localized JSON responses) might lag during instant privacy configuration switches. 

This tool performs unauthenticated HTTP requests to parse public DOM elements (`application/json`) and targets specific timeline metadata nodes (`polaris_timeline_connection`) to audit:
* **Information Disclosure:** Unintended persistence of public asset structures.
* **Improper Cache Invalidation:** Evaluating if distributed CDN endpoints instantly decouple from raw unauthenticated queries.

---

## 🛠️ System Architecture & Workflow

1. **Reconnaissance:** Sends a standard, non-session HTTP GET request replicating mobile client headers.
2. **Parsing:** Utilizes `BeautifulSoup` to safely trace embedded structural metadata strings.
3. **Data Mapping:** Parses complex JSON objects recursively to isolate public-facing media resolutions.
4. **Local Verification Panel:** Spins up a local loopback web server (`localhost:8080`) to seamlessly present logs and mapped artifacts in a clear responsive dashboard.

---

## 🚀 Getting Started & Requirements

### Prerequisites
Make sure you have Python 3.8 or higher installed on your environment (Termux, Linux, Windows, or macOS).

### Installation
Clone this repository or download the script directly:
```bash
git clone [https://github.com/osint-media-cache-analyzer.git](https://github.com/osint-media-cache-analyzer.git)
cd osint-media-cache-analyzer
```
Install the required third-party libraries:
```
pip install requests beautifulsoup4
```
Usage
Run the auditing tool via terminal:
```
python osint-cache-analyzer.py
```

Follow the screen prompts to input the target profile username for the public network caching audit.
🛡️ Mitigation Strategies & Platform Defense
To mitigate the exposure analyzed by this research framework, modern web application architectures should deploy:
Immediate CDN Purging: Implementing real-time cache invalidation webhooks when user account scopes or visibility settings alter.
Cryptographic URL Signing: Restricting static content paths by adding time-bound access hashes requiring live session validation.
👤 Author
Aryan Kacher - Cyber Security Enthusiast & Developer
📜 Disclaimer
This software is provided strictly for Educational, Ethical Research, and Defensive Security Auditing purposes. The author does not condone or support unauthorized scanning or automated scraping against platform terms of service. It operates entirely within publicly exposed, unauthenticated client domains.

