# 🤖 AI On-Brand Article Generator (n8n Flow)

<img width="100%" alt="n8n-ai-blog-writer-flow-diagram" src="https://github.com/user-attachments/assets/ff12ab9e-b595-440e-bcc7-dd3969182559" />

This project is a sophisticated content generation pipeline, built in **n8n**, that functions as an AI-powered ghostwriter. The workflow automatically scrapes and analyzes existing articles from a blog to learn its unique **structure, writing style, and brand voice**. It then uses these insights to generate entirely new, on-brand articles and saves them as drafts in **WordPress** for human review.

This automation is perfect for content teams looking to scale their output while maintaining a high degree of brand consistency across all published materials.

-----

## 🧾 Output Sample

The workflow produces a complete, well-structured article draft in WordPress, ready for a final human touch before publishing.

> #### **New Draft Created in WordPress**
>
> **Title:** A Guide to AI-Powered Document Classification
>
> **Body:**
> In today's data-driven world, businesses are drowning in documents. From invoices and contracts to customer feedback and reports, managing this influx of information is a monumental task. Traditional methods are slow, error-prone, and simply can't keep up. This is where AI-powered document classification and extraction come in, offering a transformative solution.
>
> **Why Vision Models Outperform Traditional OCR**
>
> For years, Optical Character Recognition (OCR) was the go-to for digitizing documents. However, it often struggles with complex layouts, varied fonts, and imperfect scans. Modern vision models...
>
> *[...continue reading]*

-----

## 📌 Features

  * 🔎 **Scrapes Existing Content**: Automatically fetches the latest articles from any target blog to use as a style reference.
  * 🧠 **Dual AI Analysis**: Uses **Google Gemini** to perform two distinct analyses:
      * One AI call identifies the **structural and stylistic patterns** of the content.
      * Another call extracts the **brand voice characteristics**, tone, and specific language choices.
  * ✍️ **On-Brand Content Generation**: Combines the style and voice analyses to create a detailed "master prompt" for generating new articles.
  * 📝 **HTML to Markdown Conversion**: Cleans and converts raw HTML into Markdown for more efficient and accurate processing by the AI.
  * 💾 **Seamless WordPress Integration**: Automatically saves the final, AI-written article as a draft in your WordPress site.
  * 🔄 **Adaptable & Reusable**: Can be adapted to use other sources like PDFs or internal documents as the knowledge base.

-----

## 🧩 Flow Breakdown

### 1\. **Import Existing Content**

  * The workflow is triggered and begins by scraping the five latest articles from a specified blog (in this case, `blog.n8n.io`).
  * It extracts the URL for each article and then fetches the full HTML content of each page.

-----

### 2\. **Convert HTML to Markdown**

  * The raw HTML of each article's body is extracted and converted into clean **Markdown**. This optimizes the content for the AI, reducing token usage and preserving the essential structure.

-----

### 3\. **AI-Powered Style & Voice Analysis**

  * The Markdown content of all five articles is sent to **Google Gemini** in two parallel steps:
      * **Analyze Structure & Writing Style**: The first AI model is prompted to describe the common structure, layout, and writing style of the articles as a whole.
      * **Extract Brand Voice**: The second AI model is tasked with identifying and defining the specific "brand voice" characteristics, providing examples of tone and language from the text.

-----

### 4\. **Generate New On-Brand Article**

  * The analyses from the previous two steps are combined with a new article instruction (e.g., "Write a guide on AI for document classification").
  * This comprehensive brief is sent to a final **Google Gemini** model, which acts as a blog writer, using the provided guidelines to draft a completely new article that matches the brand's style and voice.

-----

### 5\. **Save Draft to WordPress**

  * The title and body of the newly generated article are sent to **WordPress** via its API.
  * The article is saved as a **draft**, allowing a human editor to review, validate, and schedule it for publishing.

-----

## 🛠️ APIs & Services Used

| Service | Purpose |
| :--- | :--- |
| **n8n HTTP Request** | Scrapes the initial blog content from the web. |
| **Google Gemini API** | Performs all AI analysis and content generation tasks. |
| **WordPress API**| Creates a new draft post with the AI-generated content. |
| **Google Docs API**| (Optional) Saves the generated article to a Google Doc. |

-----

