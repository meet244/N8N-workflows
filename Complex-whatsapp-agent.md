Here’s your enhanced and polished **README** with the requested changes:

* ✅ Output images displayed **side by side** and **smaller**.
* ✅ Clear mention that the assistant is **designed for Glossier**, a beauty brand.
* ✅ Polished formatting and minor readability improvements.

---

# 🤖 WhatsApp AI Agent – Smart Media Response Bot (n8n Flow)

<img width="100%" alt="flow-graph" src="https://github.com/user-attachments/assets/03f95710-f047-471c-8ae5-1ce59d6127a9" />

This project is a fully automated AI-driven WhatsApp assistant built using **n8n**. It intelligently handles **text, audio, and image** inputs and replies back via WhatsApp — either in **text** or **AI-generated voice** — using powerful APIs like **Google Gemini**, **Groq (Whisper)**, and **Deepgram**.

This specific flow is tailored to act as a **WhatsApp assistant for Glossier**, a popular U.S.-based beauty and skincare brand.

---

## 🧾 Output Sample

<table>
  <tr>
    <td><img width="300" alt="output-1" src="https://github.com/user-attachments/assets/31daa5aa-c467-4d13-9dd4-29680cd3dc0a" /></td>
    <td><img width="300" alt="output-2" src="https://github.com/user-attachments/assets/44fceb37-0146-4c47-bdc6-b65314a5e55f" /></td>
  </tr>
</table>

---

## 📌 Features

* 🔁 Handles **Text**, **Audio**, and **Image** inputs from WhatsApp
* 🧠 Uses **Google Gemini 2.5** via AI Agent for smart replies
* 🎙️ Converts audio messages to text using **Groq Whisper**
* 🖼️ Analyzes images using **Gemini Vision**
* 🔊 Sends back **voice replies** using **Deepgram TTS**
* 💬 Falls back to **text message** if voice is not required
* 🧠 Supports **memory and context** for better conversation flow

---

## 🧩 Flow Breakdown

### 1. **Trigger: WhatsApp**

* Starts when a new message is received on WhatsApp.
* Message can be text, image, or audio.

---

### 2. **Switch: Message Type Handler**

* Routes the message based on whether it’s:

  * 📄 Text
  * 🔊 Audio
  * 🖼️ Image

---

### 3. **Text Handling**

* Text is sent directly to the AI agent (Gemini) for processing.

---

### 4. **Audio Handling**

* Audio is downloaded, then transcribed using **Groq Whisper**.
* Transcribed text is passed to the AI agent.

---

### 5. **Image Handling**

* Image is downloaded and passed to **Gemini Vision** for analysis.
* The interpreted content is sent to the AI agent.

---

### 6. **AI Agent (Glossier Chat Assistant)**

* Chat agent is customized to act as a support agent for **Glossier**, a modern beauty brand.
* It can:

  * Answer product/order questions
  * Recommend skincare and makeup
  * Track/refund orders
  * Link to relevant pages
  * Escalate to human if needed

---

### 7. **Audio or Text Reply?**

* Based on user preference or context:

  * ✅ If audio: Uses **Deepgram** to convert AI response into voice and sends it as WhatsApp audio.
  * ✅ If text: Sends AI response back as a WhatsApp text message.

---

## 🛠️ APIs Used

| Service                | Purpose                                 |
| ---------------------- | --------------------------------------- |
| **WhatsApp Cloud API** | Message delivery & media handling       |
| **Groq Whisper API**   | Transcribes audio to text               |
| **Gemini 2.5 (Flash)** | Handles AI replies & vision analysis    |
| **Deepgram TTS**       | Converts text to realistic voice output |

---

## 🚀 Use Cases

* 🛍️ AI sales/chat support for e-commerce brands like **Glossier**
* 💬 Smart WhatsApp assistant for product discovery
* 🖼️ Visual Q\&A using image input (e.g. show a product and ask questions)
* 📦 Order tracking and customer service via WhatsApp

