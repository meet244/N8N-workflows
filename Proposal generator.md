# 📄 Proposal Generation Automation Workflow

This workflow helps you **automatically generate professional proposals** for multiple clients at scale.  
All you need to do is provide the client’s details — the system handles the rest. 🚀  

<img width="1638" height="558" alt="c903e8a3-49f8-43d9-bda3-f02cb91b1191" src="https://github.com/user-attachments/assets/291a0ec0-fa77-40cd-a014-b3cb2cdc8d50" />


## ✨ What It Does

- 🔎 **Scrapes your website** for content & information  
- 🤖 **Uses Gemini LLM** to generate a client-ready proposal  
- 📝 **Fills a Google Docs template** with the proposal content  
- 📧 **Drafts a personalized email** with the proposal attached, ready to send  

---

## ⚙️ How It Works

1. **Enter Client Details**  
   - Name, email, company info, etc.  

2. **Automatic Website Scraping**  
   - Extracts key details from your site for proposal context.  

3. **Proposal Generation (Gemini LLM)**  
   - AI writes a polished proposal tailored to the client.  

4. **Google Docs Integration**  
   - Content is placed into your pre-set proposal template.  

5. **Email Drafting**  
   - Generates a ready-to-send draft email with the proposal attached.  

---

## 🚀 Use Cases

- Agencies creating **multiple proposals daily**  
- Freelancers who need to **save time on writing**  
- Businesses looking to **standardize their proposals**  
- Teams that want to **scale outbound pitches**  

---

## 🛠️ Setup & Requirements

