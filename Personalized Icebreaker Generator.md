# ❄️ Personalized Icebreaker Generator for Cold Emails

<img width="1224" height="405" alt="image" src="https://github.com/user-attachments/assets/43bd7f43-1048-4f22-b009-2b75956a4d62" />

This automation helps you craft **highly personalized icebreakers** for cold emails by analyzing each lead's website and generating tailored intro lines using **Google Gemini AI**.

Perfect for outreach campaigns where personalization boosts replies.

---

## ⚙️ How It Works

1. **Start** – Click "Test workflow".
2. **Fetch Data** – Pulls client info from a connected Google Sheet.
3. **Filter** – Removes rows with missing or processed data.
4. **Loop** – Iterates through each client.
5. **Scrape Website** – Visits each client's website to understand what they do.
6. **LLM Processing** – Uses Google Gemini AI to generate a personalized message.
7. **Update Sheet** – Writes the icebreaker back into your Google Sheet.

---

## ✅ What You Get

- A custom-written, smart icebreaker per client.
- Designed to be used as the opening line in your cold emails.
- Helps build instant trust and increase email replies.

---

## 🔧 Requirements

- Google Sheets integration  
- Google Gemini AI access  
- Local scraper endpoint running at `http://127.0.0.1:8000/scrape` (or update with your actual scraper)

---

## 💡 Use Examples

- “Loved how your roofing brand in New York highlights eco-friendly materials!”  
- “Impressed by how you simplify bookkeeping for freelancers on your homepage!”

---

## 🧑‍💻 Code

