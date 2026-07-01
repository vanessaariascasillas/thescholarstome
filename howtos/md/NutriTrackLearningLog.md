# NutriTrack — Learning Log
### A Researcher's Notebook on Building & Deploying a Full-Stack AI Web App

---

> This is a personal record of the decisions made, mistakes encountered, and lessons learned while building NutriTrack from scratch using AI-assisted development (vibe coding). It is written as a journal, not a tutorial — the goal is to capture the *experience* of building, not just the end result.

---

## Entry 0 — Before the First Line of Code: The Workshop & The Prompt Enhancer

**This project was built as part of a GeeksforGeeks workshop on vibe coding and AI-assisted development.** The workshop (available on the [GeeksforGeeks YouTube channel](https://www.youtube.com/@GeeksforGeeksVideos)) is unlisted and not publicly searchable — it was the starting point that introduced the workflow, tools, and approach documented throughout this log.

---

**The actual beginning of this project was not writing code. It was writing a rough idea.**

This is the full three-step chain that started NutriTrack before anything was built:

```
Step 1: Write a rough prompt using a simple framework
        ↓
Step 2: Paste it into Max AI (prompt enhancer) to expand it into a detailed spec
        ↓
Step 3: Paste the enhanced spec into Claude Code (the coding AI) to build the app
```

---

### Step 1 — The Original Rough Prompt

Before any specification existed, there was a short, unpolished description of the idea. It was written using a simple prompt-writing framework:

| Framework Section | Purpose |
|---|---|
| **Role** | Tell the AI what kind of expert it should act as |
| **Define Goal** | State clearly what you want to build |
| **Provide Context** | Give details about what it needs to do |
| **Does it need AI?** | Specify if AI features are required and what for |
| **Create the Vibe** | Describe the visual style or feeling |
| **Optional: Add a Visual** | Reference a design style or example |

**The original prompt written using this framework:**

> *"You are a website builder with a strong focus on user experience. Design a web application for daily tracking of food intake, including calories, macronutrients (protein), micronutrients (iron, salt, sugar), and water. The website should facilitate diabetes management by monitoring sugar intake. Users should be able to input food items via descriptions or images, with AI assistance for calorie and nutritional estimation. A weekly summary feature is required. The desired aesthetic is skeuomorphic.*
>
> *I need tech stacks like for frontend HTML CSS JS, back end we will use API and Python."*

This is a complete, valid starting prompt. It has a role, a goal, context, an AI requirement, and a vibe. It is not polished or technical — and it does not need to be. That is the point of the next step.

---

### Step 2 — The Prompt Enhancer (Max AI)

The rough prompt above was pasted into **Max AI** — a prompt enhancement tool — with the instruction to expand it into a full technical specification for a coding agent.

**What Max AI added:**
- A specific tech stack with exact library names and versions
- Detailed color tokens and typography choices for the skeuomorphic aesthetic
- A complete list of API endpoints with HTTP methods and payloads
- A file and folder structure for the project
- Accessibility requirements
- Explicit constraints (no CSS frameworks, no JS frameworks, no frontend API keys)
- Realistic example data instead of placeholder text

The output of that enhancement is the full specification in the next section.

**The lesson:** You do not need to know how to write a technical spec. You need to know what you want to build. A prompt enhancer converts the first into the second.

---

### What is a Prompt Enhancer?

A **prompt enhancer** is when you use an AI to turn your rough idea into a detailed, structured specification *before* you start building. The workflow is:

1. Write a short description of what you want to build using the framework above
2. Paste it into a prompt enhancer AI (Max AI, Gemini, ChatGPT) and ask it to expand into a full technical specification for a coding agent
3. Review and edit the result until it matches your vision
4. Paste that specification into your coding IDE as the first instruction

This is the document that was pasted into the IDE to start NutriTrack. Everything in the project — the visual design, the file structure, the API endpoints, the database schema — came from this single starting prompt.

---

### The NutriTrack Starting Specification

```
# Enhanced Agent Prompt: NutriTrack — Daily Food & Diabetes Management Web Application

## 🎯 Project Overview

You are a senior full-stack web developer and UX designer tasked with building NutriTrack,
a daily food intake and diabetes management web application. The product must feel like a
well-crafted physical health journal brought to life on screen — skeuomorphic, tactile, and
warm, not a clinical dashboard. Every design and engineering decision should serve a user
who checks this app every day and needs clarity, trust, and ease.

## 🖥️ Tech Stack

Frontend:
- HTML5 — Semantic markup with ARIA attributes for accessibility
- CSS3 — Custom properties (CSS variables), Flexbox, Grid; NO CSS frameworks
- Vanilla JavaScript (ES6+) — Modular, no frameworks; use native fetch API
- Chart.js (CDN) — For weekly summary visualizations
- No build tools required — fully served as static files

Backend:
- Python 3.11+ with FastAPI — RESTful API server
- Uvicorn — ASGI server for FastAPI
- SQLite (via aiosqlite) — Local database; use SQLAlchemy ORM for models
- Anthropic Python SDK — For AI-powered food identification from text and images
- Pillow (PIL) — For image preprocessing before sending to the AI
- Pydantic v2 — For request/response validation schemas
- python-dotenv — For environment variable management

AI Integration:
- Anthropic Claude API (claude-sonnet-4-6 model) — Used for:
  - Parsing natural-language food descriptions into structured nutritional data
  - Analyzing food images (base64-encoded) and returning estimated macros/micros
  - Generating personalized weekly health insights

## 🎨 Visual Design — Skeuomorphic Aesthetic

The UI must look and feel like a leather-bound health journal and analog kitchen scale
combined. This is the defining aesthetic signature. Every surface should suggest physical
material.

Design Tokens:
  --parchment:       #F5EDD8   (background, journal pages)
  --leather-dark:    #3B2314   (primary text, header bars)
  --leather-mid:     #7A4728   (buttons, accents)
  --leather-light:   #C4894F   (highlights, hover states)
  --cream-card:      #FAF3E0   (card surfaces)
  --stitching:       #A0522D   (dashed borders, dividers)
  --danger-red:      #B22222   (healthy range indicators)
  --safe-green:      #4A7C59   (healthy range indicators)
  --water-blue:      #4682B4   (water intake tracker)

Typography:
  Display: 'Playfair Display' — headings, journal-style titles
  Body: 'Lora' — readable serif for data labels and descriptions
  Monospace/Data: 'Courier Prime' — numbers, calorie counts, gram values

## 📋 Feature Specifications

1. Daily Food Log (/ — main dashboard)
   - Text input: "Describe what you ate..."
   - Image upload: "📷 Snap or Upload Food Photo"
   - 5 circular SVG gauges: Calories, Protein, Iron, Salt, Sugar
   - Sugar gauge has red warning zone when >50g (diabetes alert)
   - Water intake tracker: vertical glass graphic that fills as user logs cups
   - Diabetes alert banner when sugar > 50g/day

2. Weekly Summary (/weekly)
   - Line chart (Chart.js) — calories per day for 7 days
   - Bar chart — macros per day
   - Summary cards: avg daily calories, avg sugar, avg water intake
   - AI-generated insight paragraph from weekly data

3. Settings Panel (modal overlay)
   - Daily targets: Calories, Protein, Iron, Salt, Sugar, Water
   - Diabetes mode toggle (stricter 25g sugar threshold)
   - Persisted to localStorage and synced to backend

## 🔌 API Endpoints

POST   /api/food/analyze          # text or image → NutritionEntry
POST   /api/food/log              # save food entry
GET    /api/food/log/today        # today's log + totals
DELETE /api/food/log/{entry_id}   # delete entry
GET    /api/food/log/week         # last 7 days
POST   /api/water/log             # log a glass of water
GET    /api/water/log/today       # today's water count
PUT    /api/user/settings         # save settings
GET    /api/user/settings         # get settings
POST   /api/summary/insights      # weekly data → AI insight

## 🚫 Constraints

- Do NOT use any CSS framework (Bootstrap, Tailwind, Bulma)
- Do NOT use any JavaScript framework (React, Vue, Angular)
- Do NOT use any ORM other than SQLAlchemy
- Do NOT store API keys in frontend code — all AI calls go through Python backend
- Do NOT use placeholder content — build with realistic food examples
```

---

### What This Specification Produced

The AI built the entire initial version of the app from this single document:
- The leather journal visual design with all the CSS color tokens
- The food log with circular SVG nutrient gauges
- The water tracker glass animation
- The weekly summary with Chart.js charts
- The FastAPI backend with all 9 API endpoints
- The SQLAlchemy database models
- The Gemini AI integration for food analysis
- The full file and folder structure

**What the specification did NOT include** (added later through conversation):
- User authentication (login, registration, JWT tokens)
- Forgot password / security questions
- A1c tracking
- Medication checkbox
- Blood sugar input
- Deployment to Cloud Run

Those features came through the iterative prompting documented in Entries 1–9.

---

### How to Write Your Own Starting Specification

You do not have to write this from scratch. Use an AI to help you build it:

1. Open ChatGPT, Gemini, or Claude in your browser
2. Type something like:
   > *"I want to build a [your app idea]. Help me write a detailed technical specification I can give to an AI coding assistant. Include: the tech stack, visual design direction, list of features, API endpoints it will need, and any constraints. Make it detailed enough that a developer could build it from this document alone."*
3. Review what it generates — add your own aesthetic preferences, remove features you don't need, adjust the constraints
