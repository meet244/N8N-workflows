# Cold Outreach Automation Workflow

## Overview
This project automates the process of sending hyper-personalized cold outreach emails using Gmail, social media research, and a structured workflow.


### Workflow Diagram
<img width="1615" height="588" alt="image" src="https://github.com/user-attachments/assets/118c9aba-e1eb-43ad-bae7-388c4cbec7db" />


The automation:
1. Takes a list of prospects.
2. Finds and collects publicly available data about them.
3. Generates personalized icebreakers.
4. Stores the details in an Excel/Google Sheet.
5. Sends the cold emails using multiple Gmail accounts to bypass sending limits.

---

## Step-by-Step Process

### 1. **Input Prospect Data**
- Upload or connect to your **source list** of prospects (name, email, LinkedIn URL, etc.).
- File formats supported: `.csv`, `.xlsx`, or a connected Google Sheet.

### 2. **Data Preprocessing**
- **Filter**: Remove duplicates, invalid email addresses, or unwanted entries.
- **Load**: Store clean data in memory for processing.

### 3. **Prospect Research**
- Search for each contact across:
  - **LinkedIn**
  - **Facebook**
  - **Company websites**
  - **Public email sources**
- Extract relevant profile data (e.g., recent posts, achievements, company updates).

### 4. **Generate Icebreakers**
- For each prospect, feed the gathered data into the **personalization generator**.
- The generator:
  - Summarizes key findings.
  - Writes a 1–2 sentence hyper-personalized opening line for the email.

### 5. **Update Storage**
- Append the personalized icebreaker to the prospect’s row in the **Google Sheet/Excel**.
- Maintain columns:
  - `Name`
  - `Email`
  - `Source URL`
  - `Icebreaker`
  - `Status`

### 6. **Email Sending**
- Compose the cold outreach email by combining:
  - Greeting + Icebreaker + Value Proposition + CTA.
- Send through Gmail.
- **Multiple Gmail accounts** are used in rotation to avoid Google’s sending limit (~500/day for free accounts).

### 7. **Logging & Status Tracking**
- Track each email’s send status (`Pending`, `Sent`, `Failed`).
- Store any bounce or failure messages for later follow-up.

---

## Tech Stack
- **Automation platform**: n8n / Zapier / Make (adapt depending on your setup).
- **Email sending**: Gmail API.
- **Data storage**: Google Sheets / Excel.
- **Personalization**: GPT API for text generation.
- **Data extraction**: Web scraping / LinkedIn APIs.

---

## File Structure Example
