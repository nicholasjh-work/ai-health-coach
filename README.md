<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/nh-logo-dark.svg" width="80">
    <source media="(prefers-color-scheme: light)" srcset="assets/nh-logo-light.svg" width="80">
    <img alt="Hidalgo Systems Labs" src="assets/nh-logo-light.svg" width="80">
  </picture>
</p>

<h1 align="center">AI Health Coach</h1>
<p align="center"><b>Personalized health coaching from wearable biometric data using local LLMs</b></p>

<p align="center">
  <a href="https://coach.nicholashidalgo.com"><img src="https://img.shields.io/badge/Demo-coach.nicholashidalgo.com-2563EB?style=for-the-badge" alt="Demo"></a>
  <a href="https://github.com/nicholasjh-work/ai-health-coach/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"></a>
  <a href="https://github.com/nicholasjh-work/ai-health-coach"><img src="https://img.shields.io/badge/Tests-15_passing-16a34a?style=for-the-badge" alt="Tests"></a>
  <a href="https://github.com/nicholasjh-work/ai-health-coach"><img src="https://img.shields.io/badge/dbt_Models-9-7c3aed?style=for-the-badge" alt="Models"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/dbt-FF694B?style=flat&logo=dbt&logoColor=white" alt="dbt">
  <img src="https://img.shields.io/badge/LiteLLM-1C3C3C?style=flat" alt="LiteLLM">
  <img src="https://img.shields.io/badge/Ollama-000000?style=flat" alt="Ollama">
  <img src="https://img.shields.io/badge/Evidence.dev-2563EB?style=flat" alt="Evidence">
  <img src="https://img.shields.io/badge/Cloudflare_Pages-F48120?style=flat&logo=cloudflare&logoColor=white" alt="Cloudflare">
</p>

---

### What This Does

<table>
<tr>
<td>

**2K members** and **200K+ daily biometric readings** (HRV, sleep, recovery, strain) flow through a full analytics pipeline, from synthetic data generation into PostgreSQL, through dbt transformations with rolling 7/30-day averages and trend detection, into a coaching engine powered by locally-hosted LLMs.

Each insight is generated using **segment-aware prompts** (power / active / casual), routed through **compliance-tier LLM routing** via LiteLLM + Ollama, and scored by a **separate evaluation model** on relevance, specificity, actionability, and safety.

Three Evidence.dev dashboard pages render coaching priorities, cohort retention, and AI quality metrics. Deployed on Cloudflare Pages.

**No paid API keys. No data leaves the machine.**

</td>
</tr>
</table>

---

### Architecture

```
Synthetic Data Generator (Python, NumPy, Faker)
        │
        ▼
   PostgreSQL (raw schema)
        │
        ▼
   dbt (staging → intermediate → marts)
   - stg_members, stg_daily_metrics, stg_feature_events, stg_sessions
   - int_member_health_summary (7d/30d rolling avgs, trend detection)
   - int_feature_adoption (weekly engagement depth)
   - mart_coaching_context (biometrics + trends + engagement + priority)
   - mart_cohort_retention (D7/D14/D30/D60/D90)
   - mart_ai_evaluation (quality scores)
        │
        ▼
   LiteLLM Router (compliance tiers → Ollama local models)
        │
        ▼
   Coaching Engine (segment-aware prompts, A/B variants, eval harness)
        │
        ▼
   Evidence.dev Dashboard (Cloudflare Pages)
```

---

### dbt Models

#### ![Staging](https://img.shields.io/badge/STAGING-58a6ff?style=for-the-badge) Sources to clean typed tables

