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

---

## Code

```
{
  "nodes": [
    {
      "parameters": {},
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [
        -80,
        0
      ],
      "id": "1efa414b-3d7c-4d3b-b8c3-d356c9073b5e",
      "name": "When clicking ‘Execute workflow’"
    },
    {
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "id": "77041761-f01b-46e6-ba14-cba79710aa80",
              "name": "search_field",
              "value": "n8n",
              "type": "string"
            }
          ]
        },
        "options": {}
      },
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.4,
      "position": [
        128,
        0
      ],
      "id": "c0774092-49e2-405e-bac2-ab302b3074f9",
      "name": "Edit Fields"
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://api.apify.com/v2/acts/jupri~upwork/run-sync-get-dataset-items",
        "sendQuery": true,
        "queryParameters": {
          "parameters": [
            {
              "name": "token"
            }
          ]
        },
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={\n    \"contract_to_hire\": false,\n    \"dev_dataset_clear\": false,\n    \"dev_no_strip\": false,\n    \"fixed\": false,\n    \"hourly\": false,\n    \"includes.attachments\": false,\n    \"includes.history\": false,\n    \"no_hires\": false,\n    \"payment_verified\": false,\n    \"previous_clients\": false,\n    \"query\": \"{{ $json.search_field }}\",\n    \"sort\": \"newest\"\n}",
        "options": {}
      },
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        320,
        0
      ],
      "id": "20562a4e-4285-4478-a2d9-3ef0be6b37ef",
      "name": "get upwork jobs"
    },
    {
      "parameters": {
        "operation": "create",
        "base": {
          "__rl": true,
          "value": "appcJJNophyUXQhCt",
          "mode": "list",
          "cachedResultName": "Upwork Jobs",
          "cachedResultUrl": "https://airtable.com/appcJJNophyUXQhCt"
        },
        "table": {
          "__rl": true,
          "value": "tbl26xjj6ZnKnfvMY",
          "mode": "list",
          "cachedResultName": "Table 1",
          "cachedResultUrl": "https://airtable.com/appcJJNophyUXQhCt/tbl26xjj6ZnKnfvMY"
        },
        "columns": {
          "mappingMode": "defineBelow",
          "value": {
            "Pay type": "={{ $('Loop Over Items').item.json.type }}",
            "Duration": "={{ $('Loop Over Items').item.json.fixed.duration.label }}",
            "Amount": "={{ $('Loop Over Items').item.json.fixed?.budget?.amount ? $('Loop Over Items').item.json.fixed.budget.amount : ($('Loop Over Items').item.json.hourly?.min && $('Loop Over Items').item.json.hourly?.max ? $('Loop Over Items').item.json.hourly.min + ' - ' + $('Loop Over Items').item.json.hourly.max : '') }} {{ $('Loop Over Items').item.json.currency }}\n\n\n",
            "job summary": "={{ $('Loop Over Items').item.json.description }}",
            "job URL": "={{ $('Loop Over Items').item.json.url }}",
            "Job Title": "={{ $('Loop Over Items').item.json.title }}",
            "Experience level required": "={{ $('Loop Over Items').item.json.contractorTier }}",
            "Job ID": "={{ $('Loop Over Items').item.json.id }}",
            "Cover Letter": "={{ $json.cover_letter }}"
          },
          "matchingColumns": [],
          "schema": [
            {
              "id": "Job Title",
              "displayName": "Job Title",
              "required": false,
              "defaultMatch": false,
              "canBeUsedToMatch": true,
              "display": true,
              "type": "string",
              "readOnly": false,
              "removed": false
            },
            {
              "id": "Job ID",
              "displayName": "Job ID",
              "required": false,
              "defaultMatch": false,
              "canBeUsedToMatch": true,
              "display": true,
              "type": "string",
              "readOnly": false,
              "removed": false
            },
            {
              "id": "job URL",
              "displayName": "job URL",
              "required": false,
              "defaultMatch": false,
              "canBeUsedToMatch": true,
              "display": true,
              "type": "string",
              "readOnly": false,
              "removed": false
            },
            {
              "id": "job summary",
              "displayName": "job summary",
              "required": false,
              "defaultMatch": false,
              "canBeUsedToMatch": true,
              "display": true,
              "type": "string",
              "readOnly": false,
              "removed": false
            },
            {
              "id": "Pay type",
              "displayName": "Pay type",
              "required": false,
              "defaultMatch": false,
              "canBeUsedToMatch": true,
              "display": true,
              "type": "string",
              "readOnly": false,
              "removed": false
            },
            {
              "id": "Amount",
              "displayName": "Amount",
              "required": false,
              "defaultMatch": false,
              "canBeUsedToMatch": true,
              "display": true,
              "type": "string",
              "readOnly": false,
              "removed": false
            },
            {
              "id": "Experience level required",
              "displayName": "Experience level required",
              "required": false,
              "defaultMatch": false,
              "canBeUsedToMatch": true,
              "display": true,
              "type": "string",
              "readOnly": false,
              "removed": false
            },
            {
              "id": "Duration",
              "displayName": "Duration",
              "required": false,
              "defaultMatch": false,
              "canBeUsedToMatch": true,
              "display": true,
              "type": "string",
              "readOnly": false,
              "removed": false
            },
            {
              "id": "Cover Letter",
              "displayName": "Cover Letter",
              "required": false,
              "defaultMatch": false,
              "canBeUsedToMatch": true,
              "display": true,
              "type": "string",
              "readOnly": false,
              "removed": false
            },
            {
              "id": "Created at",
              "displayName": "Created at",
              "required": false,
              "defaultMatch": false,
              "canBeUsedToMatch": true,
              "display": true,
              "type": "string",
              "readOnly": true,
              "removed": false
            }
          ],
          "attemptToConvertTypes": false,
          "convertFieldsToString": false
        },
        "options": {}
      },
      "type": "n8n-nodes-base.airtable",
      "typeVersion": 2.1,
      "position": [
        1584,
        96
      ],
      "id": "3e041333-ac99-49eb-b37b-6d77613e2e03",
      "name": "Create a record",
      "credentials": {
        "airtableTokenApi": {
          "id": "YULBv0dd8wPczZXJ",
          "name": "Airtable Personal Access Token account"
        }
      }
    },
    {
      "parameters": {
        "batchSize": "=1",
        "options": {}
      },
      "type": "n8n-nodes-base.splitInBatches",
      "typeVersion": 3,
      "position": [
        544,
        0
      ],
      "id": "6b93aea1-7674-47e0-8748-3b54d1b88eec",
      "name": "Loop Over Items"
    },
    {
      "parameters": {
        "operation": "search",
        "base": {
          "__rl": true,
          "value": "appcJJNophyUXQhCt",
          "mode": "list",
          "cachedResultName": "Upwork Jobs",
          "cachedResultUrl": "https://airtable.com/appcJJNophyUXQhCt"
        },
        "table": {
          "__rl": true,
          "value": "tbl26xjj6ZnKnfvMY",
          "mode": "list",
          "cachedResultName": "Table 1",
          "cachedResultUrl": "https://airtable.com/appcJJNophyUXQhCt/tbl26xjj6ZnKnfvMY"
        },
        "filterByFormula": "={Job ID} = \"{{$json.id}}\"",
        "returnAll": false,
        "limit": 1,
        "options": {}
      },
      "type": "n8n-nodes-base.airtable",
      "typeVersion": 2.1,
      "position": [
        816,
        112
      ],
      "id": "607698f3-2d99-44b1-997d-9770f557c675",
      "name": "Search records",
      "alwaysOutputData": true,
      "credentials": {
        "airtableTokenApi": {
          "id": "YULBv0dd8wPczZXJ",
          "name": "Airtable Personal Access Token account"
        }
      }
    },
    {
      "parameters": {
        "conditions": {
          "options": {
            "caseSensitive": true,
            "leftValue": "",
            "typeValidation": "strict",
            "version": 2
          },
          "conditions": [
            {
              "id": "b2b17953-6c48-40ac-a3f9-95e4b80fe2fa",
              "leftValue": "={{ $json.isEmpty() }}",
              "rightValue": "",
              "operator": {
                "type": "boolean",
                "operation": "true",
                "singleValue": true
              }
            }
          ],
          "combinator": "and"
        },
        "options": {}
      },
      "type": "n8n-nodes-base.if",
      "typeVersion": 2.2,
      "position": [
        1024,
        112
      ],
      "id": "df287ac1-89d9-4078-904e-5af0dc7e78d7",
      "name": "empty?"
    },
    {
      "parameters": {
        "promptType": "define",
        "text": "={{ $('Loop Over Items').item.json }}",
        "hasOutputParser": true,
        "messages": {
          "messageValues": [
            {
              "message": "You are a good writer who writes good cover letters for Upwork work, so I will give you the details about the job on Upwork and you have to write a good cover letter for that. My profile is given below, based on that profile you have to write a great cover letter. You must try to cover all the queries in your cover letter and it should not be too big. it should be easy and quick to read. no use of jargons, keep it a bit informal and concise.\n\n\n# my details\n\n# Meet Patel\n\n**Headline:** AI & Automation Developer | 2 Years Experience  \nSkilled in building AI-driven solutions and automating complex workflows to save time and improve efficiency. Passionate about creating intelligent systems that solve real-world problems.\n\n**Title:** AI & Automation Developer  \nExperienced in developing automation scripts, AI models, and integration tools. Focused on delivering high-quality, maintainable, and scalable solutions for businesses.\n\n**Current Company:** TechNova Solutions  \nWorking on AI-powered automation projects for clients across industries. Responsible for designing, implementing, and optimizing AI workflows and automation pipelines.\n\n**Education:** B.Tech in Computer Science, University of Mumbai  \nCompleted a strong foundation in computer science, machine learning, and software development. Focused on AI and automation projects during coursework and internships.\n\n**About Me:**  \nAn enthusiastic AI and automation developer with 2 years of experience. Adept at problem-solving, learning new technologies quickly, and turning ideas into functional AI applications. Always aiming to improve processes and deliver impactful solutions.\n\n\n\n\noutput format - \n{  \n\"cover_letter\": \"Hi ...\"\n}"
            }
          ]
        },
        "batching": {}
      },
      "type": "@n8n/n8n-nodes-langchain.chainLlm",
      "typeVersion": 1.7,
      "position": [
        1232,
        96
      ],
      "id": "f8c289f9-a701-4e02-8f60-356bb27fcf5c",
      "name": "Basic LLM Chain"
    },
    {
      "parameters": {
        "options": {}
      },
      "type": "@n8n/n8n-nodes-langchain.lmChatGoogleGemini",
      "typeVersion": 1,
      "position": [
        1232,
        256
      ],
      "id": "11659679-4bbb-4b87-8a97-85449f9634d9",
      "name": "Google Gemini Chat Model",
      "credentials": {
        "googlePalmApi": {
          "id": "gQgC07v7jtToYr9F",
          "name": "Gemini meet2005pokar3-1"
        }
      }
    },
    {
      "parameters": {
        "jsonSchemaExample": "{\n  \"cover_letter\": \"Hi [Client Name],\\n\\nI saw your job posting for [Job Title] and it looks like a perfect fit. [1–2 lines on how you’ll solve the client’s problem or handle the task]. I have experience with [relevant skills/tools] and can deliver [what client wants] efficiently.\\n\\nI’m happy to start right away and keep communication smooth throughout. Looking forward to helping you with [specific job task/result].\\n\\nBest,\\n[Your Name]\"\n}\n"
      },
      "type": "@n8n/n8n-nodes-langchain.outputParserStructured",
      "typeVersion": 1.3,
      "position": [
        1376,
        256
      ],
      "id": "082a8e3e-964b-46c3-bc23-4557f62e28e5",
      "name": "Structured Output Parser"
    },
    {
      "parameters": {
        "operation": "send",
        "phoneNumberId": "",
        "recipientPhoneNumber": "",
        "textBody": "=New Upwork Job Alert!*\\n\\n*Job Title:* {{ $('Loop Over Items').item.json.title }}",
        "additionalFields": {}
      },
      "type": "n8n-nodes-base.whatsApp",
      "typeVersion": 1,
      "position": [
        1808,
        96
      ],
      "id": "f5ae080b-7436-4dc3-ac69-c59ce56c5edf",
      "name": "Send message",
      "webhookId": "0bacbd41-cc99-4c69-a34c-ccfb90bc3196",
      "credentials": {
        "whatsAppApi": {
          "id": "oJN3WLpPKn4sdt1i",
          "name": "WhatsApp account"
        }
      }
    }
  ],
  "connections": {
    "When clicking ‘Execute workflow’": {
      "main": [
        [
          {
            "node": "Edit Fields",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Edit Fields": {
      "main": [
        [
          {
            "node": "get upwork jobs",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "get upwork jobs": {
      "main": [
        [
          {
            "node": "Loop Over Items",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Create a record": {
      "main": [
        [
          {
            "node": "Send message",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Loop Over Items": {
      "main": [
        [],
        [
          {
            "node": "Search records",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Search records": {
      "main": [
        [
          {
            "node": "empty?",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "empty?": {
      "main": [
        [
          {
            "node": "Basic LLM Chain",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Loop Over Items",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Basic LLM Chain": {
      "main": [
        [
          {
            "node": "Create a record",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Google Gemini Chat Model": {
      "ai_languageModel": [
        [
          {
            "node": "Basic LLM Chain",
            "type": "ai_languageModel",
            "index": 0
          }
        ]
      ]
    },
    "Structured Output Parser": {
      "ai_outputParser": [
        [
          {
            "node": "Basic LLM Chain",
            "type": "ai_outputParser",
            "index": 0
          }
        ]
      ]
    },
    "Send message": {
      "main": [
        [
          {
            "node": "Loop Over Items",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "pinData": {
    "get upwork jobs": [
      {
        "buyer": {
          "avgHourlyJobsRate": null,
          "company": {
            "companyId": "1316106713544855552",
            "contractDate": "2020-10-13T00:00:00.000Z",
            "isEDCReplicated": null,
            "name": null,
            "profile": {
              "industry": null,
              "size": null
            }
          },
          "jobs": {
            "openCount": 2,
            "postedCount": 6
          },
          "location": {
            "city": null,
            "country": "India",
            "countryTimezone": "Asia/Calcutta (UTC+05:30)",
            "offsetFromUtcMillis": 19800000
          },
          "stats": {
            "activeAssignmentsCount": 0,
            "feedbackCount": 0,
            "hoursCount": 0,
            "score": 0,
            "totalAssignments": 0,
            "totalCharges": null,
            "totalJobsWithHires": 0
          }
        },
        "category": {
          "name": "Web Development",
          "urlSlug": "web-development"
        },
        "categoryGroup": {
          "name": "Web, Mobile & Software Dev",
          "urlSlug": "web-mobile-software-dev"
        },
        "clientActivity": {
          "invitationsSent": 0,
          "lastBuyerActivity": "2025-08-17T06:30:05.946Z",
          "totalApplicants": 1,
          "totalHired": 0,
          "totalInvitedToInterview": 0,
          "unansweredInvites": 0
        },
        "contractorTier": "EXPERT",
        "currency": "USD",
        "description": "Description:\nI’m looking for an experienced n8n developer to build a workflow that collects Wix website URLs. The workflow should be simple, reliable, and allow filtering by country and website type (e.g., e-commerce, blog, portfolio).\n\nRequirements:\n\nUse n8n to build the workflow\n\nCollect URLs from Google search or reliable APIs (like SerpAPI/Zenserp)\n\nHandle pagination and deduplication\n\nAllow dynamic filters: country and niche/type\n\nOutput results to Google Sheets, Airtable, or CSV\n\nDeliver a working workflow that can be reused\n\nDeliverables:\n\nFully working n8n workflow\n\nInstructions on how to run it and apply filters\n\nSample output with 10–20 URLs\n\nSkills Required:\n\nn8n workflow automation\n\nWeb scraping or API integration\n\nData handling and filtering",
        "fixed": {
          "budget": {
            "amount": "100.0",
            "isoCurrencyCode": null
          },
          "duration": {
            "ctime": "2014-06-04T17:59:10.123Z",
            "id": "474250516458926083",
            "label": "Less than 1 month",
            "mtime": "2014-06-04T17:59:10.123Z",
            "rid": 4,
            "weeks": 3
          }
        },
        "hourly": {
          "duration": null,
          "max": null,
          "min": null,
          "type": null
        },
        "id": "1956966747065053351",
        "isContractToHire": true,
        "isPaymentMethodVerified": true,
        "level": "ExpertLevel",
        "numberOfPositionsToHire": 1,
        "occupation": {
          "freeText": null,
          "id": "1110580755107926016",
          "ontologyId": "upworkOccupation:fullstackdevelopment",
          "prefLabel": "Full Stack Development"
        },
        "openJobs": [
          {
            "ciphertext": "~021956944627719646150",
            "id": "1956944627719646150",
            "isPtcPrivate": false,
            "title": "Help Me Fix Small Issue in Running Facebook Ad (Beginner Level)",
            "type": "FIXED"
          }
        ],
        "phoneVerification": null,
        "premium": false,
        "qualifications": {
          "countries": null,
          "earnings": null,
          "group": null,
          "groupRecno": null,
          "languages": null,
          "localDescription": null,
          "localFlexibilityDescription": null,
          "localMarket": false,
          "location": null,
          "locationCheckRequired": false,
          "locations": null,
          "minHoursWeek": null,
          "minJobSuccessScore": 0,
          "minOdeskHours": 0,
          "onSiteType": null,
          "prefEnglishSkill": "ANY",
          "regions": null,
          "risingTalent": false,
          "shouldHavePortfolio": false,
          "states": null,
          "tests": null,
          "timezones": null,
          "type": "ANY"
        },
        "questions": [],
        "skills": [
          {
            "id": "1733104400597401607",
            "name": "n8n"
          },
          {
            "id": "996364628025274383",
            "name": "JavaScript"
          }
        ],
        "status": "ACTIVE",
        "tags": [
          "contractToHireSet",
          "searchable",
          "C2HJobsOptInEducation"
        ],
        "title": "Build n8n Workflow to Collect Wix Website URLs with Filters",
        "ts_create": "2025-08-17T06:30:06.035Z",
        "ts_publish": "2025-08-17T06:30:21.277Z",
        "ts_sourcing": null,
        "type": "FIXED",
        "url": "https://www.upwork.com/jobs/~021956966747065053351"
      },
      {
        "buyer": {
          "avgHourlyJobsRate": {
            "amount": 12.2315872390705
          },
          "company": {
            "companyId": "1337632209047199744",
            "contractDate": "2020-12-12T00:00:00.000Z",
            "profile": {
              "industry": "Tech & IT",
              "size": 2
            }
          },
          "jobs": {
            "openCount": 2,
            "postedCount": 16
          },
          "location": {
            "city": "Pune",
            "country": "India",
            "countryTimezone": "Europe/London (UTC+01:00)",
            "offsetFromUtcMillis": 3600000
          },
          "stats": {
            "activeAssignmentsCount": 1,
            "feedbackCount": 7,
            "hoursCount": 76.17,
            "score": 4.95,
            "totalAssignments": 13,
            "totalCharges": {
              "amount": 1637.18
            },
            "totalJobsWithHires": 12
          }
        },
        "category": {
          "name": "Scripts & Utilities",
          "urlSlug": "scripts-utilities"
        },
        "categoryGroup": {
          "name": "Web, Mobile & Software Dev",
          "urlSlug": "web-mobile-software-dev"
        },
        "clientActivity": {
          "invitationsSent": 2,
          "lastBuyerActivity": "2025-08-17T06:25:40.723Z",
          "totalApplicants": 4,
          "totalInvitedToInterview": 2,
          "unansweredInvites": 1
        },
        "contractorTier": "EXPERT",
        "currency": "USD",
        "description": "Project Overview: Urgent Hiring (50% is already done)\n\nWe need to build a prototype multi-agent system that automates grant writing for charities. The system should process grant documents, analyze requirements, conduct research, and generate high-quality responses.\n\nTechnical Requirements\nPlatform: N8n.io\nAI Services Integration:\n\nMistral AI API - Document parsing and OCR\nClaude API - Content analysis and generation\nPerplexity API - Research automation\nSupabase/ Pinecome - Data storage and vector database\n\nCore Workflow to Build\n\nDocument Processing: Parse grant guidelines and client information\nGap Analysis: Identify missing information requirements\nResearch Automation: Find relevant data to fill gaps\nContent Generation: Create tailored grant responses\nQuality Review: Automated review and refinement\n\nDeliverables\n\nWorking prototype processing end-to-end grant application\nDocumentation of workflows and setup\nDemo video showing complete process\nRecommendations for production implementation\n\nIdeal Candidate\n\nExperience with N8n workflows OR CrewAI multi-agent systems\nFamiliarity with Claude API, Perplexity API integration\nUnderstanding of document processing and AI automation\nSupabase/PostgreSQL experience preferred\nExperience with API integrations and workflow automation",
        "fixed": {
          "budget": {
            "amount": "100.0"
          },
          "duration": {
            "ctime": "2014-06-04T17:59:10.123Z",
            "id": "474250516458926082",
            "label": "1 to 3 months",
            "mtime": "2014-06-04T17:59:10.123Z",
            "rid": 3,
            "weeks": 9
          }
        },
        "id": "1956947333448336992",
        "isPaymentMethodVerified": true,
        "level": "ExpertLevel",
        "numberOfPositionsToHire": 1,
        "occupation": {
          "id": "1110580764771602432",
          "ontologyId": "upworkOccupation:scriptingandautomation",
          "prefLabel": "Scripting & Automation"
        },
        "openJobs": [
          {
            "ciphertext": "~021943581077195644077",
            "id": "1943581077195644077",
            "title": "N8N and AI Automation Expert",
            "type": "FIXED"
          }
        ],
        "phoneVerification": "VERIFIED",
        "qualifications": {
          "prefEnglishSkill": "ANY",
          "type": "ANY"
        },
        "skills": [
          {
            "id": "1733104400597401607",
            "name": "n8n"
          },
          {
            "id": "1031626717876699136",
            "name": "Automation"
          },
          {
            "id": "996364628025274386",
            "name": "Python"
          },
          {
            "id": "1031626755474440192",
            "name": "Machine Learning"
          },
          {
            "id": "1031626716094119936",
            "name": "Artificial Intelligence"
          },
          {
            "id": "1691099314245873665",
            "name": "AI Agent Development"
          }
        ],
        "status": "ACTIVE",
        "tags": [
          "searchable"
        ],
        "title": "N8N Expert Needed for Automation Projects",
        "ts_create": "2025-08-17T05:12:57.474Z",
        "ts_publish": "2025-08-17T05:12:57.872Z",
        "type": "FIXED",
        "url": "https://www.upwork.com/jobs/~021956947333448336992"
      },
      {
        "buyer": {
          "avgHourlyJobsRate": {
            "amount": 20.246738008736337
          },
          "company": {
            "companyId": "1514241738051461121",
            "contractDate": "2022-04-13T00:00:00.000Z",
            "profile": {
              "industry": "Retail & Consumer Goods",
              "size": 10
            }
          },
          "jobs": {
            "openCount": 7,
            "postedCount": 170
          },
          "location": {
            "city": "Schoonrewoerd",
            "country": "Netherlands",
            "countryTimezone": "Europe/Paris (UTC+02:00)",
            "offsetFromUtcMillis": 7200000
          },
          "stats": {
            "activeAssignmentsCount": 19,
            "feedbackCount": 34,
            "hoursCount": 2122.17,
            "score": 5,
            "totalAssignments": 78,
            "totalCharges": {
              "amount": 51129.57
            },
            "totalJobsWithHires": 67
          }
        },
        "category": {
          "name": "Graphic, Editorial & Presentation Design",
          "urlSlug": "graphic-editorial-presentation-design"
        },
        "categoryGroup": {
          "name": "Design & Creative",
          "urlSlug": "design-creative"
        },
        "clientActivity": {
          "lastBuyerActivity": "2025-08-17T06:13:22.714Z",
          "totalApplicants": 8
        },
        "contractorTier": "INTERMEDIATE",
        "currency": "USD",
        "description": "Are you the person who stays up until 2 AM testing new AI tools just because you can't help yourself?\n\nDo you get genuinely excited when a new model drops or when you discover a prompt hack that nobody else is talking about yet?\n\nHave you ever thought: \"I wish someone would just pay me to experiment with all the coolest AI tools and actually implement them in a real business\"?\n\nThis is that job.\n\nHERE'S WHAT MOST COMPANIES GET WRONG ABOUT \"AI ROLES\":\n\nThey either want you to be a data scientist with a PhD, or they think AI means \"use ChatGPT to write some emails.\"\n\nWe're different.\n\nWe're an e-commerce brand that actually gets it. \n\nWe know AI isn't just a tool — it's a complete reimagining of how marketing, content, and operations can work.\n\nAnd we need someone who lives and breathes this stuff to help us push the boundaries.\n\nWHAT YOU'LL ACTUALLY DO:\n\n— Test ChatGPT, Claude, MidJourney, ElevenLabs, makeugc.ai, and whatever drops next week\n— Build workflows in n8n and Make that actually blow our minds\n— Bring us discoveries that make us say \"We need to implement this immediately\"\n— Write marketing copy that converts (and do it 10x faster than traditional copywriters)\n— Create UGC-style content that people actually engage with\n— Build automations that save us hours while making everything better\n— Be our internal AI consultant and trainer\n— Help us stay ahead of competitors who are still hiring \"social media managers\"\n— Document and systemize what works so we can scale it\n\nWHY THIS ROLE EXISTS (AND WHY IT'S PERFECT FOR YOU)\n\nMost companies are afraid of AI. They're worried about replacing humans or making mistakes.\nWe're the opposite. We see AI as a superpower that lets creative people do impossible things.\n\nThe problem: Finding someone who has both the technical curiosity AND the business sense to make AI actually work in the real world.\n\nThat's you.\n\nYou're not just someone who plays with AI tools.\n \nYou're someone who sees the bigger picture. \n\nWho understands that the real magic happens when you combine AI capabilities with actual business strategy.\n\nWHAT MAKES YOU PERFECT FOR THIS:\n\nYou're obsessed with AI (like, actually obsessed):\n— You have strong opinions about GPT vs Claude vs Gemini\n— You've experimented with prompt engineering and have your own techniques\n— You get excited about new tool launches and actually test them\n\nYou understand business, not just technology:\n— You've used AI for copywriting, content creation, or marketing\n— You think in terms of ROI and results, not just \"cool features\"\n— You can explain complex AI concepts to less-technical people\n\nYou work like the future of work:\n— Fully remote and async doesn't scare you — it excites you\n— You communicate results clearly and document your discoveries\n— You're self-directed but love collaborating with a team that \"gets it\"\n\nBonus points if:\n— You've worked in e-commerce or understand the pet industry\n— You've built actual automations that saved time/money\n— You have examples of AI-generated content that performed well\n\nWHAT YOU'RE REALLY GETTING:\n\nComplete creative freedom:\n— Remote work with flexible hours\n— Unlimited experimentation budget for new AI tools\n— Direct input on company strategy and direction\n\nUnprecedented growth potential:\n— Be the AI expert in a company that's going all-in on AI\n— Build skills that will be worth 10x more in 2 years\n— Shape processes that could be scaled to massive teams\n\nThe ultimate learning environment:\n— Work with a team that values innovation over \"how we've always done it\"\n— Get paid to stay on the cutting edge of technology\n— Build a portfolio of AI implementations that will make you legendary\n\nTHE REAL TALK:\nIf you're looking for a traditional 9-5 where someone tells you exactly what to do, this isn't it.\n\nIf you want to be told \"just use ChatGPT to write some blog posts,\" we're not your company.\n\nBut if you're the type of person who:\n— Dreams about what marketing will look like in 2026\n— Has strong opinions about which AI tools are overhyped vs underrated\n— Wants to build something that's never been built before\n\nThen this might be the most important proposal you send this year.\n\nHOW TO APPLY (AND STAND OUT):\nDon't send us a generic proposal.\n\nInstead, show us you're exactly who we're looking for:\n\nTell us about your AI obsession:\n— What's your current favorite AI tool and why?\n— What's one AI trend everyone's missing?\n— Share an example of something creative you've built with AI\n— Show us one specific way you've used AI to solve a real problem\n— Include metrics if you have them (engagement, time saved, revenue generated, etc.)\n— Make us excited about working with you\n\nSalary: Competitive, based on experience, with rapid growth potential tied to performance\nHours: Flexible, both part-time and full-time options available\nDuration: Long-term collaboration for the right candidate\n\nP.S. If you're reading this and thinking \"This sounds too good to be true,\" you're probably not our person. \n\nThe right candidate is thinking \"Finally, someone who gets it.\"\n\nAre you that person?",
        "hourly": {
          "duration": {
            "ctime": "2014-06-04T17:59:10.123Z",
            "label": "More than 6 months",
            "mtime": "2014-06-04T17:59:10.123Z",
            "rid": 1,
            "weeks": 52
          },
          "max": 30,
          "min": 5,
          "type": "PART_TIME"
        },
        "id": "1956934167146399328",
        "isContractToHire": true,
        "isPaymentMethodVerified": true,
        "level": "IntermediateLevel",
        "numberOfPositionsToHire": 1,
        "occupation": {
          "id": "1737190722360750080",
          "ontologyId": "mp:70-10591",
          "prefLabel": "AI Image Generation & Editing"
        },
        "openJobs": [
          {
            "ciphertext": "~021956899209426152390",
            "id": "1956899209426152390",
            "title": "Funnel Builder - High-Converting Advertorial Pages (Pet Industry)",
            "type": "HOURLY"
          },
          {
            "ciphertext": "~021952114215685684872",
            "id": "1952114215685684872",
            "title": "Trademark Consultant Needed for E-Commerce Brand in CANADA",
            "type": "HOURLY"
          },
          {
            "ciphertext": "~021951305240708233396",
            "id": "1951305240708233396",
            "title": "🚀 Taboola Media Buyer – Scale a Fast-Growing Pet Brand with Native Ads",
            "type": "HOURLY"
          },
          {
            "ciphertext": "~021946486507812501446",
            "id": "1946486507812501446",
            "title": "🎯 Pinterest Ads for Pet Brand | Performance Marketing | Direct Response",
            "type": "HOURLY"
          },
          {
            "ciphertext": "~021944857107861366481",
            "id": "1944857107861366481",
            "title": "GERMAN Native Proofreader/Translator to join our e-commerce pet brand",
            "type": "HOURLY"
          },
          {
            "ciphertext": "~021944451137369572422",
            "id": "1944451137369572422",
            "title": "Conversion Rate Optimization for D2C Pet Brand",
            "type": "HOURLY"
          }
        ],
        "qualifications": {
          "minHoursWeek": 30,
          "prefEnglishSkill": "ANY",
          "type": "ANY"
        },
        "skills": [
          {
            "id": "1623716864165548032",
            "name": "Midjourney AI"
          },
          {
            "id": "1623716864178130944",
            "name": "ChatGPT"
          },
          {
            "id": "1733104400597401607",
            "name": "n8n"
          },
          {
            "id": "1733104401071357956",
            "name": "ElevenLabs"
          },
          {
            "id": "1691099315571273728",
            "name": "Claude"
          }
        ],
        "status": "ACTIVE",
        "tags": [
          "jsi_contractToHire",
          "contractToHireSet",
          "searchable",
          "C2HJobsOptInEducation"
        ],
        "title": "The AI Playground Job That Doesn't Exist Anywhere Else",
        "ts_create": "2025-08-17T04:20:38.376Z",
        "ts_publish": "2025-08-17T04:21:00.533Z",
        "type": "HOURLY",
        "url": "https://www.upwork.com/jobs/~021956934167146399328"
      },
      {
        "buyer": {
          "company": {
            "companyId": "1706674406148935680",
            "contractDate": "2023-09-26T00:00:00.000Z"
          },
          "jobs": {
            "openCount": 1,
            "postedCount": 2
          },
          "location": {
            "city": "Haifa",
            "country": "Israel",
            "countryTimezone": "Asia/Jerusalem (UTC+03:00)",
            "offsetFromUtcMillis": 10800000
          },
          "stats": {
            "activeAssignmentsCount": 1,
            "totalAssignments": 1,
            "totalCharges": {
              "amount": 360
            },
            "totalJobsWithHires": 1
          }
        },
        "category": {
          "name": "Virtual Assistance",
          "urlSlug": "virtual-assistance"
        },
        "categoryGroup": {
          "name": "Admin Support",
          "urlSlug": "admin-support"
        },
        "clientActivity": {
          "invitationsSent": 1,
          "lastBuyerActivity": "2025-08-16T21:53:42.148Z",
          "totalApplicants": 10,
          "totalInvitedToInterview": 1
        },
        "contractorTier": "INTERMEDIATE",
        "currency": "USD",
        "description": "I need an n8n expert to build a complete workflow for a voice assistant.\nThe assistant should:\n\t•\tTranscribe incoming voice messages (e.g., “I want to book a session”).\n\t•\tDetect user intent and ask for missing details (e.g., Which option? What time?).\n\t•\tContinue the conversation until the request is complete.\n\t•\tEither confirm and schedule the booking or provide requested information.\n\nRequirements:\n\t•\tFull implementation in n8n.\n\t•\tIntegration with speech-to-text and AI/NLP.\n\t•\tAbility to reply back to the user automatically.\n\t•\tDocumentation included.\n\nOptional: multi-language support + conversation logs.",
        "hourly": {
          "duration": {
            "ctime": "2014-06-04T17:59:10.123Z",
            "label": "1 to 3 months",
            "mtime": "2014-06-04T17:59:10.123Z",
            "rid": 3,
            "weeks": 9
          },
          "type": "FULL_TIME"
        },
        "id": "1956836051982354016",
        "isPaymentMethodVerified": true,
        "level": "IntermediateLevel",
        "numberOfPositionsToHire": 1,
        "occupation": {
          "id": "1110580768370315264",
          "ontologyId": "upworkOccupation:virtualadministrativeassistantservice",
          "prefLabel": "General Virtual Assistance"
        },
        "phoneVerification": "VERIFIED",
        "qualifications": {
          "minHoursWeek": 40,
          "minJobSuccessScore": 90,
          "prefEnglishSkill": "NATIVE",
          "risingTalent": true,
          "type": "INDEPENDENT"
        },
        "questions": [
          "Describe your recent experience with similar projects"
        ],
        "skills": [
          {
            "id": "1733104400597401607",
            "name": "n8n"
          },
          {
            "id": "1110580482566246400",
            "name": "API Integration"
          },
          {
            "id": "1192876961584136192",
            "name": "Automatic Speech Recognition"
          },
          {
            "id": "1633880258703847424",
            "name": "Conversational AI"
          },
          {
            "id": "1110580732286717952",
            "name": "Virtual Assistance"
          }
        ],
        "status": "ACTIVE",
        "tags": [
          "jpgV2Generated"
        ],
        "title": "n8n Voice Assistant Workflow Development for Scheduling & Information",
        "ts_create": "2025-08-16T21:50:45.910Z",
        "ts_publish": "2025-08-16T21:50:46.339Z",
        "type": "HOURLY",
        "url": "https://www.upwork.com/jobs/~021956836051982354016"
      },
      {
        "buyer": {
          "avgHourlyJobsRate": {
            "amount": 15.001357588922074
          },
          "company": {
            "companyId": "1728235159623634944",
            "contractDate": "2023-11-25T00:00:00.000Z"
          },
          "jobs": {
            "openCount": 1,
            "postedCount": 5
          },
          "location": {
            "city": "Santa Clara",
            "country": "United States",
            "countryTimezone": "America/Tijuana (UTC-07:00)",
            "offsetFromUtcMillis": -25200000
          },
          "stats": {
            "feedbackCount": 5,
            "hoursCount": 36.83,
            "score": 5,
            "totalAssignments": 7,
            "totalCharges": {
              "amount": 630.03
            },
            "totalJobsWithHires": 5
          }
        },
        "category": {
          "name": "AI & Machine Learning",
          "urlSlug": "ai-machine-learning"
        },
        "categoryGroup": {
          "name": "Data Science & Analytics",
          "urlSlug": "data-science-analytics"
        },
        "clientActivity": {
          "invitationsSent": 1,
          "lastBuyerActivity": "2025-08-17T01:16:27.662Z",
          "totalApplicants": 17,
          "totalInvitedToInterview": 4
        },
        "contractorTier": "INTERMEDIATE",
        "currency": "USD",
        "description": "use n8n + AI to fully automate a daily AI-focused newsletter that gets read by tens of thousands of people. From scraping hundreds of news articles across the internet every day, to generating bite-size content with custom prompting, this video shows exactly how you can automate an industry-specific newsletter for your niche",
        "hourly": {
          "duration": {
            "ctime": "2014-06-04T17:59:10.123Z",
            "label": "Less than 1 month",
            "mtime": "2014-06-04T17:59:10.123Z",
            "rid": 4,
            "weeks": 3
          },
          "type": "PART_TIME"
        },
        "id": "1956831763751152582",
        "isPaymentMethodVerified": true,
        "level": "IntermediateLevel",
        "occupation": {
          "id": "1110580759050571776",
          "ontologyId": "upworkOccupation:machinelearningservice",
          "prefLabel": "Machine Learning"
        },
        "phoneVerification": "VERIFIED",
        "qualifications": {
          "localMarket": true,
          "minHoursWeek": 30,
          "prefEnglishSkill": "ANY",
          "type": "ANY"
        },
        "skills": [
          {
            "id": "1031626762999021568",
            "name": "Node.js"
          },
          {
            "id": "1031626773660942336",
            "name": "React"
          },
          {
            "id": "1623716864178130944",
            "name": "ChatGPT"
          },
          {
            "id": "1733104400580624384",
            "name": "OpenAI API"
          },
          {
            "id": "1691099313809666048",
            "name": "FlutterFlow"
          },
          {
            "id": "1225465944849223680",
            "name": "Make.com"
          },
          {
            "id": "1031626723769696256",
            "name": "Chatbot Development"
          },
          {
            "id": "1691099314245873665",
            "name": "AI Agent Development"
          },
          {
            "id": "1691099314170376192",
            "name": "AI Bot"
          },
          {
            "id": "1031626716094119936",
            "name": "Artificial Intelligence"
          },
          {
            "id": "1733104400597401607",
            "name": "n8n"
          },
          {
            "id": "1691099315676131329",
            "name": "LangChain"
          },
          {
            "id": "1031626717876699136",
            "name": "Automation"
          },
          {
            "id": "1691099314254262272",
            "name": "AI Development"
          },
          {
            "id": "1253342869935763456",
            "name": "Chatbot"
          }
        ],
        "status": "ACTIVE",
        "tags": [
          "invitePost"
        ],
        "title": "N8n newsletter",
        "ts_create": "2025-08-16T21:33:43.503Z",
        "ts_publish": "2025-08-16T21:33:44.062Z",
        "type": "HOURLY",
        "url": "https://www.upwork.com/jobs/~021956831763751152582"
      }
    ]
  },
  "meta": {
    "templateCredsSetupCompleted": true,
    "instanceId": "023b86b457a9dc285230d548a523bd29bf8a1b2d347562a41abd78b1db45a14d"
  }
}
```
