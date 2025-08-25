# 🤖 Automated LinkedIn Content Factory – AI-Powered Content Generation & Publishing (n8n Flow)

<img width="100%" alt="flow-graph" src="https://github.com/user-attachments/assets/aa5e2070-2286-4de7-95ff-eaa45f983b86" />

This project is a complete, end-to-end content automation pipeline built in **n8n**. It autonomously ideates, writes, designs, and publishes high-quality content to **LinkedIn** on a schedule. By leveraging **Google Gemini** for text, **OpenAI DALL-E** for images, and **Airtable** as a content database, this workflow runs a social media presence with minimal human intervention.

This specific flow is configured to act as the voice of **FIVOON**, a fictional automation company, generating insightful posts about AI and technology.

-----

## 🧾 Output Sample

The final result is a fully-formed LinkedIn post, complete with a unique AI-generated image, published automatically according to the schedule.

> #### **FIVOON**
>
> **Is AI Stealing Our Creativity? Unpacking the Copyright Clash\!**
>
> The paintbrush is in the AI's hand. But who owns the masterpiece?
>
> Generative AI has unleashed an explosion of creativity, from stunning art to compelling prose. But beneath the surface of this innovation, a storm is brewing: the copyright conundrum. As an AI engineer and founder, I'm constantly fascinated by how these technologies push boundaries, not just technically, but ethically and legally.
>
> Traditional copyright law is built on human authorship. But what happens when an algorithm, trained on millions of human-created works, produces something novel? This isn’t just a philosophical debate; it's a practical nightmare for industries from music to publishing...
>
> *[AI-Generated Image: A dark, grainy image with a human and robotic hand reaching for a glowing pixel]*
>
> \#AIethics \#CopyrightLaw \#GenerativeAI \#FutureOfWork

-----

## 📌 Features

  * 🔁 **End-to-End Automation**: Handles the entire content lifecycle from idea generation to final publication.
  * 🧠 **AI-Powered Copywriting**: Uses **Google Gemini** to brainstorm new topics, write post text, and create image prompts, avoiding repetition.
  * 🖼️ **AI Image Generation**: Leverages **OpenAI DALL-E** to create unique, high-quality images based on a consistent style reference.
  * 🗓️ **Dual-Schedule System**: One schedule generates content in advance, while a separate schedule handles publishing.
  * 🗂️ **Content Management in Airtable**: Uses an **Airtable** base as a CMS to track the status of each post (e.g., Idea, Create, Ready, Post, Posted).
  * 👔 **Custom AI Persona**: The AI is prompted to adopt the specific voice and expertise of a founder in the automation space.

-----

## 🧩 Flow Breakdown

The workflow is divided into three main stages:

### 1\. **Generate a New Post Idea and All Materials**

  * **Schedule Trigger**: The process starts automatically at a set time (e.g., 5 AM daily).
  * **Search Records**: It fetches previously used ideas from an **Airtable** base to ensure new content is unique.
  * **Idea Generator (Gemini)**: The core AI step where **Google Gemini** receives the list of old ideas and a detailed prompt. It generates a new post idea, title, full text, and a detailed image description.
  * **Structured Output**: The AI's response is parsed into a clean JSON format.

-----

### 2\. **Generate an Image and Save**

  * **Image Style**: Downloads a style reference image from **Google Drive** to guide the AI.
  * **OpenAI Image**: Sends the Gemini-generated image description and the style reference to the **OpenAI DALL-E** API, which creates a new, stylistically consistent image.
  * **Save & Update**: The newly created image is saved to a designated folder in **Google Drive**, and the corresponding **Airtable** record is updated with the post text, image link, and its status is set to "Ready."

-----

### 3\. **Auto Posting**

  * **Schedule Trigger 2**: This independent process runs at a different time (e.g., 4 PM daily), designed for optimal publishing time.
  * **Search & Pick**: It searches the **Airtable** base for any records with the status "Post" and picks one.
  * **Publish Post**: It downloads the image from Google Drive and publishes the post—text and image—directly to a **LinkedIn** company page.
  * **Update Record**: After successful posting, it updates the record's status in Airtable to "Posted" to complete the cycle.

-----

## 🛠️ APIs & Services Used

| Service | Purpose |
| :--- | :--- |
| **Airtable API** | Acts as the content database and CMS. |
| **Google Gemini API** | Generates all text content (ideas, posts, image descriptions). |
| **OpenAI DALL-E API** | Creates unique, AI-generated images for each post. |
| **Google Drive API** | Stores and serves the generated images and style references. |
| **LinkedIn API** | Automatically publishes the final content to a company page. |

-----

## 🚀 Use Cases

  * 👨‍💼 **Automated Personal Branding**: Ideal for founders, CEOs, and professionals who want to maintain an active, high-quality social media presence.
  * 🏢 **Corporate Content Marketing**: Run a company's LinkedIn page on autopilot, ensuring a consistent stream of relevant content.
  * 💡 **Creative AI Exploration**: A powerful template for experimenting with multi-modal AI content generation workflows.
  * 📢 **Scalable Content Production**: Easily manage and scale a content calendar without the need for a large team.

-----

## 🧠 AI Personality Prompt (FIVOON Founder)

The AI is given a detailed persona to ensure the generated content is consistent, professional, and valuable to the target audience.

> "ROLE: You're an AI engineer and founder of an automation company named FIVOON. You regularly post about AI and automation topics, aiming to share valuable and practical insights with your LinkedIn audience.
>
> OBJECTIVE: Your goal is to create a structure for your next LinkedIn post including 1) a concise post name, 2) a clear post idea, 3) a captivating title, 4) the full post text, and 5) an ultra-minimalistic image description tailored to AI and automation.
>
> SCENARIO: Your LinkedIn blog focuses on AI advancements, automation strategies, and your journey as a founder. Your audience includes AI developers, startup founders, automation enthusiasts, and tech professionals...
>
> EXPECTATION: Produce a 200-300 word LinkedIn post outline with a strong hook, engaging narrative, and a meaningful marketing or automation insight conclusion..."