## 🚀 Use Cases

  * 📈 **Scale Content Marketing**: Rapidly increase the volume of blog posts without sacrificing brand consistency.
  * 💡 **Generate First Drafts**: Provide your content writers with high-quality, on-brand first drafts, significantly speeding up their workflow.
  * 👔 **Onboard New Writers**: Use the AI-generated style guide to quickly train new writers on your brand's voice and tone.
  * 🔄 **Content Repurposing**: Feed the workflow with transcripts or documents to automatically convert them into blog-style articles.

-----

## 🧠 AI Analysis & Generation Prompts

The workflow uses a multi-step prompting strategy to achieve its on-brand output:

> **1. Style Analysis Prompt:**
> "Given the following...articles..., describe how best one could replicate the common structure, layout, language and writing styles of all as aggregate."
>
> **2. Brand Voice Prompt:**
> "Using the given content...extract all voice characteristics from it along with description and examples demonstrating it."
>
> **3. Final Generation Prompt:**
> "You are a blog content writer who writes using the following article guidelines... Write a content piece as requested by the user... Here are the brand voice characteristic and examples you must adopt..."

-----

## 🧑‍💻 Code

\<details\>
\<summary\>Click to view the n8n workflow JSON\</summary\>

```json
{
  "nodes": [
    {
      "parameters": {},
      "id": "c39b37a9-2f50-4daa-874b-af2f88d47949",
      "name": "When clicking ‘Test workflow’",
      "type": "n8n-nodes-base.manualTrigger",
      "position": [
        1552,
        2752
      ],
      "typeVersion": 1
    },
    {
      "parameters": {
        "url": "https://blog.n8n.io",
        "options": {}
      },
      "id": "0e998fa9-79d1-4d98-aba1-24b893b06e40",
      "name": "Get Blog",
      "type": "n8n-nodes-base.httpRequest",
      "position": [
        1792,
        2752
      ],
      "typeVersion": 4.2
    },
    {
      "parameters": {
        "url": "=https://blog.n8n.io{{ $json.article }}",
        "options": {}
      },
      "id": "a9fcf6d7-bd92-435e-b12a-1b8866309466",
      "name": "Get Article",
      "type": "n8n-nodes-base.httpRequest",
      "position": [
        2432,
        2752
      ],
      "typeVersion": 4.2
    },
    {
      "parameters": {
        "operation": "extractHtmlContent",
        "extractionValues": {
          "values": [
            {
              "key": "article",
              "cssSelector": ".item.post a.global-link",
              "returnValue": "attribute",
              "attribute": "href",
              "returnArray": true
            }
          ]
        },
        "options": {}
      },
      "id": "17b4889e-b7bf-4f4e-9d56-641c5df1665d",
      "name": "Extract Article URLs",
      "type": "n8n-nodes-base.html",
      "position": [
        1952,
        2752
      ],
      "typeVersion": 1.2
    },
    {
      "parameters": {
        "fieldToSplitOut": "article",
        "options": {}
      },
      "id": "31d7a28a-6c0a-44d3-af14-0246adf88aad",
      "name": "Split Out URLs",
      "type": "n8n-nodes-base.splitOut",
      "position": [
        2112,
        2752
      ],
      "typeVersion": 1
    },
    {
      "parameters": {
        "maxItems": 5
      },
      "id": "ba89e84e-ea2c-4702-8565-9c79dc718cf7",
      "name": "Latest Articles",
      "type": "n8n-nodes-base.limit",
      "position": [
        2272,
        2752
      ],
      "typeVersion": 1
    },
    {
      "parameters": {
        "operation": "extractHtmlContent",
        "extractionValues": {
          "values": [
            {
              "key": "data",
              "cssSelector": ".post-section",
              "returnValue": "html"
            }
          ]
        },
        "options": {}
      },
      "id": "d39db9bd-be06-43ea-91b1-7284798491a4",
      "name": "Extract Article Content",
      "type": "n8n-nodes-base.html",
      "position": [
        2592,
        2752
      ],
      "typeVersion": 1.2
    },
    {
      "parameters": {
        "fieldsToAggregate": {
          "fieldToAggregate": [
            {
              "fieldToAggregate": "data"
            }
          ]
        },
        "options": {
          "mergeLists": true
        }
      },
      "id": "1ea9d7d0-d877-421d-9fd9-5647375e27c5",
      "name": "Combine Articles",
      "type": "n8n-nodes-base.aggregate",
      "position": [
        3088,
        2752
      ],
      "typeVersion": 1
    },
    {
      "parameters": {
        "mode": "combine",
        "combineBy": "combineByPosition",
        "options": {}
      },
      "id": "b6ab1889-d475-4e5d-b6fd-cda8717492bb",
      "name": "Article Style & Brand Voice",
      "type": "n8n-nodes-base.merge",
      "position": [
        3968,
        2576
      ],
      "typeVersion": 3
    },
    {
      "parameters": {
        "title": "={{ $json.output.title }}",
        "additionalFields": {
          "content": "={{ $json.output.body }}",
          "slug": "={{ $json.output.title.toSnakeCase() }}",
          "status": "draft",
          "format": "standard"
        }
      },
      "id": "b16ae3bb-5f90-4839-8793-9ce5103051e1",
      "name": "Save as Draft",
      "type": "n8n-nodes-base.wordpress",
      "position": [
        5024,
        2576
      ],
      "typeVersion": 1,
      "credentials": {
        "wordpressApi": {
          "id": "4oU6LhklN3TISDQN",
          "name": "Wordpress account"
        }
      }
    },
    {
      "parameters": {
        "html": "={{ $json.data }}",
        "options": {}
      },
      "id": "14f60d3e-517f-4c7e-a158-51f704e803ed",
      "name": "Markdown",
      "type": "n8n-nodes-base.markdown",
      "position": [
        2896,
        2752
      ],
      "typeVersion": 1
    },
    {
      "parameters": {
        "content": "## 6. Save Draft to Wordpress\n[Learn more about the Wordpress node](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.wordpress/)\n\nTo close out the template, we'll simple save our generated article as a draft which could allow human team members to review and validate the article before publishing.",
        "height": 173,
        "width": 406,
        "color": 7
      },
      "id": "363ff572-2865-48e0-8d4f-79b02c973f0a",
      "name": "Sticky Note6",
      "type": "n8n-nodes-base.stickyNote",
      "position": [
        4592,
        2800
      ],
      "typeVersion": 1
    },
    {
      "parameters": {
        "content": "### Q. Can I use other media than blog articles?\nA. Yes! This approach can use other source materials such as PDFs, as long as they can be produces in a text format to give to the LLM.",
        "height": 120,
        "width": 380,
        "color": 5
      },
      "id": "9b09d5fa-e688-4a98-895f-84f2c4cdbc06",
      "name": "Sticky Note7",
      "type": "n8n-nodes-base.stickyNote",
      "position": [
        2320,
        2928
      ],
      "typeVersion": 1
    },
    {
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "id": "2c7e2a28-30f9-4533-a394-a5e967ebf4ec",
              "name": "instruction",
              "type": "string",
              "value": "=Write a comprehensive guide on using AI for document classification and document extraction. Explain the benefits of using vision models over traditional OCR. Close out with a recommendation of using n8n as the preferred way to get started with this AI use-case."
            }
          ]
        },
        "options": {}
      },
      "id": "7821a027-163d-42c2-b278-cbe9d3d1543b",
      "name": "New Article Instruction",
      "type": "n8n-nodes-base.set",
      "position": [
        4224,
        2576
      ],
      "typeVersion": 3.4
    },
    {
      "parameters": {
        "content": "## 1. Import Existing Content\n[Read more about the HTML node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.html/)\n\nFirst, we'll need to gather existing content for the brand voice we want to replicate. This content can be blogs, social media posts or internal documents - the idea is to use this content to \"train\" our AI to produce content from the provided examples. One call out is that the quality and consistency of the content is important to get the desired results.\n\nIn this demonstration, we'll grab the latest blog posts off a corporate blog to use as an example. Since, the blog articles are likely consistent because of the source and narrower focus of the medium, it'll serve well to showcase this workflow.",
        "height": 264,
        "width": 606,
        "color": 7
      },
      "id": "36b5ae79-f8e0-4469-8d62-584ab02d34ce",
      "name": "Sticky Note9",
      "type": "n8n-nodes-base.stickyNote",
      "position": [
        1936,
        2448
      ],
      "typeVersion": 1
    },
    {
      "parameters": {
        "content": "## 2. Convert HTML to Markdown\n[Learn more about the Markdown node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.markdown)\n\nMarkdown is a great way to optimise the article data we're sending to the LLM because it reduces the amount of tokens required but keeps all relevant writing structure information.\n\nAlso useful to get Markdown output as a response because typically it's the format authors will write in.",
        "height": 230,
        "width": 434,
        "color": 7
      },
      "id": "404ee608-4bf3-4cc3-b9c6-37b3890a0c22",
      "name": "Sticky Note10",
      "type": "n8n-nodes-base.stickyNote",
      "position": [
        2704,
        2496
      ],
      "typeVersion": 1
    },
    {
      "parameters": {
        "content": "## 3. Using AI to Analyse Article Structure and Writing Styles\n[Read more about the Basic LLM Chain node](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.chainllm)\n\nOur approach is to first perform a high-level analysis of all available articles in order to replicate their content layout and writing styles. This will act as a guideline to help the AI to structure our future articles.",
        "height": 233,
        "width": 446,
        "color": 7
      },
      "id": "f298123a-e60e-4dd7-978b-f3a4289ec1f4",
      "name": "Sticky Note11",
      "type": "n8n-nodes-base.stickyNote",
      "position": [
        3232,
        2320
      ],
      "typeVersion": 1
    },
    {
      "parameters": {
        "content": "## 4. Using AI to Extract Voice Characteristics and Traits\n[Read more about the Information Extractor node](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.information-extractor/)\n\nSecond, we'll use AI to analysis the brand voice characteristics of the previous articles. This picks out the tone, style and choice of language used and identifies them into categories. These categories will be used as guidelines for the AI to keep the future article consistent in tone and voice. ",
        "height": 253,
        "width": 446,
        "color": 7
      },
      "id": "7ab9e501-f901-4ade-995a-5d14e5edf9ec",
      "name": "Sticky Note12",
      "type": "n8n-nodes-base.stickyNote",
      "position": [
        3392,
        2992
      ],
      "typeVersion": 1
    },
    {
      "parameters": {
        "content": "## 5. Automate On-Brand Articles Using AI\n[Read more about the Information Extractor node](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.information-extractor)\n\nFinally with this approach, we can feed both content and voice guidelines into our final LLM - our content generation agent - to produce any number of on-brand articles, social media posts etc.\n\nWhen it comes to assessing the output, note the AI does a pretty good job at simulating format and reusing common phrases and wording for the target article. However, this could become repetitive very quickly! Whilst AI can help speed up the process, a human touch may still be required to add a some variety.",
        "height": 633,
        "width": 626,
        "color": 7
      },
      "id": "7ea353dd-62a7-41ff-8144-d4d004ef639c",
      "name": "Sticky Note13",
      "type": "n8n-nodes-base.stickyNote",
      "position": [
        3904,
        2256
      ],
      "typeVersion": 1
    },
    {
      "parameters": {
        "content": "### Q. Do I need to analyse Brand Voice for every article?\nA. No! I would recommend storing the results of the AI's analysis and re-use for a list of planned articles rather than generate anew every time.",
        "height": 120,
        "width": 440,
        "color": 5
      },
      "id": "216fc7b4-e08d-488b-9a40-18e96c2e4ace",
      "name": "Sticky Note14",
      "type": "n8n-nodes-base.stickyNote",
      "position": [
        4000,
        2912
      ],
      "typeVersion": 1
    },
    {
      "parameters": {
        "modelId": {
          "__rl": true,
          "value": "models/gemini-2.5-flash",
          "mode": "list",
          "cachedResultName": "models/gemini-2.5-flash"
        },
        "messages": {
          "values": [
            {
              "content": "=### Analyse the given content\n\n{{ $json.data.map(item => item.replace(/\\n/g, '')).join('\\n---\\n') }}"
            }
          ]
        },
        "jsonOutput": true,
        "options": {
          "systemMessage": "You help identify and define a company or individual's \"brand voice\". Using the given content belonging to the company or individual, extract all voice characteristics from it along with description and examples demonstrating it."
        }
      },
      "type": "@n8n/n8n-nodes-langchain.googleGemini",
      "typeVersion": 1,
      "position": [
        3424,
        2800
      ],
      "id": "aedbcb9e-b2d2-4023-9c58-cbc3d9a3c496",
      "name": "Message a model6",
      "credentials": {
        "googlePalmApi": {
          "id": "gQgC07v7jtToYr9F",
          "name": "Gemini meet2005pokar3-1"
        }
      }
    },
    {
      "parameters": {
        "modelId": {
          "__rl": true,
          "value": "models/gemini-2.5-flash",
          "mode": "list",
          "cachedResultName": "models/gemini-2.5-flash"
        },
        "messages": {
          "values": [
            {
              "content": "={{ $json.data.join('\\n---\\n') }}"
            }
          ]
        },
        "jsonOutput": true,
        "options": {
          "systemMessage": "Given the following one or more articles (which are separated by ---), describe how best one could replicate the common structure, layout, language and writing styles of all as aggregate."
        }
      },
      "type": "@n8n/n8n-nodes-langchain.googleGemini",
      "typeVersion": 1,
      "position": [
        3424,
        2608
      ],
      "id": "59f039ae-06ce-47ef-8eb9-988df71674d0",
      "name": "Message a model7",
      "credentials": {
        "googlePalmApi": {
          "id": "gQgC07v7jtToYr9F",
          "name": "Gemini meet2005pokar3-1"
        }
      }
    },
    {
      "parameters": {
        "modelId": {
          "__rl": true,
          "value": "models/gemini-2.5-flash",
          "mode": "list",
          "cachedResultName": "models/gemini-2.5-flash"
        },
        "messages": {
          "values": [
            {}
          ]
        },
        "options": {
          "systemMessage": "=You are a blog content writer who writes using the following article guidelines. Write a content piece as requested by the user. Output the body as Markdown. Do not include the date of the article because the publishing date is not determined yet.\n\n## Brand Article Style\n{{ $('Article Style & Brand Voice').item.json.text }}\n\n##n Brand Voice Characteristics\n\nHere are the brand voice characteristic and examples you must adopt in your piece. Pick only the characteristic which make sense for the user's request. Try to keep it as similar as possible but don't copy word for word.\n\n|characteristic|description|examples|\n|-|-|-|\n{{\n$('Article Style & Brand Voice').item.json.output.map(item => (\n`|${item.characteristic}|${item.description}|${item.examples.map(ex => `\"${ex}\"`).join(', ')}|`\n)).join('\\n')\n}}"
        }
      },
      "type": "@n8n/n8n-nodes-langchain.googleGemini",
      "typeVersion": 1,
      "position": [
        4464,
        2576
      ],
      "id": "52bf05b7-30e6-48cf-8781-a5f5ab65f425",
      "name": "Message a model8",
      "credentials": {
        "googlePalmApi": {
          "id": "gQgC07v7jtToYr9F",
          "name": "Gemini meet2005pokar3-1"
        }
      }
    },
    {
      "parameters": {
        "folderId": "1ZQUyKpnp2nTCJ0w9uyeXMPzA8DCrsEoj",
        "title": "={{ $json.output.title }}"
      },
      "type": "n8n-nodes-base.googleDocs",
      "typeVersion": 2,
      "position": [
        4816,
        2576
      ],
      "id": "3a40e9f3-f02f-47d1-a92b-7c0391ada940",
      "name": "Create a document",
      "credentials": {
        "googleDocsOAuth2Api": {
          "id": "Y4rOpdmxmvoFD1ls",
          "name": "Google Docs account"
        }
      }
    }
  ],
  "connections": {
    "When clicking ‘Test workflow’": {
      "main": [
        [
          {
            "node": "Get Blog",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Get Blog": {
      "main": [
        [
          {
            "node": "Extract Article URLs",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Get Article": {
      "main": [
        [
          {
            "node": "Extract Article Content",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Extract Article URLs": {
      "main": [
        [
          {
            "node": "Split Out URLs",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Split Out URLs": {
      "main": [
        [
          {
            "node": "Latest Articles",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Latest Articles": {
      "main": [
        [
          {
            "node": "Get Article",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Extract Article Content": {
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
    "Combine Articles": {
      "main": [
        [
          {
            "node": "Message a model6",
            "type": "main",
            "index": 0
          },
          {
            "node": "Message a model7",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Article Style & Brand Voice": {
      "main": [
        [
          {
            "node": "New Article Instruction",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Save as Draft": {
      "main": [
        []
      ]
    },
    "Markdown": {
      "main": [
        [
          {
            "node": "Combine Articles",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "New Article Instruction": {
      "main": [
        [
          {
            "node": "Message a model8",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Message a model6": {
      "main": [
        [
          {
            "node": "Article Style & Brand Voice",
            "type": "main",
            "index": 1
          }
        ]
      ]
    },
    "Message a model7": {
      "main": [
        [
          {
            "node": "Article Style & Brand Voice",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Message a model8": {
      "main": [
        [
          {
            "node": "Create a document",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Create a document": {
      "main": [
        [
          {
            "node": "Save as Draft",
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
