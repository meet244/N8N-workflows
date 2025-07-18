# 🟡 Yellow Pages Lead Generator

<img width="1573" height="415" alt="image (5)" src="https://github.com/user-attachments/assets/45542209-e6e2-4afc-8631-4e55f4293712" />

This automation scrapes business leads from **Yellow Pages** based on any niche and location you choose — like “roofers in New York” — and automatically sends the leads to your **Google Sheet**.

---

## ⚙️ How It Works

1. **Start** – Click "Test workflow".
2. **Enter Details** – Fill in your niche and location (e.g., "roofers", "New York").
3. **URL Generator** – Builds the Yellow Pages search URL.
4. **Scrape** – Pulls business data from Yellow Pages.
5. **AI Extractor** – Uses Google Gemini AI to clean and format the data.
6. **Save to Google Sheets** – Final leads are added to your Sheet.

---

## ✅ What You Get

- Business name  
- Phone number  
- Address  
- Website  
- And more (depends on what’s available)

---

## 🔧 Requirements

- Oxylabs Scraper API access  
- Google Gemini AI access  
- Google Sheets connected

---

## 💡 Use Examples

- **Roofers in New York**  
- **Plumbers in Los Angeles**  
- **Dentists in Miami**

Use any business type + city combo to generate leads.

---

## 🧑‍💻 Code

