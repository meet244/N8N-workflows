# 🤖 Upwork Job Scraper & AI Assistant (n8n Flow)

<img width="100%" alt="n8n-upwork-flow-diagram" src="https://github.com/user-attachments/assets/016570fa-6150-4113-a9ec-981838f9172f" />

This project is a fully automated job monitoring and application assistant built with **n8n**. It actively scrapes new job listings from **Upwork** based on a specific search query, checks if they've been seen before, uses **Google Gemini** to draft a personalized cover letter, and sends an instant **WhatsApp notification** for every new, relevant opportunity.

This workflow is designed for freelancers and agencies who want to get a competitive edge by being the first to know about and respond to new client projects on Upwork.

-----

## 📌 Features

  * 🔎 **Automated Job Scraping**: Fetches the latest jobs from **Upwork** using a specific keyword (e.g., "n8n").
  * 💾 **Persistent Memory**: Uses an **Airtable** base to keep track of jobs it has already processed, preventing duplicate alerts.
  * 🤖 **AI Cover Letter Generation**: Leverages **Google Gemini** to analyze the job description and write a tailored, informal cover letter based on a predefined user profile.
  * ⚡ **Instant WhatsApp Notifications**: Sends a message to your phone the moment a new job matching your criteria is found.
  * 📄 **Structured Data Storage**: Saves all relevant job details (title, URL, budget, description, and AI cover letter) into Airtable for easy access and tracking.
  * ⚙️ **Easy to Configure**: Simply change the search keyword in the first node to monitor different types of jobs.

-----

## 🧩 Flow Breakdown

### 1\. **Trigger & Configuration**

  * Starts with a **Manual Trigger** (but can be easily switched to a schedule).
  * An **Edit Fields** node sets the `search_field` variable (e.g., "n8n"), which defines the keyword for the job search on Upwork.

-----

### 2\. **Scrape & Process Jobs**

  * An **HTTP Request** node calls the **Apify API** to scrape the latest Upwork jobs matching the search keyword.
  * A **Loop Over Items** node processes each scraped job individually.

-----

### 3\. **Check for New Jobs**

  * For each job, the **Search records** node checks the **Airtable** base to see if a record with the same Job ID already exists.
  * An **IF** node then checks if the search result was empty.
      * ✅ **If empty (True)**: It means the job is new, and the workflow proceeds to the next step.
      * ❌ **If not empty (False)**: The job has been seen before, and the workflow stops for that item.

-----

### 4\. **Generate Cover Letter & Save**

  * **Basic LLM Chain (Gemini)**: The new job's details are sent to **Google Gemini**. The AI is prompted to act as a skilled writer and draft a compelling cover letter based on a provided freelancer profile.
  * **Create a record**: The original job details and the newly generated cover letter are saved as a new record in **Airtable**.

-----

### 5\. **Send Notification**

  * **Send message**: A **WhatsApp** node sends an instant notification to a specified phone number, alerting the user about the new job opportunity with its title.

-----

## 🛠️ APIs & Services Used

| Service               | Purpose                                                 |
| --------------------- | ------------------------------------------------------- |
| **Apify API** | Scrapes job listings from Upwork.com.                   |
| **Airtable API** | Acts as a database to store jobs and prevent duplicates.|
| **Google Gemini API** | Analyzes job details and generates cover letters.       |
| **WhatsApp Cloud API**| Sends real-time notifications for new jobs.             |

-----

## 🚀 Use Cases

  * ⚡ **First Mover Advantage**: Get notified and apply to new Upwork jobs faster than the competition.
  * ✍️ **Streamline Applications**: Eliminate the initial effort of writing a cover letter from scratch for every job.
  * 📊 **Freelance Job Tracker**: Automatically build a personal database of all relevant jobs in your niche.
  * 🧑‍💻 **Market Research**: Monitor the demand for specific skills or technologies on the world's largest freelance platform.

-----

## 🧠 AI Cover Letter Prompt

The AI is instructed to act as an expert cover letter writer, using a specific freelancer profile to create a personalized and informal proposal for each job.

> "You are a good writer who writes good cover letters for Upwork work, so I will give you the details about the job on Upwork and you have to write a good cover letter for that. My profile is given below, based on that profile you have to write a great cover letter. You must try to cover all the queries in your cover letter and it should not be too big. it should be easy and quick to read. no use of jargons, keep it a bit informal and concise.
>
> **my details**
>
> **Meet Patel**
>
> **Headline:** AI & Automation Developer | 2 Years Experience
> **About Me:** An enthusiastic AI and automation developer with 2 years of experience. Adept at problem-solving, learning new technologies quickly, and turning ideas into functional AI applications..."
