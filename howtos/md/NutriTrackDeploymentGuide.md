---
type: Guide
---

# NutriTrack — Complete Deployment & Architecture Guide

An educational guide detailing the local setup, cloud migration, database architecture transitions, and production deployment of the NutriTrack health journal. Use this document to teach others how to deploy a full-stack, AI-powered web application on Google Cloud.

---

## Table of Contents
1. [Architecture & Tech Stack Overview](#1-architecture--tech-stack-overview)
2. [Choose Your Ecosystem First](#2-choose-your-ecosystem-first)
3. [Install Required Tools](#3-install-required-tools)
4. [Account Creation Step-by-Step](#4-account-creation-step-by-step)
5. [Connect & Verify Everything](#5-connect--verify-everything)
6. [Local Development Setup](#6-local-development-setup)
7. [The Deployment Journey: SQLite ➔ Cloud SQL ➔ Neon Postgres](#7-the-deployment-journey-sqlite--cloud-sql--neon-postgres)
8. [Google Cloud Platform Configuration (One-Time Per Project)](#8-google-cloud-platform-configuration-one-time-per-project)
9. [Deploying the Application to Cloud Run](#9-deploying-the-application-to-cloud-run)
10. [PostgreSQL Migration Pitfalls & Debugging](#10-postgresql-migration-pitfalls--debugging)
11. [Billing & AI Cost FAQ (Teaching Guide)](#11-billing--ai-cost-faq-teaching-guide)
12. [Checking Live Logs & Troubleshooting](#12-checking-live-logs--troubleshooting)
13. [Publishing to GitHub Safely](#13-publishing-to-github-safely)
14. [Deploying a Second Website (Same Billing, New Project)](#14-deploying-a-second-website-same-billing-new-project)
15. [Vibe Coding: How This Project Was Built with AI](#15-vibe-coding-how-this-project-was-built-with-ai)

---

## 1. Architecture & Tech Stack Overview


NutriTrack is a personal health journal that runs as a containerized full-stack application:
*   **Frontend:** Pure, framework-less HTML5, CSS3 (warm, skeuomorphic leather journal aesthetic), and vanilla JavaScript.
*   **Backend:** FastAPI (Python 3.12, async), running on Uvicorn.
*   **AI Integration:** Google Gemini 2.5 Flash via Vertex AI (`google-cloud-aiplatform`).
*   **Database:** PostgreSQL accessed asynchronously via SQLAlchemy ORM and the `asyncpg` driver.
*   **Hosting:** Google Cloud Run (serverless container hosting).

In production, **FastAPI serves both the API and the static frontend files** from a single Docker container. This eliminates CORS issues and simplifies the deployment architecture to a single service.

---

## 2. Choose Your Ecosystem First

> **The most overlooked step in vibe coding:** Most beginners spend more time on configuration — accounts, billing, authentication, cloud resources, IDE setup — than on actual prompting. Choosing your ecosystem *before* creating accounts saves significant time because every tool in an ecosystem is designed to connect to the others.

An **ecosystem** is a family of tools from one provider that work together natively:

| Ecosystem | AI Brain | IDE | Cloud Host | Database |
|---|---|---|---|---|
| **Google (used here)** | Gemini | Antigravity | Cloud Run | Neon / Cloud SQL |
| **Anthropic** | Claude | Cursor / VS Code | Any | Any |
| **OpenAI** | ChatGPT | Cursor / VS Code | Any | Any |
| **Local / Open Source** | Ollama | VS Code | Self-hosted | Any |

**This guide uses the Google ecosystem** — Gemini AI, Antigravity IDE, Google Cloud Run for hosting, and Neon for the database.

> **Recommendation for beginners:** Pick one ecosystem and learn it fully before mixing. Each tool you add from a different provider introduces a new authentication layer, a new billing account, and a new set of docs.

---

## 3. Install Required Tools

These are installed **once on your computer**, not once per project. Skip any you already have.

### A. Python 3.12+
1. Go to https://www.python.org/downloads/ and download the latest Python 3.12 installer.
2. Run the installer. **Check the box that says "Add Python to PATH"** before clicking Install.
3. Verify it worked — open a terminal and run:
   ```bash
   python --version
   ```
   You should see `Python 3.12.x` or higher.

### B. Google Cloud SDK (gcloud CLI)
This is the command-line tool used to deploy to Cloud Run, manage secrets, and configure GCP.

**Windows:**
1. Go to https://cloud.google.com/sdk/docs/install and download the **Windows installer** (.exe).
2. Run the installer — it will also install Python if you don't have it.
3. At the end of installation, leave the box checked that says **"Run gcloud init"** and click Finish. A terminal will open automatically.

**Mac:**
```bash
brew install google-cloud-sdk
```
Or download the macOS package from the same URL above.

**After installation (all platforms), run:**
```bash
gcloud init
```
This walks you through:
- Logging in to your Google account in a browser
- Selecting a default project (you can change this later)
- Selecting a default region

Verify it worked:
```bash
gcloud --version
```

### C. Antigravity IDE
Antigravity is the AI-native development environment used to build this project. Think of it as the AI's "hands" — Gemini (or Claude) is the brain that reasons, but the IDE is what actually reads your files, writes code, and runs terminal commands.

1. Go to https://antigravity.dev and download the installer for your OS
2. Install and open it
3. Sign in with your Google account (same one you'll use for Google Cloud)
4. Open your project folder via **File → Open Folder**

> If you prefer VS Code, Claude Code (https://claude.ai/code) works the same way as an extension. This project was built using Claude Code inside Antigravity.

### D. Docker (Optional — for local container testing only)
Only needed if you want to test the production container on your own machine before deploying. You can skip this and deploy directly to Cloud Run without it.

If you do want it: https://www.docker.com/products/docker-desktop

---

## 4. Account Creation Step-by-Step

To host this project in production with zero constant costs, you need three things set up: a Google identity, a Google Cloud workspace, and a free database.

> **Important distinction — two different "Google" accounts:**
> - **Google Account** (gmail.com) — your identity. Used to log in to everything.
> - **Google Cloud Account** — a separate workspace where your applications actually run. Requires its own sign-up and billing setup even if you already have Gmail.
>
> You need both. They are linked but not the same thing.

### A. Google Account (Identity)
If you have Gmail, you already have this. If not:
1. Go to https://accounts.google.com and click **Create account**
2. This account becomes your login for Google Cloud, Gemini API, Antigravity, and everything else in the ecosystem

### B. Google Cloud Platform (GCP) + Billing
1. Go to [Google Cloud Console](https://console.cloud.google.com) and sign in with your Google account
2. Click **Get Started for Free** or **Try for Free**
3. Set up a **Billing Account** — enter your credit card
   > [!NOTE]
   > Google requires a credit card to prevent abuse. New users receive ~$300 in free credits before any charges apply. The setup in this guide stays within the free tier after those credits.
4. Click the project dropdown in the top-left and select **New Project**
5. Name your project (e.g., `nutritrack-app`)
6. Copy and save your **Project ID** (e.g. `nutritrack-app-429317`) and **Project Number** from the project dashboard

### C. Enable the Gemini API
This turns Gemini from a chatbot you use in a browser into a tool your application can call programmatically.
1. Go to https://ai.google.dev and click **Get API Key**
2. Select your Google Cloud project
3. Click **Create API Key**
4. Save the key — you'll use it in your `.env` file
   > Do not paste this key into frontend code. It must stay on the backend only.

### D. Neon Serverless PostgreSQL
1. Go to [Neon](https://neon.tech) and sign up (you can use Google or GitHub OAuth, no credit card required).
2. Create a new project named `nutritrack`.
3. Pick a hosting region geographically close to your Cloud Run deployment region (e.g., if you plan to deploy Cloud Run to `us-central1` (Iowa), pick AWS US East or US West to minimize network latency).
4. Go to the project dashboard, select **Connection Details**, and copy the connection string. It will look like:
   ```
   postgresql://neondb_owner:abc123xyz@ep-xxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
5. Save this URL. You will modify it slightly in later steps.

---

## 5. Connect & Verify Everything

> **Why this step matters:** Each service you set up requires authentication before the next one can use it. If any link in the chain is missing, you get silent failures — the app loads but nothing works, with no obvious error message. Verify each connection before moving on.

### What is MCP?

**MCP (Model Context Protocol)** is what transforms an AI chatbot into an AI agent.

| Without MCP | With MCP |
|---|---|
| AI can answer questions | AI can read and write your files |
| AI can suggest code | AI can execute terminal commands |
| AI can explain concepts | AI can deploy to Cloud Run |
| AI can write a deploy command | AI can *run* the deploy command |

MCP is the bridge between the AI's intelligence and the tools on your computer and in the cloud. Without it, the AI is a very smart advisor. With it, the AI is a hands-on developer.

### Connect Antigravity to Google Services

1. Open Antigravity IDE
2. Go to **Settings → MCP Servers** (or the MCP panel in the sidebar)
3. Add the Google Cloud MCP server — Antigravity may prompt you to do this automatically when you first open a project with Cloud Run integration
4. Authenticate: when prompted, log in with the same Google account used for Google Cloud
5. Run in the terminal inside Antigravity:
   ```bash
   gcloud auth application-default login
   ```
   This creates a local credential file that lets code running on your machine call Google APIs (Gemini, Cloud Run, etc.) without needing an API key in every request.

### Verification Checkpoint

Before writing any code, confirm each of these works. Missing one causes silent failures later.

| Check | How to verify |
|---|---|
| ✅ Google account active | You can log in to console.cloud.google.com |
| ✅ Billing enabled | Console shows a project with billing linked |
| ✅ Gemini API enabled | You have an API key from ai.google.dev |
| ✅ gcloud CLI authenticated | Run `gcloud auth list` — your email appears |
| ✅ Antigravity signed in | Your Google account shows in the IDE top bar |
| ✅ MCP connected | Antigravity can list your GCP projects |
| ✅ App default credentials | Run `gcloud auth application-default print-access-token` — returns a token |

If any check fails, fix it before proceeding. Every step after this assumes the full chain is working.

### The Authentication Chain

Understanding this chain explains why "it works on my machine but not in production" happens so often:

```
Your Google Account
      ↓ (identity)
Google Cloud Project
      ↓ (workspace)
APIs Enabled (Cloud Run, Gemini, Secret Manager)
      ↓ (services available)
Service Account (Cloud Run's own identity)
      ↓ (permissions granted)
Secrets & Resources (JWT key, database)
```