```
{
  "name": "yellow pages -> sheets",
  "nodes": [
    {
      "parameters": {},
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [
        -1320,
        400
      ],
      "id": "417c48fe-3d30-4094-b379-c84c68004ceb",
      "name": "When clicking ‘Test workflow’"
    },
    {
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "id": "6471a106-2e18-4ca6-980e-a024c4d42be8",
              "name": "website",
              "value": "https://www.yellowpages.com/search?search_terms=Dentists&geo_location_terms=New%20York%2C%20NY",
              "type": "string"
            },
            {
              "id": "a8c416f2-5410-4493-a1ed-d51282566216",
              "name": "pages",
              "value": "3",
              "type": "string"
            }
          ]
        },
        "options": {}
      },
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.4,
      "position": [
        -1040,
        400
      ],
      "id": "f34dcbbb-b095-4949-b8ec-19be79b20794",
      "name": "Website"
    },
    {
      "parameters": {
        "text": "={{ $json.results[0].content }}",
        "schemaType": "manual",
        "inputSchema": "{\n\t\"type\": \"array\",\n\t\"items\": {\n\t\t\"type\": \"object\",\n\t\t\"properties\": {\n\t\t\t\"company_name\": {\n\t\t\t\t\"type\": \"string\"\n\t\t\t},\n\t\t\t\"phone_number\": {\n\t\t\t\t\"type\": \"string\",\n\t\t\t\t\"pattern\": \"^\\\\+?[0-9]{7,15}$\"\n\t\t\t},\n           \"website\": {\n\t\t\t\t\"type\": \"string\"\n\t\t\t},\n\t\t\t\"year_in_business\": {\n\t\t\t\t\"type\": \"number\",\n\t\t\t\t\"minimum\": 0,\n\t\t\t\t\"maximum\": 99\n\t\t\t}\n\t\t}\n\t}\n}\n",
        "options": {
          "systemPromptTemplate": "You are an expert extraction algorithm.\nOnly extract relevant information from the text.\nIf you do not know the value of an attribute asked to extract, you may omit the attribute's value.\nAlways output the data in a json array called results. \nYour goal is to extract all the companies of the page. To do so, you will give: company name, phone number, website, number of years in business, for each result you can find."
        }
      },
      "type": "@n8n/n8n-nodes-langchain.informationExtractor",
      "typeVersion": 1,
      "position": [
        260,
        240
      ],
      "id": "12a4ea8c-f3c0-478d-9f49-b09fed1d1a52",
      "name": "Information Extractor"
    },
    {
      "parameters": {
        "fieldToSplitOut": "output",
        "options": {}
      },
      "type": "n8n-nodes-base.splitOut",
      "typeVersion": 1,
      "position": [
        620,
        240
      ],
      "id": "900a99b2-6c3d-4fe9-a414-035cf9fe1d66",
      "name": "Split Out"
    },
    {
      "parameters": {
        "operation": "append",
        "documentId": {
          "__rl": true,
          "value": "1uap4hvLV7Lr4I0vMK_nmF0LXkAUud_6BxLcVV8lngCw",
          "mode": "list",
          "cachedResultName": "YT Demo",
          "cachedResultUrl": "https://docs.google.com/spreadsheets/d/1uap4hvLV7Lr4I0vMK_nmF0LXkAUud_6BxLcVV8lngCw/edit?usp=drivesdk"
        },
        "sheetName": {
          "__rl": true,
          "value": 1523234638,
          "mode": "list",
          "cachedResultName": "NSheet",
          "cachedResultUrl": "https://docs.google.com/spreadsheets/d/1uap4hvLV7Lr4I0vMK_nmF0LXkAUud_6BxLcVV8lngCw/edit#gid=1523234638"
        },
        "columns": {
          "mappingMode": "defineBelow",
          "value": {
            "Dentist": "={{ $json.company_name }}",
            "phone number": "={{ $json.phone_number }}",
            "website": "={{ $json.website }}"
          },
          "matchingColumns": [],
          "schema": [
            {
              "id": "Dentist",
              "displayName": "Dentist",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true
            },
            {
              "id": "phone number",
              "displayName": "phone number",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true
            },
            {
              "id": "website",
              "displayName": "website",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": false
            },
            {
              "id": "year_in_business",
              "displayName": "year_in_business",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
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
        960,
        500
      ],
      "id": "8c727e94-b0e1-43b9-aac7-2c2ab8d22cc4",
      "name": "Google Sheets",
      "credentials": {
        "googleSheetsOAuth2Api": {
          "id": "AVwoU0GyG4ST2FnC",
          "name": "Google Sheets account"
        }
      }
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://realtime.oxylabs.io/v1/queries",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpBasicAuth",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "Content-Type",
              "value": "application/json"
            }
          ]
        },
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={\n  \"source\": \"universal\",\n  \"url\": \"{{ $json.url }}\"\n}\n\n",
        "options": {}
      },
      "id": "c0e4042b-e1a9-41cd-9c01-52df097e4772",
      "name": "ScrapeWebsite",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        20,
        240
      ],
      "credentials": {
        "httpBasicAuth": {
          "id": "KoZg7xxuNPNti28e",
          "name": "Unnamed credential"
        }
      }
    },
    {
      "parameters": {
        "batchSize": "=1",
        "options": {
          "reset": false
        }
      },
      "type": "n8n-nodes-base.splitInBatches",
      "typeVersion": 3,
      "position": [
        -220,
        400
      ],
      "id": "7bcba922-7e14-4d68-bf4b-aff771fa26f0",
      "name": "Loop Over Items"
    },
    {
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "id": "920c0da2-b882-4504-bdf4-7e697785f028",
              "name": "counter",
              "value": 2,
              "type": "number"
            }
          ]
        },
        "options": {}
      },
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.4,
      "position": [
        -820,
        400
      ],
      "id": "76d017af-f18b-492a-b653-a627d6d77202",
      "name": "init"
    },
    {
      "parameters": {
        "content": "Fill here website and ",
        "height": 280
      },
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        -1100,
        300
      ],
      "id": "1b4cb48f-7c54-458b-b30a-006b663650db",
      "name": "Sticky Note"
    },
    {
      "parameters": {
        "jsCode": "const websiteData = $(\"Website\").all()[0]?.json;\nconst pages = Array.from({ length: websiteData.pages }, (_, i) => i + 1);\nconst urls = pages.map((page) => ({ json: { url: `${websiteData.website}&page=${page}` } }));\n\nreturn urls;\n"
      },
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        -600,
        400
      ],
      "id": "42c44001-4bc9-46b9-a981-511a2cd424bf",
      "name": "generate_URL"
    },
    {
      "parameters": {
        "modelName": "models/gemini-2.5-flash-preview-05-20",
        "options": {}
      },
      "type": "@n8n/n8n-nodes-langchain.lmChatGoogleGemini",
      "typeVersion": 1,
      "position": [
        300,
        460
      ],
      "id": "0b08c8e3-06ab-4cba-96aa-049f2b4a8fd4",
      "name": "Google Gemini Chat Model",
      "credentials": {
        "googlePalmApi": {
          "id": "OfXCih6MCcmMIypL",
          "name": "Google Gemini(PaLM) Api account 2"
        }
      }
    }
  ],
  "pinData": {},
  "connections": {
    "When clicking ‘Test workflow’": {
      "main": [
        [
          {
            "node": "Website",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Website": {
      "main": [
        [
          {
            "node": "init",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Information Extractor": {
      "main": [
        [
          {
            "node": "Split Out",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Split Out": {
      "main": [
        [
          {
            "node": "Google Sheets",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "ScrapeWebsite": {
      "main": [
        [
          {
            "node": "Information Extractor",
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
            "node": "ScrapeWebsite",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Google Sheets": {
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
    "init": {
      "main": [
        [
          {
            "node": "generate_URL",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "generate_URL": {
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
    "Google Gemini Chat Model": {
      "ai_languageModel": [
        [
          {
            "node": "Information Extractor",
            "type": "ai_languageModel",
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
  "versionId": "5e5dcfbf-7555-46c5-9b46-d355a907828c",
  "meta": {
    "templateCredsSetupCompleted": true,
    "instanceId": "023b86b457a9dc285230d548a523bd29bf8a1b2d347562a41abd78b1db45a14d"
  },
  "id": "iKFpF4uV8OysDV6q",
  "tags": []
}
```
