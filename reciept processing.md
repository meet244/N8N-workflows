# 🧾 Automated Receipt & Invoice OCR Processor (n8n Flow)

<img width="100%" alt="n8n-receipt-ocr-flow-diagram" src="https://github.com/user-attachments/assets/ccd3e7b0-6c7d-4984-b957-8c239d80cbad" />

This project is a powerful automation workflow built in **n8n** that completely automates the process of digitizing receipts and invoices. Simply drop a file into a designated **Google Drive** folder, and this system will automatically perform Optical Character Recognition (OCR), extract key details like vendor name, date, and total amount, and save the structured data into a **Google Sheet**.

Designed for individuals and businesses, this workflow eliminates manual data entry, making expense tracking, accounting, and record-keeping effortless and error-free.

-----

## 🧾 Output Sample

The final output is a clean, organized Google Sheet where each row corresponds to a processed receipt, with all key information extracted and a direct link to the original file in Google Drive.

| business\_name | invoice\_number | date | items | total\_paid |
| :--- | :--- | :--- | :--- | :--- |
| QuickMart | INV-1043 | 2024-08-15 | Coffee, Sandwich, Water | 15.75 |
| Tech Solutions Inc. | 2024-033 | 2024-08-14 | Monthly Subscription | 99.00 |
| Office Supplies Co. | 54321 | 2024-08-12 | Pens, Notebooks, Paper | 45.50 |

-----

## 📌 Features

  * 📂 **Automatic File Trigger**: Activates whenever a new file is added to a specific **Google Drive** folder.
  * 👀 **Powerful OCR Engine**: Uses an external OCR API to accurately scan and extract text from images or PDF files (receipts/invoices).
  * 🤖 **Intelligent Data Extraction**: Automatically identifies and parses key fields such as business name, date, invoice number, line items, and total amount paid.
  * 📊 **Structured Data Output**: Organizes the extracted information and saves it in a clean, structured format in a **Google Sheet**.
  * 🧠 **Prevents Duplicates**: Checks the Google Sheet to ensure that it doesn't process the same file twice.
  * 🔄 **Manual & Automated Runs**: Can be triggered manually to process a whole folder or run automatically for new files.

-----

## 🧩 Flow Breakdown

### 1\. **Trigger: New File in Google Drive**

  * The workflow starts in one of two ways:
      * **Automatically**: The `On new file in Google Drive` node triggers the moment a new receipt is uploaded.
      * **Manually**: The `When clicking 'Test workflow'` button can be used to process all unprocessed files in the folder at once.

-----

### 2\. **Load and Filter Files**

  * **Load Files**: It fetches a list of all files from the designated "receipts" folder in Google Drive.
  * **Get Processed Rows**: Simultaneously, it reads the Google Sheet to get a list of receipts that have already been processed.
  * **Filter Processed Files**: A `Merge` node compares the two lists and filters out any files that have already been logged, ensuring each receipt is processed only once.

-----

### 3\. **Perform OCR and Extract Data**

  * **Download File**: The workflow downloads the new, unprocessed receipt file from Google Drive.
  * **OCR Recognize**: An `HTTP Request` node sends the file to a specialized **Receipt & Invoice OCR API**, which scans the document and returns the extracted text data.
  * **Unserialize JSON**: The OCR API's response is a JSON string. A `Code` node parses this string into a structured JSON object that n8n can easily work with.

-----

### 4\. **Save Result to Google Sheets**

  * **Save OCR Result**: The final, structured data is appended as a new row in the target **Google Sheet**. Key fields like business name, total paid, items, and a direct link back to the original file in Google Drive are mapped to the appropriate columns.

-----

## 🛠️ APIs & Services Used

| Service | Purpose |
| :--- | :--- |
| **Google Drive API** | To monitor for new files and download them for processing. |
| **Receipt & Invoice OCR API** | Performs Optical Character Recognition to extract data from files. |
| **Google Sheets API**| Serves as the database to store and organize the final extracted data. |

-----

## 🚀 Use Cases

  * 💼 **Automated Expense Tracking**: Perfect for freelancers or employees who need to track business expenses without manual data entry.
  * 🧾 **Small Business Accounting**: Streamline the process of digitizing supplier invoices and receipts for bookkeeping.
  * 🏡 **Personal Finance Management**: Easily keep a digital record of household bills and receipts for budgeting.
  * 📈 **Data Collection**: Quickly convert stacks of physical documents into a structured digital format for analysis.

-----

## 🧑‍💻 Code

\<details\>
\<summary\>Click to view the n8n workflow JSON\</summary\>