```
{
  "name": "Personal_icebreaker",
  "nodes": [
    {
      "parameters": {},
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [
        -40,
        0
      ],
      "id": "ebd163e4-7eea-4f1a-8fab-669c83646140",
      "name": "When clicking ‘Test workflow’"
    },
    {
      "parameters": {
        "promptType": "define",
        "text": "=name = {{ $('Loop').item.json['Name'] }}\ncompany name = {{ $('Loop').item.json['Company Name'] }}\nratings = {{ $('Loop').item.json.ratings }}\ntype = \t{{ $('Loop').item.json.type }}\nplace = {{ $('Loop').item.json.location }}\nmobile = {{ $('Loop').item.json.phone }}\t\nWebsite = {{ $('Loop').item.json.website }}\n\nwebsite content - {{ $if($js, $json.content, \"\") }}\n\ngmaps content - {{ $if($json.gmaps_scraped && $json.gmaps_scraped[0].status != \"error\", $json.gmaps_scraped[0].content, \"\") }}\n\nlinkedin content - {{ $if($json.instagram_scraped, $json.instagram_scraped[0].content, \"\") }}\n\ninsta content - {{ $if($json.instagram_scraped, $json.instagram_scraped[0].content, \"\") }}\n\nfb content - {{ $if($json.facebook_scraped, $json.facebook_scraped[0].content, \"\") }}",
        "messages": {
          "messageValues": [
            {
              "message": "=You are an expert cold email copywriter. Your task is to write a hyper-personalized icebreaker (just the opening line) for a cold email. Use the following details to research the person and tailor the icebreaker to their background, achievements, or content. Make it feel like it was written specifically for them by a human and only them. It should show genuine interest and spark curiosity. Also, it must feel like a human has written it particularly and personalized for them. Try to give out a compliment to them, because everybody likes that.\n\nOutput should only be the as follows, no subject line. place data in {} variables\n\n\"Hey {name/company},\n\n{icebreaker}\"\n"
            }
          ]
        }
      },
      "type": "@n8n/n8n-nodes-langchain.chainLlm",
      "typeVersion": 1.5,
      "position": [
        1140,
        20
      ],
      "id": "9e089da8-ec43-45e4-8eec-a5f119fca824",
      "name": "Basic LLM Chain"
    },
    {
      "parameters": {
        "modelName": "models/gemini-2.5-flash",
        "options": {}
      },
      "type": "@n8n/n8n-nodes-langchain.lmChatGoogleGemini",
      "typeVersion": 1,
      "position": [
        1160,
        220
      ],
      "id": "737dd7ef-4a36-401d-af0e-8f16888aa050",
      "name": "Google Gemini Chat Model",
      "credentials": {
        "googlePalmApi": {
          "id": "OfXCih6MCcmMIypL",
          "name": "Google Gemini(PaLM) Api account 2"
        }
      }
    },
    {
      "parameters": {
        "operation": "update",
        "documentId": {
          "__rl": true,
          "value": "1N9rq-L8ecCOc5B2I1NoJcIPbOqTep6VujcbmVPmyBh8",
          "mode": "list",
          "cachedResultName": "leads for AAA",
          "cachedResultUrl": "https://docs.google.com/spreadsheets/d/1N9rq-L8ecCOc5B2I1NoJcIPbOqTep6VujcbmVPmyBh8/edit?usp=drivesdk"
        },
        "sheetName": {
          "__rl": true,
          "value": "gid=0",
          "mode": "list",
          "cachedResultName": "Sheet1",
          "cachedResultUrl": "https://docs.google.com/spreadsheets/d/1N9rq-L8ecCOc5B2I1NoJcIPbOqTep6VujcbmVPmyBh8/edit#gid=0"
        },
        "columns": {
          "mappingMode": "defineBelow",
          "value": {
            "row_number": "={{ $('Loop').item.json.row_number }}",
            "icebreaker": "={{ $json.text }}"
          },
          "matchingColumns": [
            "row_number"
          ],
          "schema": [
            {
              "id": "gmaps",
              "displayName": "gmaps",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": true
            },
            {
              "id": "dentals",
              "displayName": "dentals",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": true
            },
            {
              "id": "ratings",
              "displayName": "ratings",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": true
            },
            {
              "id": "ratings_count",
              "displayName": "ratings_count",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": true
            },
            {
              "id": "C*D",
              "displayName": "C*D",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": true
            },
            {
              "id": "type",
              "displayName": "type",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": true
            },
            {
              "id": "location",
              "displayName": "location",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": true
            },
            {
              "id": "opening",
              "displayName": "opening",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": true
            },
            {
              "id": "phone",
              "displayName": "phone",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": true
            },
            {
              "id": "reviews",
              "displayName": "reviews",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": true
            },
            {
              "id": "website",
              "displayName": "website",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": true
            },
            {
              "id": "icebreaker",
              "displayName": "icebreaker",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true
            },
            {
              "id": "row_number",
              "displayName": "row_number",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "readOnly": true,
              "removed": false
            }
          ],
          "attemptToConvertTypes": false,
          "convertFieldsToString": false
        },
        "options": {}
      },
      "type": "n8n-nodes-base.googleSheets",
      "typeVersion": 4.5,
      "position": [
        1520,
        200
      ],
      "id": "8ccaeac0-2360-4543-97e7-1e44479cb37e",
      "name": "Update icebreaker",
      "credentials": {
        "googleSheetsOAuth2Api": {
          "id": "AVwoU0GyG4ST2FnC",
          "name": "Google Sheets account"
        }
      }
    },
    {
      "parameters": {
        "documentId": {
          "__rl": true,
          "value": "1N9rq-L8ecCOc5B2I1NoJcIPbOqTep6VujcbmVPmyBh8",
          "mode": "list",
          "cachedResultName": "Untitled spreadsheet",
          "cachedResultUrl": "https://docs.google.com/spreadsheets/d/1N9rq-L8ecCOc5B2I1NoJcIPbOqTep6VujcbmVPmyBh8/edit?usp=drivesdk"
        },
        "sheetName": {
          "__rl": true,
          "value": "gid=0",
          "mode": "list",
          "cachedResultName": "Sheet1",
          "cachedResultUrl": "https://docs.google.com/spreadsheets/d/1N9rq-L8ecCOc5B2I1NoJcIPbOqTep6VujcbmVPmyBh8/edit#gid=0"
        },
        "filtersUI": {
          "values": [
            {
              "lookupColumn": "icebreaker",
              "lookupValue": "="
            }
          ]
        },
        "options": {}
      },
      "type": "n8n-nodes-base.googleSheets",
      "typeVersion": 4.5,
      "position": [
        180,
        0
      ],
      "id": "f10e76cf-dd3e-4ca7-bc6a-1ce1cc012e25",
      "name": "Fetch Data",
      "credentials": {
        "googleSheetsOAuth2Api": {
          "id": "AVwoU0GyG4ST2FnC",
          "name": "Google Sheets account"
        }
      }
    },
    {
      "parameters": {
        "options": {}
      },
      "type": "n8n-nodes-base.splitInBatches",
      "typeVersion": 3,
      "position": [
        640,
        0
      ],
      "id": "4269305b-01bd-4c7a-a9fc-1e1921ae8830",
      "name": "Loop"
    },
    {
      "parameters": {
        "method": "POST",
        "url": "=http://127.0.0.1:8000/scrape",
        "sendBody": true,
        "contentType": "multipart-form-data",
        "bodyParameters": {
          "parameters": [
            {
              "name": "url",
              "value": "={{ $json.website }},{{ $json.Linkedin }},{{ $json.Instagram }},{{ $json.gmaps }},{{ $json.FB }}"
            }
          ]
        },
        "options": {}
      },
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        920,
        20
      ],
      "id": "b9a3e110-dccd-4c4e-a1c4-b8b0bc0aa0e0",
      "name": "Scrape Data",
      "onError": "continueRegularOutput"
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
              "id": "d8f1605f-d324-460b-8338-f86e450c5d3d",
              "leftValue": "={{ $json.website }}",
              "rightValue": "",
              "operator": {
                "type": "string",
                "operation": "notEmpty",
                "singleValue": true
              }
            },
            {
              "id": "c027cfe4-8705-434d-bc10-69aeaf9eb0dd",
              "leftValue": "={{ $json.email }}",
              "rightValue": "",
              "operator": {
                "type": "string",
                "operation": "notEmpty",
                "singleValue": true
              }
            },
            {
              "id": "deaa39ad-309e-4888-bbd0-0ec623c59942",
              "leftValue": "={{ $json.email }}",
              "rightValue": "-",
              "operator": {
                "type": "string",
                "operation": "notEquals"
              }
            }
          ],
          "combinator": "and"
        },
        "options": {}
      },
      "type": "n8n-nodes-base.filter",
      "typeVersion": 2.2,
      "position": [
        400,
        0
      ],
      "id": "17688ae2-0ac0-4169-9dd3-b99e637d5b86",
      "name": "Filter"
    }
  ],
  "pinData": {},
  "connections": {
    "When clicking ‘Test workflow’": {
      "main": [
        [
          {
            "node": "Fetch Data",
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
    "Basic LLM Chain": {
      "main": [
        [
          {
            "node": "Update icebreaker",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Update icebreaker": {
      "main": [
        [
          {
            "node": "Loop",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Fetch Data": {
      "main": [
        [
          {
            "node": "Filter",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Loop": {
      "main": [
        [],
        [
          {
            "node": "Scrape Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Scrape Data": {
      "main": [
        [
          {
            "node": "Basic LLM Chain",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Filter": {
      "main": [
        [
          {
            "node": "Loop",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": false,
  "settings": {
    "executionOrder": "v1"
  },
  "versionId": "646672be-5dd3-4445-9560-bf2a4d2144b7",
  "meta": {
    "templateCredsSetupCompleted": true,
    "instanceId": "023b86b457a9dc285230d548a523bd29bf8a1b2d347562a41abd78b1db45a14d"
  },
  "id": "V0pJFvC5u9U8uS0j",
  "tags": []
}
```

---

Built with 🤖 by Meet Patel