- [n8n](https://n8n.io/) for workflow automation  
- Google Docs API access (for template writing)  
- Gemini API access (for LLM proposal generation)  
- (Optional) Email API like Gmail/Outlook for sending drafts  

---

## 📌 n8n Code

```json
{
  "nodes": [
    {
      "parameters": {
        "resource": "draft",
        "subject": "={{ $('Form').item.json['Company name'] }} | {{ $('Make Proposal').item.json.output.aiSystem }} Proposal",
        "emailType": "html",
        "message": "=<p>Hi {{ $('Form').item.json['First Name'] }},</p>\n<p>Here’s the proposal for the <strong>{{ $('Make Proposal').item.json.output.aiSystem }}</strong> build we discussed.<br>\nLet me know if you have any questions.</p>\n\n<p>– Meet</p>\n",
        "options": {
          "attachmentsUi": {
            "attachmentsBinary": [
              {
                "property": "proposal"
              }
            ]
          },
          "sendTo": "={{ $('Form').item.json.Email }}"
        }
      },
      "type": "n8n-nodes-base.gmail",
      "typeVersion": 2.1,
      "position": [
        464,
        800
      ],
      "id": "d0283494-11df-4628-b95f-d17faa831194",
      "name": "Create a draft",
      "webhookId": "4d4cb0cb-4793-423e-8a31-f6d6b87d1de3",
      "credentials": {
        "gmailOAuth2": {
          "id": "PmwCwQaIkpLF5mMq",
          "name": "Gmail account meet2005pokar@gmail.com"
        }
      }
    },
    {
      "parameters": {
        "operation": "copy",
        "fileId": {
          "__rl": true,
          "value": "1-2-hKtyaQSECXAiI2J6s1IO01sC0yo00aZ2wp0s7H-g",
          "mode": "list",
          "cachedResultName": "Proposal Template",
          "cachedResultUrl": "https://docs.google.com/document/d/1-2-hKtyaQSECXAiI2J6s1IO01sC0yo00aZ2wp0s7H-g/edit?usp=drivesdk"
        },
        "name": "={{ $json['Company name'] }} | Ai Proposal",
        "options": {}
      },
      "type": "n8n-nodes-base.googleDrive",
      "typeVersion": 3,
      "position": [
        -1216,
        784
      ],
      "id": "fd130459-07fc-437a-b9d7-dcd1463b7db3",
      "name": "Copy file",
      "executeOnce": true,
      "credentials": {
        "googleDriveOAuth2Api": {
          "id": "LZ6gnq6e2551KE90",
          "name": "Google Drive account"
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
              "id": "b841bba4-4d97-4e4e-9c70-acc0f0727d59",
              "leftValue": "={{ $('Form').item.json['Sales call recording URL'] }}",
              "rightValue": "",
              "operator": {
                "type": "string",
                "operation": "notEmpty",
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
        -672,
        784
      ],
      "id": "45b3e20d-ede6-44c7-ad97-731ad7886f12",
      "name": "has sales call?"
    },
    {
      "parameters": {
        "operation": "download",
        "fileId": {
          "__rl": true,
          "value": "={{ $('Form').item.json['Sales call recording URL'] }}",
          "mode": "url"
        },
        "options": {}
      },
      "type": "n8n-nodes-base.googleDrive",
      "typeVersion": 3,
      "position": [
        -496,
        720
      ],
      "id": "228b9cc3-f928-4689-bc33-92cb20ed0e41",
      "name": "Download sales call",
      "credentials": {
        "googleDriveOAuth2Api": {
          "id": "LZ6gnq6e2551KE90",
          "name": "Google Drive account"
        }
      }
    },
    {
      "parameters": {
        "url": "https://api.groq.com/openai/v1/audio/transcriptions",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "Authorization",
              "value": "=Bearer "
            }
          ]
        },
        "sendBody": true,
        "contentType": "multipart-form-data",
        "bodyParameters": {
          "parameters": [
            {
              "parameterType": "formBinaryData",
              "name": "file",
              "inputDataFieldName": "data"
            },
            {
              "name": "model",
              "value": "whisper-large-v3"
            }
          ]
        },
        "options": {}
      },
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        -336,
        720
      ],
      "id": "c8f40d46-af9b-4c86-bc66-adc70c4ed18b",
      "name": "Transcribe"
    },
    {
      "parameters": {
        "modelName": "models/gemini-2.5-pro",
        "options": {}
      },
      "type": "@n8n/n8n-nodes-langchain.lmChatGoogleGemini",
      "typeVersion": 1,
      "position": [
        -160,
        1008
      ],
      "id": "7c5f9c17-bb5f-4ec1-a09f-1a61e2e93bdb",
      "name": "Gemini",
      "credentials": {
        "googlePalmApi": {
          "id": "RDJ0bMhUW5qV8WEo",
          "name": "Gemini meet2005pokar-1"
        }
      }
    },
    {
      "parameters": {
        "promptType": "define",
        "text": "=Please analyze the following data.\n\nProspect Details\nFirst Name:{{ $('Form').item.json['First Name'] }}\nLast Name:{{ $('Form').item.json['Last Name'] }}\nCompany Name: {{ $('Form').item.json['Company name'] }}\nSales Call Transcript: {{ $json.text ? $json.text : 'NA' }}\nWebsite: {{ $('Markdown').item.json.data ? $('Markdown').item.json.data : 'NA' }}\n",
        "hasOutputParser": true,
        "messages": {
          "messageValues": [
            {
              "message": "# Overview  \nYou are an AI agent responsible for generating tailored proposal components in JSON format based on a sales call transcript and basic prospect details.\n\n## Context  \n- Your role is to craft high-conversion proposal content using a professional but conversational tone.  \n- Outputs must be JSON elements only — no explanatory or surrounding text.  \n- Each piece should reflect a deep understanding of the prospect’s problems and clearly explain how the proposed solution and upsell will provide meaningful outcomes.  \n- Pricing should range from $2,000 to $10,000 and reflect 5–10% of the value being saved or generated over the next year.  \n\n## Instructions  \n1. Analyze the sales call transcript to identify the core pain point of the prospect, ideally using their own words.  \n2. Construct a compelling problem statement and expand with three concise supporting bullets.  \n3. Name the proposed AI system based on the outcome it delivers and align it with the problem.  \n4. Write a clear solution statement and elaborate with three supporting bullets.  \n5. Explain why this solution works in 2–3 benefit-focused sentences.  \n6. Outline the detailed scope of work for the solution.  \n7. Generate a price in $USD aligned with the estimated annual value, keeping within the $2K–$10K range.  \n8. Define pricing type as either \"one time\" or \"monthly\".  \n9. Calculate and return 50% of the solution price in $USD.  \n10. Craft a complementary upsell offer that addresses the next logical or adjacent problem.  \n11. Follow a similar format for the upsell: name, scope (1–2 sentences), three supporting bullets, price, and pricing type.  \n\n## Tools  \n- Input:  \n  - Prospect Details  \n  - Sales Call Transcript  \n\n## Examples  \n- Input:  \n  - Sales Call Transcript: \"We spend hours manually tagging customer support tickets, which delays our response times.\"  \n- Output (JSON):  \n  ```json\n  {\n    \"problemStatement\": \"Your team is bogged down by the manual tagging of support tickets, causing delays in response times and reducing customer satisfaction.\",\n    \"problemStatementBulletOne\": \"Manual tagging consumes hours of valuable time weekly.\",\n    \"problemStatementBulletTwo\": \"Delayed ticket handling frustrates customers and risks churn.\",\n    \"problemStatementBulletThree\": \"Lack of automation is limiting your scalability.\",\n    \"aiSystem\": \"Smart Support Tagger\",\n    \"solutionStatement\": \"Smart Support Tagger is an AI-powered system that automatically classifies and tags incoming support tickets, ensuring faster routing and response.\",\n    \"solutionStatementBulletOne\": \"Automates initial support triage using natural language understanding.\",\n    \"solutionStatementBulletTwo\": \"Reduces average handling time by 40–60%.\",\n    \"solutionStatementBulletThree\": \"Integrates with existing support platforms like Zendesk and Intercom.\",\n    \"whyThisWorks\": \"This solution eliminates your team's repetitive workload and boosts response speed, directly improving the customer experience. It’s designed to scale as you grow, creating long-term efficiency gains.\",\n    \"workScope\": \"Setup and training of the AI model using your past ticket data, integration with current support platform, testing and QA, and deployment.\",\n    \"price\": \"$7000\",\n    \"solutionPricingType\": \"one time\",\n    \"50percentDiscount\": \"$3500\",\n    \"upsellOne\": \"Support Sentiment Monitor\",\n    \"upsellOneScope\": \"Support Sentiment Monitor analyzes incoming tickets and ongoing chats to detect customer emotions in real time. Paired with Smart Support Tagger, this enables even smarter routing and faster escalation of critical tickets.\",\n    \"upsellOneBulletOne\": \"Monitors sentiment to highlight at-risk customers.\",\n    \"upsellOneBulletTwo\": \"Pairs well with ticket tagging for full visibility.\",\n    \"upsellOneBulletThree\": \"Boosts NPS and customer retention by flagging issues early.\",\n    \"upsellOnePricing\": \"$5000\",\n    \"upsellOnePricingType\": \"one time\"\n  }\n  ```\n\n## SOP (Standard Operating Procedure)  \n1. Parse the sales call transcript and extract emotional or urgent language to form the problem statement.  \n2. Use clear and outcome-driven naming conventions for the AI system.  \n3. Create a concise yet compelling solution pitch with benefits and clarity.  \n4. Estimate solution pricing based on annual value potential.  \n5. Create a logical, adjacent upsell opportunity and match structure to the core offer.  \n6. Output only the final proposal JSON object with all specified keys.  \n\n## Final Notes  \n- Avoid abstract names for systems — prioritize clarity and outcome orientation.  \n- Make sure each bullet adds distinct value and insight.  \n- Keep tone professional but conversational to build rapport and trust.  \n---"
            }
          ]
        },
        "batching": {}
      },
      "type": "@n8n/n8n-nodes-langchain.chainLlm",
      "typeVersion": 1.7,
      "position": [
        -160,
        800
      ],
      "id": "c9dc87f4-32f2-41c0-b8d2-16d9ff209a6f",
      "name": "Make Proposal"
    },
    {
      "parameters": {
        "operation": "download",
        "fileId": {
          "__rl": true,
          "value": "={{ $json.documentId }}",
          "mode": "id"
        },
        "options": {
          "binaryPropertyName": "proposal",
          "googleFileConversion": {
            "conversion": {
              "docsToFormat": "application/pdf"
            }
          },
          "fileName": "=Proposal | {{ $('Form').item.json['Company name'] }}.pdf"
        }
      },
      "type": "n8n-nodes-base.googleDrive",
      "typeVersion": 3,
      "position": [
        304,
        800
      ],
      "id": "1c6f1a0f-930c-4301-9de5-ab98151dfee0",
      "name": "Download file",
      "credentials": {
        "googleDriveOAuth2Api": {
          "id": "LZ6gnq6e2551KE90",
          "name": "Google Drive account"
        }
      }
    },
    {
      "parameters": {
        "operation": "update",
        "documentURL": "={{ $('Copy file').item.json.id }}",
        "actionsUi": {
          "actionFields": [
            {
              "action": "replaceAll",
              "text": "{{prospectFirstName}}",
              "replaceText": "={{ $('Form').item.json['First Name'] }}"
            },
            {
              "action": "replaceAll",
              "text": "{{companyName}}",
              "replaceText": "={{ $('Form').item.json['Company name'] }}"
            },
            {
              "action": "replaceAll",
              "text": "{{problemStatement}}",
              "replaceText": "={{ $json.output.problemStatement }}"
            },
            {
              "action": "replaceAll",
              "text": "{{problemStatementBulletOne}}",
              "replaceText": "={{ $json.output.problemStatementBulletOne }}"
            },
            {
              "action": "replaceAll",
              "text": "{{problemStatementBulletTwo}}",
              "replaceText": "={{ $json.output.problemStatementBulletTwo }}"
            },
            {
              "action": "replaceAll",
              "text": "{{problemStatementBulletThree}}",
              "replaceText": "={{ $json.output.problemStatementBulletThree }}"
            },
            {
              "action": "replaceAll",
              "text": "{{aiSystem}}",
              "replaceText": "={{ $json.output.aiSystem }}"
            },
            {
              "action": "replaceAll",
              "text": "{{solutionStatement}}",
              "replaceText": "={{ $json.output.solutionStatement }}"
            },
            {
              "action": "replaceAll",
              "text": "{{solutionStatementBulletOne}}",
              "replaceText": "={{ $json.output.solutionStatementBulletOne }}"
            },
            {
              "action": "replaceAll",
              "text": "{{solutionStatementBulletTwo}}",
              "replaceText": "={{ $json.output.solutionStatementBulletTwo }}"
            },
            {
              "action": "replaceAll",
              "text": "{{solutionStatementBulletThree}}",
              "replaceText": "={{ $json.output.solutionStatementBulletThree }}"
            },
            {
              "action": "replaceAll",
              "text": "{{whyThisWorks}}",
              "replaceText": "={{ $json.output.whyThisWorks }}"
            },
            {
              "action": "replaceAll",
              "text": "{{workScope}}",
              "replaceText": "={{ $json.output.workScope }}"
            },
            {
              "action": "replaceAll",
              "text": "{{price}}",
              "replaceText": "={{ $json.output.price }}"
            },
            {
              "action": "replaceAll",
              "text": "{{solutionPricingType}}",
              "replaceText": "={{ $json.output.solutionPricingType }}"
            },
            {
              "action": "replaceAll",
              "text": "{{50percentDiscount}}",
              "replaceText": "={{ $json.output['50percentDiscount'] }}"
            },
            {
              "action": "replaceAll",
              "text": "{{upsellOne}}",
              "replaceText": "={{ $json.output.upsellOne }}"
            },
            {
              "action": "replaceAll",
              "text": "{{upsellOneScope}}",
              "replaceText": "={{ $json.output.upsellOneScope }}"
            },
            {
              "action": "replaceAll",
              "text": "{{upsellOneBulletOne}}",
              "replaceText": "={{ $json.output.upsellOneBulletOne }}"
            },
            {
              "action": "replaceAll",
              "text": "{{upsellOneBulletTwo}}",
              "replaceText": "={{ $json.output.upsellOneBulletTwo }}"
            },
            {
              "action": "replaceAll",
              "text": "{{upsellOneBulletThree}}",
              "replaceText": "={{ $json.output.upsellOneBulletThree }}"
            },
            {
              "action": "replaceAll",
              "text": "{{upsellOnePricing}}",
              "replaceText": "={{ $json.output.upsellOnePricing }}"
            },
            {
              "action": "replaceAll",
              "text": "{{upsellOnePricingType}}",
              "replaceText": "={{ $json.output.upsellOnePricingType }}"
            },
            {
              "action": "replaceAll",
              "text": "{{date}}",
              "replaceText": "={{ new Date().toLocaleDateString('en-GB') }}"
            }
          ]
        }
      },
      "type": "n8n-nodes-base.googleDocs",
      "typeVersion": 2,
      "position": [
        144,
        800
      ],
      "id": "42ede0cc-d5a0-4948-938d-38653fc3da4e",
      "name": "write proposal",
      "credentials": {
        "googleDocsOAuth2Api": {
          "id": "Y4rOpdmxmvoFD1ls",
          "name": "Google Docs account"
        }
      }
    },
    {
      "parameters": {
        "jsonSchemaExample": "{\n  \"problemStatement\": \"Your team is struggling to manage the high volume of inbound property inquiries, which means valuable, time-sensitive leads are slipping through the cracks and engaging with competitors instead.\",\n  \"problemStatementBulletOne\": \"Manually qualifying leads from multiple online portals is slow and prone to error.\",\n  \"problemStatementBulletTwo\": \"Delayed response times cause potential buyers to lose interest in a fast-moving market.\",\n  \"problemStatementBulletThree\": \"Top agents are spending more time on administrative follow-up than on closing deals.\",\n  \"aiSystem\": \"Instant Lead Engager\",\n  \"solutionStatement\": \"The Instant Lead Engager is an AI-powered system that immediately responds to, qualifies, and nurtures every new inquiry from your website and real estate portals, 24/7.\",\n  \"solutionStatementBulletOne\": \"Initiates personalized, conversational follow-ups via SMS and email within 90 seconds of an inquiry.\",\n  \"solutionStatementBulletTwo\": \"Asks key qualifying questions to gauge budget, timeline, and interest level.\",\n  \"solutionStatementBulletThree\": \"Schedules appointments with qualified, high-intent buyers directly on your agents' calendars.\",\n  \"whyThisWorks\": \"This system ensures you make a powerful first impression with every potential buyer at the peak of their interest. By automating the initial outreach and qualification, your agents can focus their energy exclusively on warm, vetted leads, dramatically increasing their efficiency and close rate.\",\n  \"workScope\": \"Integration with your primary lead sources (e.g., website, Zillow, Realtor.com), configuration of custom AI conversation scripts, connection to your team's calendars, and a live deployment and training session.\",\n  \"price\": \"$8500\",\n  \"solutionPricingType\": \"one time\",\n  \"50percentDiscount\": \"$4250\",\n  \"upsellOne\": \"Buyer Preference Matcher\",\n  \"upsellOneScope\": \"The Buyer Preference Matcher analyzes lead conversations to automatically match them with properties in your portfolio. It proactively sends listings that fit their stated needs, keeping them engaged and showcasing your inventory.\",\n  \"upsellOneBulletOne\": \"Identifies buyer criteria like price, location, and key features from conversations.\",\n  \"upsellOneBulletTwo\": \"Automatically cross-references your current listings to find the best matches.\",\n  \"upsellOneBulletThree\": \"Increases site visit requests by proactively showing buyers what they want to see.\",\n  \"upsellOnePricing\": \"$4000\",\n  \"upsellOnePricingType\": \"one time\"\n}\n"
      },
      "type": "@n8n/n8n-nodes-langchain.outputParserStructured",
      "typeVersion": 1.3,
      "position": [
        -16,
        1008
      ],
      "id": "f9de77f9-3a60-4393-9045-3d3f16693902",
      "name": "Output Parser"
    },
    {
      "parameters": {
        "url": "={{\n  $('Form').item.json['Website URL'] && $('Form').item.json['Website URL'].trim()\n    ? (\n        /^https?:\\/\\//i.test($('Form').item.json['Website URL'].trim())\n          ? $('Form').item.json['Website URL'].trim()\n          : 'https://' + $('Form').item.json['Website URL'].trim()\n      )\n    : ''\n}}",
        "options": {}
      },
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        -1040,
        784
      ],
      "id": "33868ba2-79a5-48aa-84a1-1c1e86a6b678",
      "name": "visit website"
    },
    {
      "parameters": {
        "html": "={{ $json.data }}",
        "options": {}
      },
      "type": "n8n-nodes-base.markdown",
      "typeVersion": 1,
      "position": [
        -864,
        784
      ],
      "id": "b7ef3447-571a-4b14-a27b-24931bad46f0",
      "name": "Markdown"
    },
    {
      "parameters": {
        "formTitle": "AI Proposal Generator",
        "formDescription": "Instantly craft tailored business proposals with AI. Just enter your details and let our smart system handle the rest — fast, accurate, and ready to impress.",
        "formFields": {
          "values": [
            {
              "fieldLabel": "First Name",
              "placeholder": "Meet",
              "requiredField": true
            },
            {
              "fieldLabel": "Last Name",
              "placeholder": "Patel",
              "requiredField": true
            },
            {
              "fieldLabel": "Company name",
              "placeholder": "XYZ Constructions",
              "requiredField": true
            },
            {
              "fieldLabel": "Email",
              "placeholder": "email@comapny.com",
              "requiredField": true
            },
            {
              "fieldLabel": "Website URL",
              "placeholder": "www.example.com"
            },
            {
              "fieldLabel": "Sales call recording URL",
              "placeholder": "https://drive.google.com/file/d/1RFt5KLTF"
            }
          ]
        },
        "options": {}
      },
      "type": "n8n-nodes-base.formTrigger",
      "typeVersion": 2.2,
      "position": [
        -1376,
        784
      ],
      "id": "d2b451a0-5163-4542-9b54-703e4f45cd84",
      "name": "Form",
      "webhookId": "81552498-ca13-40e8-9ca6-53b24a2a1033"
    }
  ],
  "connections": {
    "Copy file": {
      "main": [
        [
          {
            "node": "visit website",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "has sales call?": {
      "main": [
        [
          {
            "node": "Download sales call",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Make Proposal",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Download sales call": {
      "main": [
        [
          {
            "node": "Transcribe",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Transcribe": {
      "main": [
        [
          {
            "node": "Make Proposal",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Gemini": {
      "ai_languageModel": [
        [
          {
            "node": "Make Proposal",
            "type": "ai_languageModel",
            "index": 0
          }
        ]
      ]
    },
    "Make Proposal": {
      "main": [
        [
          {
            "node": "write proposal",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Download file": {
      "main": [
        [
          {
            "node": "Create a draft",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "write proposal": {
      "main": [
        [
          {
            "node": "Download file",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Output Parser": {
      "ai_outputParser": [
        [
          {
            "node": "Make Proposal",
            "type": "ai_outputParser",
            "index": 0
          }
        ]
      ]
    },
    "visit website": {
      "main": [
        [
          {
            "node": "Markdown",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Markdown": {
      "main": [
        [
          {
            "node": "has sales call?",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Form": {
      "main": [
        [
          {
            "node": "Copy file",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "pinData": {},
  "meta": {
    "templateCredsSetupCompleted": true,
    "instanceId": "023b86b457a9dc285230d548a523bd29bf8a1b2d347562a41abd78b1db45a14d"
  }
}
```