| Model | Grain | Purpose |
|:------|:------|:--------|
| [![stg_members](https://img.shields.io/badge/stg__members-161b22?style=flat-square&logo=dbt&logoColor=FF694B)](src/dbt_project/models/staging/stg_members.sql) | 1 row per member | Clean profiles with tenure calculation |
| [![stg_daily_metrics](https://img.shields.io/badge/stg__daily__metrics-161b22?style=flat-square&logo=dbt&logoColor=FF694B)](src/dbt_project/models/staging/stg_daily_metrics.sql) | 1 row per member per day | Typed biometric readings with weekend flag |
| [![stg_feature_events](https://img.shields.io/badge/stg__feature__events-161b22?style=flat-square&logo=dbt&logoColor=FF694B)](src/dbt_project/models/staging/stg_feature_events.sql) | 1 row per event | Clean engagement events |
| [![stg_sessions](https://img.shields.io/badge/stg__sessions-161b22?style=flat-square&logo=dbt&logoColor=FF694B)](src/dbt_project/models/staging/stg_sessions.sql) | 1 row per session | Clean app sessions |

#### ![Intermediate](https://img.shields.io/badge/INTERMEDIATE-d29922?style=for-the-badge) Business logic and feature engineering

| Model | Grain | Purpose |
|:------|:------|:--------|
| [![int_member_health_summary](https://img.shields.io/badge/int__member__health__summary-161b22?style=flat-square&logo=dbt&logoColor=FF694B)](src/dbt_project/models/intermediate/int_member_health_summary.sql) | 1 row per member per day | 7d/30d rolling averages, HRV and recovery trends |
| [![int_feature_adoption](https://img.shields.io/badge/int__feature__adoption-161b22?style=flat-square&logo=dbt&logoColor=FF694B)](src/dbt_project/models/intermediate/int_feature_adoption.sql) | 1 row per member per feature | Lifetime adoption depth and interaction rates |

#### ![Mart](https://img.shields.io/badge/MART-3fb950?style=for-the-badge) Consumption-ready outputs

| Model | Grain | Purpose |
|:------|:------|:--------|
| [![mart_coaching_context](https://img.shields.io/badge/mart__coaching__context-161b22?style=flat-square&logo=dbt&logoColor=FF694B)](src/dbt_project/models/marts/mart_coaching_context.sql) | 1 row per active member | Full coaching input: biometrics + trends + engagement + priority |
| [![mart_cohort_retention](https://img.shields.io/badge/mart__cohort__retention-161b22?style=flat-square&logo=dbt&logoColor=FF694B)](src/dbt_project/models/marts/mart_cohort_retention.sql) | 1 row per cohort-week / plan / channel / segment | Point-in-time retention at D7/D14/D30/D60/D90 |
| [![mart_ai_evaluation](https://img.shields.io/badge/mart__ai__evaluation-161b22?style=flat-square&logo=dbt&logoColor=FF694B)](src/dbt_project/models/marts/mart_ai_evaluation.sql) | 1 row per generated insight | Quality scores from evaluation model |

---

### LLM Routing

> All models run locally via Ollama. No API keys needed. To swap in cloud models (Claude, GPT-4), update `src/llm/router.py`. Compliance tier routing ensures PHI-adjacent data always stays local.

| Tier | Model | Use Case |
|:-----|:------|:---------|
| ![Restricted](https://img.shields.io/badge/RESTRICTED-f85149?style=flat-square) | [![gemma3:12b](https://img.shields.io/badge/ollama%2Fgemma3:12b-000000?style=flat-square&logo=ollama&logoColor=white)](https://ollama.com/library/gemma3) | PHI-adjacent context. Health data never leaves local. |
| ![Standard](https://img.shields.io/badge/STANDARD-58a6ff?style=flat-square) | [![gemma3:12b](https://img.shields.io/badge/ollama%2Fgemma3:12b-000000?style=flat-square&logo=ollama&logoColor=white)](https://ollama.com/library/gemma3) | Primary coaching generation model. |
| ![Evaluation](https://img.shields.io/badge/EVALUATION-d29922?style=flat-square) | [![gemma3:12b](https://img.shields.io/badge/ollama%2Fgemma3:12b-000000?style=flat-square&logo=ollama&logoColor=white)](https://ollama.com/library/gemma3) | Separate evaluation pass for quality scoring. |
| ![Fallback](https://img.shields.io/badge/FALLBACK-8b949e?style=flat-square) | [![llama3.1:8b](https://img.shields.io/badge/ollama%2Fllama3.1:8b-000000?style=flat-square&logo=ollama&logoColor=white)](https://ollama.com/library/llama3.1) | Lighter backup when primary is down. |

---

### Evaluation Framework

> Each generated insight is scored by a separate LLM call on four dimensions:

| Dimension | What It Measures | Target |
|:----------|:----------------|:------:|
| ![Relevance](https://img.shields.io/badge/Relevance-58a6ff?style=flat-square) | Does it reference the member's actual data? | ![>70](https://img.shields.io/badge/>70-16a34a?style=flat-square) |
| ![Specificity](https://img.shields.io/badge/Specificity-d29922?style=flat-square) | Does it include specific numbers and timeframes? | ![>60](https://img.shields.io/badge/>60-16a34a?style=flat-square) |
| ![Actionability](https://img.shields.io/badge/Actionability-3fb950?style=flat-square) | Can the member act on this in 48 hours? | ![>70](https://img.shields.io/badge/>70-16a34a?style=flat-square) |
| ![Safety](https://img.shields.io/badge/Safety-f85149?style=flat-square) | Does it avoid medical claims or dangerous advice? | ![>90](https://img.shields.io/badge/>90-16a34a?style=flat-square) |

Safety flags track medical claim frequency and ensure the coaching engine stays within guardrails.

---

### Evidence Dashboard

| Page | Description |
|:-----|:------------|
| ![Coaching](https://img.shields.io/badge/Coaching_Insights-2563EB?style=flat-square) | Member overview by segment, priority distribution, biometric trends, recent generated insights |
| ![Retention](https://img.shields.io/badge/Cohort_Retention-16a34a?style=flat-square) | Retention curves by plan type, acquisition channel, and segment at D7/D14/D30/D60/D90 |
| ![Evaluation](https://img.shields.io/badge/AI_Evaluation-d29922?style=flat-square) | Prompt version A/B comparison, quality score distributions, safety flag rates, top-scored insights |

---

### Quick Start

```bash
git clone https://github.com/nicholasjh-work/ai-health-coach.git
cd ai-health-coach

python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env

# Create database
createdb ai_health_coach

# Load synthetic data
python -m src.data_gen.generate

# Run dbt transformations
cd src/dbt_project && dbt run --profiles-dir . && cd ../..

# Generate coaching insights (requires Ollama running with gemma3)
python -m src.cli insights --n 20 --version v1

# Run A/B variant
python -m src.cli insights --n 20 --version v2

# View evaluation summary
python -m src.cli evaluate

# Launch Evidence dashboard
cd evidence && npx evidence dev
```

---

### Tech Stack

| Component | Technology |
|:----------|:-----------|
| ![DB](https://img.shields.io/badge/Database-4169E1?style=flat-square) | PostgreSQL (Snowflake-portable SQL) |
| ![Transform](https://img.shields.io/badge/Transforms-FF694B?style=flat-square) | dbt (staging / intermediate / marts) |
| ![LLM](https://img.shields.io/badge/LLM_Routing-1C3C3C?style=flat-square) | LiteLLM + Ollama (local, no paid APIs) |
| ![Eval](https://img.shields.io/badge/Evaluation-d29922?style=flat-square) | Structured LLM scoring with JSON output parsing |
| ![Dash](https://img.shields.io/badge/Dashboard-2563EB?style=flat-square) | Evidence.dev |
| ![Deploy](https://img.shields.io/badge/Deployment-F48120?style=flat-square) | Cloudflare Pages |
| ![Lang](https://img.shields.io/badge/Language-3776AB?style=flat-square) | Python 3.11 |
| ![CI](https://img.shields.io/badge/CI-333333?style=flat-square) | GitHub Actions (ruff, mypy, pytest) |

---

### Tests

```bash
pytest tests/ -v
```

15 unit tests covering data generation bounds, prompt construction, router compliance tier routing, and segment-aware tone matching.

---

<p align="center">
  <a href="https://linkedin.com/in/nicholashidalgo"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>&nbsp;
  <a href="https://nicholashidalgo.com"><img src="https://img.shields.io/badge/Website-000000?style=for-the-badge&logo=About.me&logoColor=white" alt="Website"></a>&nbsp;
  <a href="mailto:analytics@nicholashidalgo.com"><img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"></a>
</p>
