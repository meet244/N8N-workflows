# 🤖 AI WhatsApp Agent

<img width="1031" height="462" alt="image" src="https://github.com/user-attachments/assets/f689e84f-79bf-46f5-8930-4972a6851693" />

This is a simple yet powerful WhatsApp automation where an AI agent replies to messages using **Google Gemini Chat**. The agent can take on **any role** based on your prompt — from a coach or assistant to a business advisor or support rep.

---

## 🧠 Sample Output

<p float="left">
  <img src="https://github.com/user-attachments/assets/7f64ab91-8342-490e-8062-d4c5d18be6f6" width="45%" />
  <img src="https://github.com/user-attachments/assets/35b30817-5fbf-445f-b188-ccc1751c8c31" width="45%" />
</p>

> These are real outputs from the AI WhatsApp Agent, where the bot acted as a **Travel planner** based on the prompt. The replies are adaptive, contextual, and human-like.

---

## ⚙️ How It Works

1. **WhatsApp Trigger** – Activates when a new message is received.
2. **AI Agent** – Uses:
   - **Google Gemini Chat** as the brain
   - **Simple Memory** to remember past conversations
3. **Send Message** – The AI's response is sent back via WhatsApp.

---

## 💡 What Makes It Special

- Responds **instantly** to incoming WhatsApp messages.
- Adapts to **any role** you define (e.g., mentor, travel agent, support bot).
- Remembers context to maintain fluid conversations.
- Works with real-time AI via Google Gemini.

---

## 🔧 What You Need

- WhatsApp Business API (via Twilio, 360dialog, etc.)
- Google Gemini API access
- An automation platform like n8n

---

# 🧑‍💻 Code

```
{
  "name": "My workflow",
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
        0,
        0
      ],
      "id": "b55fb455-c464-40f8-be12-c744a8ea6b0c",
      "name": "WhatsApp Trigger",
      "webhookId": "32a1da59-e134-484c-af66-0975d78d5846",
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
        656,
        0
      ],
      "id": "e86246f5-4f41-42d3-b14b-71fd1531a112",
      "name": "Send message",
      "webhookId": "37865f05-c499-4336-bd1e-e3641071acb8",
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
        "text": "={{ $json.messages[0].text.body }}",
        "options": {
          "systemMessage": "You are a helpful assistant, Reply me like you're replying on Whatsapp. Don't make the message too long. Reply in a short, concise way."
        }
      },
      "type": "@n8n/n8n-nodes-langchain.agent",
      "typeVersion": 2.1,
      "position": [
        208,
        0
      ],
      "id": "cdb4cc0b-3622-4572-b17f-f9422cbca5bd",
      "name": "AI Agent"
    },
    {
      "parameters": {
        "options": {}
      },
      "type": "@n8n/n8n-nodes-langchain.lmChatGoogleGemini",
      "typeVersion": 1,
      "position": [
        80,
        208
      ],
      "id": "10a9d117-be78-497f-883f-55092dd1c844",
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
        "sessionKey": "={{ $json.metadata.phone_number_id }}",
        "contextWindowLength": 10
      },
      "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow",
      "typeVersion": 1.3,
      "position": [
        224,
        208
      ],
      "id": "1c02c3fd-9ed4-4921-9548-1dae4feee195",
      "name": "Simple Memory"
    }
  ],
  "pinData": {},
  "connections": {
    "WhatsApp Trigger": {
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
    "AI Agent": {
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
    }
  },
  "active": false,
  "settings": {
    "executionOrder": "v1"
  },
  "versionId": "ce73aaa9-8493-440d-981c-7635a7cb2c1b",
  "meta": {
    "templateCredsSetupCompleted": true,
    "instanceId": "fdc3f4073d27a27a358f30bbd32d5b44847be66a94ef1b826c22e9091531b857"
  },
  "id": "2lBXNGRRJ6N1n73t",
  "tags": []
}
```


Built with ❤️ by Meet Patel
