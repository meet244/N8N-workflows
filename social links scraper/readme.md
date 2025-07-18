# 🌐 Website & Social Media Scraper

<img width="1362" height="411" alt="image" src="https://github.com/user-attachments/assets/7690d946-da1d-4422-bcdd-8a930f6beddc" />

This automation scrapes company data from websites and social media links (like Facebook, Instagram, etc.) listed in a Google Sheet. If only the website is available, it discovers and scrapes social media links too. Built using **n8n** and custom **Python Playwright** code for deep scraping.

---

## 🔁 What It Does

1. **Start** – Trigger manually via “Test Workflow”.
2. **Read from Google Sheets** – Imports website/Facebook links.
3. **Filter** – Keeps only the unprocessed or valid rows.
4. **Loop** – Processes each row one-by-one using a queue system.
5. **Scrape** – Uses a custom API (running locally with Playwright) to:
   - Visit websites and collect social media links
   - Visit Facebook/Instagram pages and collect data like:
     - Email addresses
     - Phone numbers
     - Other available contact info
6. **Update Sheet** – Writes enriched data back to Google Sheets.

---

## 🧰 Tech Stack

- **n8n** – Automation platform for orchestrating scraping
- **Google Sheets** – For input and output
- **Python + Playwright** – Custom scraper code
- **HTTP API** – Python script runs on `http://127.0.0.1:8000/scrape`

---

## 🧠 Example Use Cases

- Enrich lead lists with missing contact info  
- Find social links from company websites  
- Scrape emails and phone numbers from Facebook/Insta pages

---

## 📂 Folder Contents

```bash
social-links-scraper/
│
├── Scrape_Details.json                    # n8n workflow file
├── app.py                   # Python script for scraping
├── requirements.txt                  # Python dependencies
└── README.md                          # (this file)