```json
{
  "nodes": [
    {
      "parameters": {},
      "id": "a39a371b-f984-4ad9-954b-eca6b74685f1",
      "name": "When clicking ‘Test workflow’",
      "type": "n8n-nodes-base.manualTrigger",
      "position": [
        0,
        0
      ],
      "typeVersion": 1
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://receipt-and-invoice-ocr-api.p.rapidapi.com/recognize",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "x-rapidapi-host",
              "value": "receipt-and-invoice-ocr-api.p.rapidapi.com"
            },
            {
              "name": "x-rapidapi-key",
              "value": ""
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
              "name": "settings",
              "value": "{ \"documentType\": \"invoice\" }"
            }
          ]
        },
        "options": {}
      },
      "id": "8abe3741-98a6-421e-908d-55b8b0210cd6",
      "name": "OCR recognize",
      "type": "n8n-nodes-base.httpRequest",
      "position": [
        1168,
        224
      ],
      "typeVersion": 4.2
    },
    {
      "parameters": {
        "jsCode": "// Loop over input items and add a new field called 'myNewField' to the JSON of each one\nfor (const item of $input.all()) {\n  item.json.parsedData = JSON.parse(item.json.result.data);\n}\n\nreturn $input.all();"
      },
      "id": "e726fb10-b67d-4f4d-b97b-4c3a292318cb",
      "name": "Unserialize response JSON",
      "type": "n8n-nodes-base.code",
      "position": [
        1392,
        224
      ],
      "typeVersion": 2
    },
    {
      "parameters": {
        "pollTimes": {
          "item": [
            {
              "mode": "everyMinute"
            }
          ]
        },
        "triggerOn": "specificFolder",
        "folderToWatch": {
          "__rl": true,
          "value": "15HXJQOiuFL6DdoNjwhPD6FX_hkkZEWhm",
          "mode": "list",
          "cachedResultName": "reciepts",
          "cachedResultUrl": "https://drive.google.com/drive/folders/15HXJQOiuFL6DdoNjwhPD6FX_hkkZEWhm"
        },
        "event": "fileCreated",
        "options": {}
      },
      "id": "d7c7fc99-b2bd-4dde-bd18-8efe49af28cf",
      "name": "On new file in Google Drive",
      "type": "n8n-nodes-base.googleDriveTrigger",
      "position": [
        0,
        352
      ],
      "typeVersion": 1,
      "credentials": {
        "googleDriveOAuth2Api": {
          "id": "LZ6gnq6e2551KE90",
          "name": "Google Drive account"
        }
      }
    },
    {
      "parameters": {
        "resource": "fileFolder",
        "returnAll": true,
        "filter": {
          "folderId": {
            "__rl": true,
            "value": "15HXJQOiuFL6DdoNjwhPD6FX_hkkZEWhm",
            "mode": "list",
            "cachedResultName": "reciepts",
            "cachedResultUrl": "https://drive.google.com/drive/folders/15HXJQOiuFL6DdoNjwhPD6FX_hkkZEWhm"
          }
        },
        "options": {}
      },
      "id": "996d3add-1d9a-4dec-a631-932128cc5d92",
      "name": "Load files from Google Drive folder",
      "type": "n8n-nodes-base.googleDrive",
      "position": [
        384,
        352
      ],
      "executeOnce": true,
      "typeVersion": 3,
      "credentials": {
        "googleDriveOAuth2Api": {
          "id": "LZ6gnq6e2551KE90",
          "name": "Google Drive account"
        }
      }
    },
    {
      "parameters": {
        "mode": "combine",
        "fieldsToMatchString": "id",
        "joinMode": "keepNonMatches",
        "outputDataFrom": "input2",
        "options": {}
      },
      "id": "afbbc371-5167-4e4c-9dca-a161a84e9434",
      "name": "Filter processed files",
      "type": "n8n-nodes-base.merge",
      "position": [
        704,
        224
      ],
      "typeVersion": 3
    },
    {
      "parameters": {
        "operation": "download",
        "fileId": {
          "__rl": true,
          "mode": "id",
          "value": "={{ $json.id }}"
        },
        "options": {}
      },
      "id": "b1e85229-c733-4788-a9ed-219fe46ca19d",
      "name": "Download file for OCR",
      "type": "n8n-nodes-base.googleDrive",
      "position": [
        944,
        224
      ],
      "typeVersion": 3,
      "credentials": {
        "googleDriveOAuth2Api": {
          "id": "LZ6gnq6e2551KE90",
          "name": "Google Drive account"
        }
      }
    },
    {
      "parameters": {
        "operation": "appendOrUpdate",
        "documentId": {
          "__rl": true,
          "value": "1c04RBa_gL0puzW140v_4GmLXnxawysT44TjJ7xtvkx8",
          "mode": "list",
          "cachedResultName": "temp",
          "cachedResultUrl": "https://docs.google.com/spreadsheets/d/1c04RBa_gL0puzW140v_4GmLXnxawysT44TjJ7xtvkx8/edit?usp=drivesdk"
        },
        "sheetName": {
          "__rl": true,
          "value": 1808085700,
          "mode": "list",
          "cachedResultName": "reciept processing",
          "cachedResultUrl": "https://docs.google.com/spreadsheets/d/1c04RBa_gL0puzW140v_4GmLXnxawysT44TjJ7xtvkx8/edit#gid=1808085700"
        },
        "columns": {
          "mappingMode": "defineBelow",
          "value": {
            "business_name": "={{ $json.parsedData.from.company_name }}",
            "total_paid": "={{ $json.parsedData.total_paid }}",
            "items": "={{ $json.parsedData.lines.map(line => line.descr).join(', ')}}\n",
            "pay_split": "={{ $json.parsedData.lines.map(line => line.unit_cost).join('+')}}",
            "date": "={{ $json.parsedData.issued_at }}",
            "invoice_number": "={{ $json.parsedData.invoice_number }}",
            "reciept_link": "=https://drive.google.com/file/d/{{ $('Download file for OCR').item.json.id }}/view?usp=sharing"
          },
          "matchingColumns": [
            "reciept_link"
          ],
          "schema": [
            {
              "id": "business_name",
              "displayName": "business_name",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": false
            },
            {
              "id": "reciept_link",
              "displayName": "reciept_link",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": false
            },
            {
              "id": "invoice_number",
              "displayName": "invoice_number",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": false
            },
            {
              "id": "date",
              "displayName": "date",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": false
            },
            {
              "id": "items",
              "displayName": "items",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": false
            },
            {
              "id": "pay_split",
              "displayName": "pay_split",
              "required": false,
              "defaultMatch": false,
              "display": true,
              "type": "string",
              "canBeUsedToMatch": true,
              "removed": false
            },
            {
              "id": "total_paid",
              "displayName": "total_paid",
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
      "id": "b0e61536-dd0b-4034-957a-72e7348d644c",
      "name": "Save OCR result into Sheets",
      "type": "n8n-nodes-base.googleSheets",
      "position": [
        1600,
        224
      ],
      "typeVersion": 4.3,
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
          "value": "1c04RBa_gL0puzW140v_4GmLXnxawysT44TjJ7xtvkx8",
          "mode": "list",
          "cachedResultName": "temp",
          "cachedResultUrl": "https://docs.google.com/spreadsheets/d/1c04RBa_gL0puzW140v_4GmLXnxawysT44TjJ7xtvkx8/edit?usp=drivesdk"
        },
        "sheetName": {
          "__rl": true,
          "value": 1808085700,
          "mode": "list",
          "cachedResultName": "reciept processing",
          "cachedResultUrl": "https://docs.google.com/spreadsheets/d/1c04RBa_gL0puzW140v_4GmLXnxawysT44TjJ7xtvkx8/edit#gid=1808085700"
        },
        "filtersUI": {
          "values": [
            {
              "lookupColumn": "reciept_link",
              "lookupValue": "=https://drive.google.com/file/d/{{$json.id}}/view?usp=sharing"
            }
          ]
        },
        "options": {}
      },
      "id": "ec253fb3-1a20-430c-9de4-40fd6ddc03b0",
      "name": "Get already processed rows from Sheets",
      "type": "n8n-nodes-base.googleSheets",
      "position": [
        384,
        0
      ],
      "executeOnce": true,
      "typeVersion": 4.3,
      "alwaysOutputData": true,
      "credentials": {
        "googleSheetsOAuth2Api": {
          "id": "AVwoU0GyG4ST2FnC",
          "name": "Google Sheets account"
        }
      }
    },
    {
      "parameters": {
        "content": "https://drive.google.com/drive/u/0/folders/15HXJQOiuFL6DdoNjwhPD6FX_hkkZEWhm"
      },
      "type": "n8n-nodes-base.stickyNote",
      "position": [
        688,
        32
      ],
      "typeVersion": 1,
      "id": "4d03f330-1d6d-4468-a6f4-f4370045995b",
      "name": "Sticky Note"
    }
  ],
  "connections": {
    "When clicking ‘Test workflow’": {
      "main": [
        [
          {
            "node": "Load files from Google Drive folder",
            "type": "main",
            "index": 0
          },
          {
            "node": "Get already processed rows from Sheets",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "OCR recognize": {
      "main": [
        [
          {
            "node": "Unserialize response JSON",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Unserialize response JSON": {
      "main": [
        [
          {
            "node": "Save OCR result into Sheets",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "On new file in Google Drive": {
      "main": [
        [
          {
            "node": "Get already processed rows from Sheets",
            "type": "main",
            "index": 0
          },
          {
            "node": "Load files from Google Drive folder",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Load files from Google Drive folder": {
      "main": [
        [
          {
            "node": "Filter processed files",
            "type": "main",
            "index": 1
          }
        ]
      ]
    },
    "Filter processed files": {
      "main": [
        [
          {
            "node": "Download file for OCR",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Download file for OCR": {
      "main": [
        [
          {
            "node": "OCR recognize",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Get already processed rows from Sheets": {
      "main": [
        [
          {
            "node": "Filter processed files",
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

\</details\>
