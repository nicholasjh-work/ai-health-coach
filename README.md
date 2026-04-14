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

Generates personalized health coaching insights from synthetic wearable biometric data (HRV, sleep, recovery, strain) using locally-hosted LLMs. No paid API keys. No data leaves the machine.

The pipeline: synthetic data generator loads 2K members and 200K+ daily biometric readings into PostgreSQL. dbt transforms raw data into coaching context windows with rolling 7/30-day averages and trend detection. LiteLLM routes prompts to local Ollama models with compliance-tier routing. A separate evaluation model scores each insight on relevance, specificity, actionability, and safety. Evidence.dev renders three dashboard pages showing coaching priorities, cohort retention, and AI quality metrics.

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

#### ![Staging](https://img.shields.io/badge/Staging-58a6ff?style=flat-square) Staging Layer

| Model | Grain | Purpose |
|:------|:------|:--------|
| `stg_members` | 1 row per member | Clean profiles with tenure calculation |
| `stg_daily_metrics` | 1 row per member per day | Typed biometric readings with weekend flag |
| `stg_feature_events` | 1 row per event | Clean engagement events |
| `stg_sessions` | 1 row per session | Clean app sessions |

#### ![Intermediate](https://img.shields.io/badge/Intermediate-d29922?style=flat-square) Intermediate Layer

| Model | Grain | Purpose |
|:------|:------|:--------|
| `int_member_health_summary` | 1 row per member per day | 7d/30d rolling averages, HRV and recovery trends |
| `int_feature_adoption` | 1 row per member per feature | Lifetime adoption depth and interaction rates |

#### ![Mart](https://img.shields.io/badge/Mart-3fb950?style=flat-square) Mart Layer

| Model | Grain | Purpose |
|:------|:------|:--------|
| `mart_coaching_context` | 1 row per active member | Full coaching input: biometrics + trends + engagement + priority |
| `mart_cohort_retention` | 1 row per cohort-week / plan / channel / segment | Point-in-time retention at D7/D14/D30/D60/D90 |
| `mart_ai_evaluation` | 1 row per generated insight | Quality scores from evaluation model |

---

### LLM Routing

All models run locally via Ollama. No API keys needed.

| Tier | Model | Use Case |
|:-----|:------|:---------|
| ![Restricted](https://img.shields.io/badge/Restricted-f85149?style=flat-square) | `ollama/gemma3:12b` | PHI-adjacent context. Health data never leaves local machine. |
| ![Standard](https://img.shields.io/badge/Standard-58a6ff?style=flat-square) | `ollama/gemma3:12b` | Primary coaching generation model. |
| ![Evaluation](https://img.shields.io/badge/Evaluation-d29922?style=flat-square) | `ollama/gemma3:12b` | Separate evaluation pass for quality scoring. |
| ![Fallback](https://img.shields.io/badge/Fallback-8b949e?style=flat-square) | `ollama/llama3.1:8b` | Lighter backup when primary model is down. |

To swap in cloud models (Claude, GPT-4), update `src/llm/router.py` config. The compliance tier routing ensures PHI-adjacent data always stays local regardless of cloud availability.

---

### Evaluation Framework

Each generated insight is scored by a separate LLM call on four dimensions:

| Dimension | What It Measures | Target |
|:----------|:----------------|:-------|
| ![Relevance](https://img.shields.io/badge/Relevance-58a6ff?style=flat-square) | Does it reference the member's actual data? | **>70** |
| ![Specificity](https://img.shields.io/badge/Specificity-d29922?style=flat-square) | Does it include specific numbers and timeframes? | **>60** |
| ![Actionability](https://img.shields.io/badge/Actionability-3fb950?style=flat-square) | Can the member act on this in 48 hours? | **>70** |
| ![Safety](https://img.shields.io/badge/Safety-f85149?style=flat-square) | Does it avoid medical claims or dangerous advice? | **>90** |

Safety flags track medical claim frequency and ensure the coaching engine stays within guardrails.

---

### Evidence Dashboard

| Page | Description |
|:-----|:------------|
| **Coaching Insights** | Member overview by segment, priority distribution, biometric trends, recent generated insights |
| **Cohort Retention** | Retention curves by plan type, acquisition channel, and segment at D7/D14/D30/D60/D90 |
| **AI Evaluation** | Prompt version A/B comparison, quality score distributions, safety flag rates, top-scored insights |

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

# Generate coaching insights
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
| Database | PostgreSQL (Snowflake-portable SQL) |
| Transformations | dbt (staging / intermediate / marts) |
| LLM Routing | LiteLLM + Ollama (local, no paid APIs) |
| Evaluation | Structured LLM scoring with JSON output parsing |
| Dashboard | Evidence.dev |
| Deployment | Cloudflare Pages |
| Language | Python 3.11 |
| CI | GitHub Actions (ruff, mypy, pytest) |

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
