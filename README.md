# osint-cache-analyzer
A Python-based Open Source Intelligence (OSINT) research tool designed to analyze residual data leakage and CDN caching mechanisms during privacy state transitions on social media networks

# OSINT Media Cache & Residual Data Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Topic: Cyber Security](https://img.shields.io/badge/Topic-Cyber%20Security-red.svg)](https://github.com/)

An educational and defensive cybersecurity tool developed to demonstrate the concept of **Information Disclosure via Caching and Broken Access Control**. 

This research project audits target endpoints to analyze whether public Content Delivery Network (CDN) links or cached metadata arrays linger after an account undergoes a privacy state transition (e.g., changing from public to private).

---

## 🔍 Core Security Concept Analyzed

Modern web platforms often implement strict controls on user profiles. However, historical data distribution architectures (like distributed CDNs and localized JSON responses) might lag during instant privacy state switches. 

This tool performs unauthenticated HTTP requests to parse public DOM data structures (`application/json`) and targets the `polaris_timeline_connection` node to audit:
* **Information Disclosure:** Persistence of public asset structures.
* **Improper Cache Invalidation:** Evaluating if CDN endpoints instantly decouple from raw unauthenticated queries.

---

## 🛠️ System Architecture & Workflow

1. **Reconnaissance:** Sends a standard, non-session HTTP GET request replicating client headers.
2. **Parsing:** Utilizes `BeautifulSoup` to trace specific embedded metadata strings safely.
3. **Data Mapping:** Parses JSON objects recursively to isolate public-facing image resolutions.
4. **Local Verification:** Spins up a local loopback server (`localhost:8080`) to seamlessly present logs and artifacts for defensive assessment.

---

## 🚀 Getting Started & Requirements

### Prerequisites
Make sure you have Python 3.8 or higher installed on your environment (Termux, Linux, Windows, or macOS).

### Installation
Clone this repository or download the script directly:
```bash
git clone [https://github.com/YOUR_USERNAME/osint-media-cache-analyzer.git](https://github.com/YOUR_USERNAME/osint-media-cache-analyzer.git)
cd osint-media-cache-analyzer

