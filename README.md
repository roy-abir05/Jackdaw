# ⚓ JACKDAW

**The 100% Local Command Center for Your Code-to-Cash Pipeline.**

[![Built for Hackathon](https://img.shields.io/badge/Built_for-WeMakeDevs_Pirates_of_the_Coral--bean-c5a059?style=for-the-badge)](https://wemakedevs.org)
[![Powered by Coral](https://img.shields.io/badge/Powered_by-Coral-7c3aed?style=for-the-badge)](https://withcoral.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

Jackdaw is a terminal-native, 100% local analytics engine that lets you query GitHub, Vercel, PostHog, and Stripe simultaneously using pure natural language. No ETL pipelines. No data warehouses. No custom glue code. 

Built for developers who want their infrastructure data fast, accurate, and completely under their control.

---

## 🏴‍☠️ Forged in the Trenches. Built for the Crew.

We waste countless hours context-switching between GitHub tabs, Vercel dashboards, PostHog charts, and Stripe logs just to piece together what went wrong during a deployment or how a release impacted revenue. 

Jackdaw acts as a unified interface that cuts through the noise. It uses **Coral** as a zero-ETL data engine to instantly turn disjointed platform APIs into secure, queryable relational tables right on your machine.

## ✨ Features (The Quartermaster's Toolkit)

* **Natural Language Routing:** Just ask, *"What failed in my last deployment?"* Our local AI strategist, Anne Bonny, translates your intent into precise, optimized Coral SQL.
* **Cross-Source JOINs:** Seamlessly connect GitHub pull requests to live Vercel build statuses and Stripe revenue in a single, unified query.
* **100% Local Execution:** Your credentials, your data, and your usage history never leave your machine. Safety without brittle sandboxing.
* **Zero Custom Integrations:** Turn any API, database, or file system into a relational table instantly.
* **The Captain's Log:** Run `jackdaw log` to transform your standard terminal into a persistent, full-screen operations dashboard tracking your entire Code-to-Cash pipeline.
* **Read-Only by Design:** Jackdaw acts as a strict read layer. Your agents can explore and query across sources without ever risking a mutation to your upstream production systems.

---

## 🚀 Installation

Install Jackdaw instantly via our secure curl script. It sets up an isolated Python virtual environment without polluting your global packages.

```bash
curl -fsSL https://jackdaw.sh/install | sh
```

_(Alternatively, you can clone this repository and run the `install.sh` script manually.)_

### Authentication

On your first run, Jackdaw will prompt you for your read-only API keys:

Bash

```
jackdaw init
```

## 🧭 Usage

### The Interactive Dashboard

Launch the persistent, terminal-native dashboard to view live correlations across your platforms:

Bash

```
jackdaw log
```

### Natural Language Queries

Ask questions in plain English directly from the CLI:

Bash

```
jackdaw ask "Show me the Vercel deployment status for the last 3 merged PRs on GitHub"
```

Bash

```
jackdaw ask "Did yesterday's production deployment correlate with any Stripe payment failures?"
```

### Raw SQL Mode

Bypass the AI agent and write direct cross-platform SQL queries using Coral:

Bash

```
jackdaw query "SELECT g.author, v.url, v.status FROM github_commits g JOIN vercel_deployments v ON g.sha = v.commit_sha LIMIT 5;"
```

## 🏗️ Architecture & Stack

-   **Core Engine:** [Coral](https://www.google.com/search?q=https://coral.co/) (Zero-ETL SQL Engine)
    
-   **CLI Framework:** Python (Rich/Textual for terminal UI)
    
-   **AI Agent:** Local LLM integration for translating intent to Coral SQL syntax.
    
-   **Landing Page:** Next.js, Tailwind CSS, Framer Motion (View at `[https://jackdaw.sh](https://jackdaw.sh)`)
    
    

## 📜 Acknowledgements & Disclosure

-   **Hackathon:** Built by Abir Roy ([`@roy-abir05`](https://github.com/roy-abir05)) and Mohammad Irshad Siddi ([`@irshadsiddi`](https://github.com/irshadsiddi)) for the **WeMakeDevs Pirates of the Coral-bean** Hackathon (May 2026).
    
-   **AI Disclosure:** Large Language Models (LLMs) were utilized during the development of this project to assist with rapid prototyping, generating boilerplate Next.js UI components for the landing page, and refining the underlying bash installation scripts.
