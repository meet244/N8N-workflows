# 🌐 Website & Social Media Scraper

<img width="1362" height="411" alt="image" src="https://github.com/user-attachments/assets/7690d946-da1d-4422-bcdd-8a930f6beddc" />

This automation scrapes company data from websites and social media links (like Facebook, Instagram, etc.) listed in a Google Sheet.  
If only the website is available, it automatically discovers social links, visits them, and scrapes **emails, mobile numbers**, and more.

Built using **n8n** for automation and **Python + Playwright** for advanced scraping.

---

## 🔁 What It Does

1. **Start** – Trigger manually via “Test Workflow”.
2. **Read from Google Sheets** – Loads website/Facebook URLs.
3. **Filter** – Keeps only unprocessed or valid rows.
4. **Loop** – Processes each record sequentially.
5. **Scrape** – Uses a Python scraper to:
   - Visit websites and extract social media links (Facebook, Instagram, etc.)
   - Visit those social links and extract:
     - **Emails**
     - **Phone/Mobile numbers**
     - Any other visible contact info
6. **Update Sheet** – Enriches the original Google Sheet with scraped details.

---

## 🧰 Tech Stack

- **n8n** – Automation and workflow orchestration  
- **Google Sheets** – Used as the data source and output destination  
- **Python + Playwright** – Headless browser scraping for dynamic websites  
- **HTTP API** – The Python script exposes a local API at `http://127.0.0.1:8000/scrape`

---

## 🧠 Example Use Cases

- Enrich CSV lead lists with contact details  
- Find missing Facebook/Instagram links for businesses  
- Extract **emails and mobile numbers** from Facebook pages  
- Build a richer outreach dataset

---

## 📂 Folder Contents

```bash
social-links-scraper/
│
├── Scrape_Details.json        # n8n workflow file
├── app.py                     # Python script for scraping (Playwright)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