---

## 🧠 Personality Prompt (Glossier Support Agent)

The AI is instructed to act like a **warm, friendly Glossier customer support representative**, with the following tone and rules:

> “You are now acting as a WhatsApp Chat Agent for **Glossier**, a modern beauty brand based in the U.S...
>
> 🎯 Help with products, orders, returns
> 💬 Use casual, friendly tone
> 💖 Use emojis sparingly
> 🤫 Never mention you're an AI
> 🕘 Hours: 9 AM – 6 PM EST
> 🌐 Website: [glossier.com](https://www.glossier.com)
> 📦 Tracking: [glossier.com/track](https://www.glossier.com/track)
> 📧 Email: [gTEAM@glossier.com](mailto:gTEAM@glossier.com)”

---

## 🧑‍💻 Code

```
{
  "name": "Complex Whatsapp Agent",
  "nodes": [
    {
      "parameters": {
        "updates": [
          "messages"
        ],
        "options": {}
      },
      "type": "n8n-nodes-base.whatsAppTrigger",
      "typeVersion": 1,
      "position": [
        96,
        80
      ],
      "id": "fa63677d-198c-4a96-a71a-badd76fedf9d",
      "name": "WhatsApp Trigger",
      "webhookId": "d97f2a6f-704c-4fc7-bb57-948974052fb5",
      "credentials": {
        "whatsAppTriggerApi": {
          "id": "Z4Gwwuu5X2QSHDoK",
          "name": "WhatsApp OAuth account"
        }
      }
    },
    {
      "parameters": {
        "operation": "send",
        "phoneNumberId": "753198667869787",
        "recipientPhoneNumber": "+918879109025",
        "textBody": "={{ $json.output }}",
        "additionalFields": {}
      },
      "type": "n8n-nodes-base.whatsApp",
      "typeVersion": 1,
      "position": [
        2080,
        144
      ],
      "id": "6b600978-bfcc-4d17-ac2a-19fde5c74329",
      "name": "Send message",
      "webhookId": "7d5913f3-7cf1-4692-a363-b2a97875b329",
      "credentials": {
        "whatsAppApi": {
          "id": "MyhO83MD9cbAkq2y",
          "name": "WhatsApp account"
        }
      }
    },
    {
      "parameters": {
        "promptType": "define",
        "text": "={{ $json.text }}",
        "options": {
          "systemMessage": "You are now acting as a WhatsApp Chat Agent for Glossier, a modern beauty brand based in the U.S. known for its skincare, makeup, and fragrance products. You will be replying to WhatsApp messages just like a friendly, professional customer support representative. You must sound like a real human — warm, helpful, and never robotic.\n\n🎯 Your Responsibilities:\nAnswer product and order-related questions\n\nRecommend skincare and beauty products based on customer needs\n\nAssist with tracking orders, returns, and refunds\n\nGuide users to the right product pages or promotions\n\nEscalate to a real human agent if needed (only if explicitly requested)\n\nCollect email, full name, and order number (when applicable)\n\n💬 Tone & Style:\nFriendly, conversational, and warm\n\nUse emojis occasionally, like 💖, 😊, or ✨\n\nAvoid being overly formal — this isn’t a corporate tone\n\nAlways use the customer’s name if available\n\nNever mention you are an AI\n\n📌 Glossier Business Info:\n🕘 Business Hours: 9 AM – 6 PM EST, Mon–Fri\n\n🧴 Product Categories: Skincare, Makeup, Fragrance, Body Care\n\n🌐 Website: https://www.glossier.com\n\n🔄 Return Policy: 30-day return on most items\n\n🚚 Shipping Info: Free shipping on orders over $40 in the U.S.\n\n📦 Track Order Page: glossier.com/track\n\n📅 Typical Delivery Time: 3–7 business days\n\n📧 Support Email: gTEAM@glossier.com"
        }
      },
      "type": "@n8n/n8n-nodes-langchain.agent",
      "typeVersion": 2.1,
      "position": [
        1472,
        -32
      ],
      "id": "ea6a7ddc-a99e-4a46-b3ff-59b937f82390",
      "name": "AI Agent"
    },
    {
      "parameters": {
        "options": {}
      },
      "type": "@n8n/n8n-nodes-langchain.lmChatGoogleGemini",
      "typeVersion": 1,
      "position": [
        1472,
        224
      ],
      "id": "b7cfbe1d-fc90-4115-9cb1-0c9bc5ce372c",
      "name": "Google Gemini Chat Model",
      "credentials": {
        "googlePalmApi": {
          "id": "Be4xhnPZFLozqGhc",
          "name": "Google Gemini(PaLM) Api account"
        }
      }
    },
    {
      "parameters": {
        "sessionIdType": "customKey",
        "sessionKey": "={{ $('WhatsApp Trigger').item.json.metadata.phone_number_id }}",
        "contextWindowLength": 10
      },
      "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow",
      "typeVersion": 1.3,
      "position": [
        1600,
        224
      ],
      "id": "471b70d9-2fa0-4ffc-a129-194ed2a9765d",
      "name": "Simple Memory"
    },
    {
      "parameters": {
        "rules": {
          "values": [
            {
              "conditions": {
                "options": {
                  "caseSensitive": true,
                  "leftValue": "",
                  "typeValidation": "strict",
                  "version": 2
                },
                "conditions": [
                  {
                    "leftValue": "={{ $json.messages[0].text.body }}",
                    "rightValue": "",
                    "operator": {
                      "type": "string",
                      "operation": "exists",
                      "singleValue": true
                    },
                    "id": "64ede2c6-932a-4788-8851-c9058f09fd0d"
                  }
                ],
                "combinator": "and"
              },
              "renameOutput": true,
              "outputKey": "text"
            },
            {
              "conditions": {
                "options": {
                  "caseSensitive": true,
                  "leftValue": "",
                  "typeValidation": "strict",
                  "version": 2
                },
                "conditions": [
                  {
                    "id": "4e0ce9b6-7fe1-4460-b3d1-913562cce951",
                    "leftValue": "={{ $json.messages[0].audio }}",
                    "rightValue": "",
                    "operator": {
                      "type": "object",
                      "operation": "exists",
                      "singleValue": true
                    }
                  }
                ],
                "combinator": "and"
              },
              "renameOutput": true,
              "outputKey": "audio"
            },
            {
              "conditions": {
                "options": {
                  "caseSensitive": true,
                  "leftValue": "",
                  "typeValidation": "strict",
                  "version": 2
                },
                "conditions": [
                  {
                    "id": "ed5f7600-8966-4f9c-8069-b40950d9e87e",
                    "leftValue": "={{ $json.messages[0].image }}",
                    "rightValue": "",
                    "operator": {
                      "type": "object",
                      "operation": "exists",
                      "singleValue": true
                    }
                  }
                ],
                "combinator": "and"
              },
              "renameOutput": true,
              "outputKey": "image"
            }
          ]
        },
        "options": {}
      },
      "type": "n8n-nodes-base.switch",
      "typeVersion": 3.2,
      "position": [
        304,
        64
      ],
      "id": "bf5ccb71-2267-4f87-8bd5-60a8ba1ff1e2",
      "name": "Switch"
    },
    {
      "parameters": {
        "resource": "media",
        "operation": "mediaUrlGet",
        "mediaGetId": "={{ $json.messages[0].audio.id }}"
      },
      "type": "n8n-nodes-base.whatsApp",
      "typeVersion": 1,
      "position": [
        576,
        80
      ],
      "id": "fe592449-d073-4c78-9fc8-15d6838e878c",
      "name": "Download URL",
      "webhookId": "41f4a894-a4c9-454a-868a-46524329815e",
      "credentials": {
        "whatsAppApi": {
          "id": "MyhO83MD9cbAkq2y",
          "name": "WhatsApp account"
        }
      }
    },
    {
      "parameters": {
        "url": "={{ $json.url }}",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "options": {}
      },
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        784,
        80
      ],
      "id": "8b375fa7-74c2-466e-a99f-6a5d906be39b",
      "name": "Download Audio",
      "credentials": {
        "httpHeaderAuth": {
          "id": "gXkL56KWdCkaPNmQ",
          "name": "Header Auth account"
        }
      }
    },
    {
      "parameters": {
        "method": "POST",
        "url": "=https://api.groq.com/openai/v1/audio/transcriptions",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "Authorization",
              "value": "Bearer gsk_"
            }
          ]
        },
        "sendBody": true,
        "contentType": "multipart-form-data",
        "bodyParameters": {
          "parameters": [
            {
              "name": "model",
              "value": "whisper-large-v3-turbo"
            },
            {
              "parameterType": "formBinaryData",
              "name": "file",
              "inputDataFieldName": "=data"
            },
            {
              "name": "temperature",
              "value": "0.55"
            }
          ]
        },
        "options": {}
      },
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        992,
        80
      ],
      "id": "37e5009c-4c46-4b91-8a0c-7b2981b725be",
      "name": "groq transcribe"
    },
    {
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "id": "10b1ee54-4009-4691-80ee-e6844800bdc4",
              "name": "text",
              "value": "={{ $json.messages[0].text.body }}",
              "type": "string"
            }
          ]
        },
        "options": {}
      },
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.4,
      "position": [
        576,
        -96
      ],
      "id": "2b5fc0fc-257b-4560-baaf-eaa466a68efd",
      "name": "Edit Fields"
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
              "id": "6c3f00da-0d59-4c35-8cb0-2e595c7460d6",
              "leftValue": "={{ $('WhatsApp Trigger').item.json.messages[0].audio }}",
              "rightValue": "",
              "operator": {
                "type": "object",
                "operation": "exists",
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
        1840,
        -32
      ],
      "id": "4a46d233-4cd2-4259-89fc-f036dcdeaddf",
      "name": "Send Audio?"
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://api.deepgram.com/v1/speak?model=aura-2-iris-en",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "Authorization",
              "value": "Token e114db454cfe5af9f7c103042ab6c6802edb8b00"
            }
          ]
        },
        "sendBody": true,
        "contentType": "raw",
        "rawContentType": "text/plain",
        "body": "={{ $json.output }}",
        "options": {
          "response": {
            "response": {
              "responseFormat": "file"
            }
          }
        }
      },
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        2080,
        -192
      ],
      "id": "1f288c2a-187d-4f5e-b8b6-6332b4351727",
      "name": "Text-to-Speech"
    },
    {
      "parameters": {
        "operation": "send",
        "phoneNumberId": "753198667869787",
        "recipientPhoneNumber": "={{ $('WhatsApp Trigger').item.json.messages[0].from }}",
        "messageType": "audio",
        "mediaPath": "useMedian8n",
        "additionalFields": {}
      },
      "type": "n8n-nodes-base.whatsApp",
      "typeVersion": 1,
      "position": [
        2288,
        -192
      ],
      "id": "ad070cb5-eb82-4ea0-b6a7-9ab5bb609dbe",
      "name": "Send audio",
      "webhookId": "05cb2fa1-bbb3-46f7-b264-13b1db4d924e",
      "credentials": {
        "whatsAppApi": {
          "id": "MyhO83MD9cbAkq2y",
          "name": "WhatsApp account"
        }
      }
    },
    {
      "parameters": {
        "resource": "media",
        "operation": "mediaUrlGet",
        "mediaGetId": "={{ $json.messages[0].image.id }}"
      },
      "type": "n8n-nodes-base.whatsApp",
      "typeVersion": 1,
      "position": [
        576,
        256
      ],
      "id": "8e7cc721-dd72-40eb-b8ea-bd1bedad6258",
      "name": "Download URL1",
      "webhookId": "41f4a894-a4c9-454a-868a-46524329815e",
      "credentials": {
        "whatsAppApi": {
          "id": "MyhO83MD9cbAkq2y",
          "name": "WhatsApp account"
        }
      }
    },
    {
      "parameters": {
        "url": "={{ $json.url }}",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "options": {}
      },
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        784,
        256
      ],
      "id": "7d13e0d2-07a6-4d4f-98dd-90339dfeb530",
      "name": "Download Image",
      "credentials": {
        "httpHeaderAuth": {
          "id": "gXkL56KWdCkaPNmQ",
          "name": "Header Auth account"
        }
      }
    },
    {
      "parameters": {
        "resource": "image",
        "operation": "analyze",
        "modelId": {
          "__rl": true,
          "value": "gpt-4o-mini",
          "mode": "list",
          "cachedResultName": "GPT-4O-MINI"
        },
        "inputType": "base64",
        "options": {}
      },
      "type": "@n8n/n8n-nodes-langchain.openAi",
      "typeVersion": 1.8,
      "position": [
        992,
        256
      ],
      "id": "305a96d1-3aab-44a2-b5e5-24731fd281b3",
      "name": "Analyze image",
      "credentials": {
        "openAiApi": {
          "id": "qgx6Mb8ysKeAP0cS",
          "name": "n8n free OpenAI API credits"
        }
      }
    },
    {
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "id": "236cdbb0-7efc-4392-b1b8-6885c20d5d40",
              "name": "text",
              "value": "=The user has uploaded an image and the image contains following - \n{{ $json.content }}",
              "type": "string"
            }
          ]
        },
        "options": {}
      },
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.4,
      "position": [
        1184,
        256
      ],
      "id": "aa122188-0a37-4af1-8e64-bb1d9db6bbda",
      "name": "Edit Fields1"
    }
  ],
  "pinData": {},
  "connections": {
    "WhatsApp Trigger": {
      "main": [
        [
          {
            "node": "Switch",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "AI Agent": {
      "main": [
        [
          {
            "node": "Send Audio?",
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
            "node": "AI Agent",
            "type": "ai_languageModel",
            "index": 0
          }
        ]
      ]
    },
    "Simple Memory": {
      "ai_memory": [
        [
          {
            "node": "AI Agent",
            "type": "ai_memory",
            "index": 0
          }
        ]
      ]
    },
    "Switch": {
      "main": [
        [
          {
            "node": "Edit Fields",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Download URL",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Download URL1",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Download URL": {
      "main": [
        [
          {
            "node": "Download Audio",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Download Audio": {
      "main": [
        [
          {
            "node": "groq transcribe",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "groq transcribe": {
      "main": [
        [
          {
            "node": "AI Agent",
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
            "node": "AI Agent",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Send Audio?": {
      "main": [
        [
          {
            "node": "Text-to-Speech",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Send message",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Text-to-Speech": {
      "main": [
        [
          {
            "node": "Send audio",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Download URL1": {
      "main": [
        [
          {
            "node": "Download Image",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Download Image": {
      "main": [
        [
          {
            "node": "Analyze image",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Analyze image": {
      "main": [
        [
          {
            "node": "Edit Fields1",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Edit Fields1": {
      "main": [
        [
          {
            "node": "AI Agent",
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
  "versionId": "99607e54-15b3-4cd9-83d5-9c0e1355fb0f",
  "meta": {
    "templateCredsSetupCompleted": true,
    "instanceId": "fdc3f4073d27a27a358f30bbd32d5b44847be66a94ef1b826c22e9091531b857"
  },
  "id": "NWa86LuNg23yxrJ6",
  "tags": []
}
```
