<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/nh-logo-dark.svg" width="80">
  <source media="(prefers-color-scheme: light)" srcset="assets/nh-logo-light.svg" width="80">
  <img alt="NH" src="assets/nh-logo-light.svg" width="80">
</picture>

# AI Health Coach

**Personalized health coaching from wearable biometric data using local LLMs**

[![Demo](https://img.shields.io/badge/Demo-coach.nicholashidalgo.com-blue?style=for-the-badge)](https://coach.nicholashidalgo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-FF694B?style=flat&logo=dbt&logoColor=white)
![LiteLLM](https://img.shields.io/badge/LiteLLM-1C3C3C?style=flat)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=flat)
![Evidence](https://img.shields.io/badge/Evidence.dev-2563EB?style=flat)

</div>

---

### What This Does

Generates personalized health coaching insights from synthetic wearable biometric data (HRV, sleep, recovery, strain) using locally-hosted LLMs. No paid API keys. No data leaves the machine.

The pipeline: synthetic data generator loads 2K members and 200K+ daily biometric readings into PostgreSQL. dbt transforms raw data into coaching context windows with rolling 7/30-day averages and trend detection. LiteLLM routes prompts to local Ollama models with compliance-tier routing. A separate evaluation model scores each insight on relevance, specificity, actionability, and safety. Evidence.dev renders three dashboard pages showing coaching priorities, cohort retention, and AI quality metrics.

---

### Architecture

```
Synthetic Data Generator (Python, NumPy, Faker)
        |
        v
   PostgreSQL (raw schema)
        |
        v
   dbt (staging -> intermediate -> marts)
   - stg_members, stg_daily_metrics, stg_feature_events, stg_sessions
   - int_member_health_summary (7d/30d rolling avgs, trend detection)
   - int_feature_adoption (weekly engagement depth)
   - mart_coaching_context (one row per member: biometrics + trends + engagement + priority score)
   - mart_cohort_retention (point-in-time retention at D7/D14/D30/D60/D90)
   - mart_ai_evaluation (quality scores for generated insights)
        |
        v
   LiteLLM Router (compliance tiers -> Ollama local models)
   - RESTRICTED: PHI-adjacent -> local only
   - STANDARD: coaching generation -> local
   - EVALUATION: quality scoring -> local
        |
        v
   Coaching Engine
   - Segment-aware prompts (power/active/casual tone)
   - A/B prompt variants (v1 vs v2)
   - Evaluation harness (relevance, specificity, actionability, safety)
        |
        v
   Evidence.dev Dashboard (Cloudflare Pages)
   - Coaching Insights (priority distribution, segment trends, recent insights)
   - Cohort Retention (plan/channel/segment curves at D7-D90)
   - AI Evaluation (quality scores, A/B comparison, safety flags)
```

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
cd src/dbt_project
dbt run --profiles-dir .
cd ../..

# Generate coaching insights (requires Ollama running with llama3)
python -m src.cli insights --n 20 --version v1

# Run A/B variant
python -m src.cli insights --n 20 --version v2

# View evaluation summary
python -m src.cli evaluate

# Launch Evidence dashboard
cd evidence
npx evidence dev
```

---

### dbt Models

| Layer | Model | Grain | Purpose |
|-------|-------|-------|---------|
| Staging | `stg_members` | 1 row per member | Clean profiles with tenure calculation |
| Staging | `stg_daily_metrics` | 1 row per member per day | Typed biometric readings with weekend flag |
| Staging | `stg_feature_events` | 1 row per event | Clean engagement events |
| Staging | `stg_sessions` | 1 row per session | Clean app sessions |
| Intermediate | `int_member_health_summary` | 1 row per member per day | 7d/30d rolling averages, HRV and recovery trends |
| Intermediate | `int_feature_adoption` | 1 row per member per feature | Lifetime adoption depth and interaction rates |
| Mart | `mart_coaching_context` | 1 row per active member | Full coaching input: biometrics + trends + engagement + priority |
| Mart | `mart_cohort_retention` | 1 row per cohort-week/plan/channel/segment | Point-in-time retention at D7/D14/D30/D60/D90 |
| Mart | `mart_ai_evaluation` | 1 row per generated insight | Quality scores from evaluation model |

---

### LLM Routing

All models run locally via Ollama. No API keys needed.

| Tier | Use Case | Model | Rationale |
|------|----------|-------|-----------|
| RESTRICTED | PHI-adjacent context | `ollama/gemma3:12b` | Health data never leaves local machine |
| STANDARD | Coaching generation | `ollama/gemma3:12b` | Primary generation model |
| EVALUATION | Quality scoring | `ollama/gemma3:12b` | Separate evaluation pass |
| FALLBACK | Primary model down | `ollama/llama3.1:8b` | Lighter model as backup |

To swap in cloud models (Claude, GPT-4), update `src/llm/router.py` config. The compliance tier routing ensures PHI-adjacent data always stays local regardless of cloud availability.

---

### Evaluation Framework

Each generated insight is scored by a separate LLM call on four dimensions:

| Dimension | What It Measures | Target |
|-----------|-----------------|--------|
| Relevance | Does it reference the member's actual data? | >70 |
| Specificity | Does it include specific numbers and timeframes? | >60 |
| Actionability | Can the member act on this in 48 hours? | >70 |
| Safety | Does it avoid medical claims or dangerous advice? | >90 |

Safety flags track medical claim frequency and ensure the coaching engine stays within guardrails.

---

### Evidence Dashboard Pages

| Page | Shows |
|------|-------|
| **Coaching Insights** | Member overview by segment, priority distribution, biometric trends, recent generated insights |
| **Cohort Retention** | Retention curves by plan type, acquisition channel, and segment at D7/D14/D30/D60/D90 |
| **AI Evaluation** | Prompt version A/B comparison, quality score distributions, safety flag rates, top-scored insights |

---

### Tech Stack

| Component | Technology |
|-----------|-----------|
| Database | PostgreSQL (Snowflake-portable SQL) |
| Transformations | dbt (staging/intermediate/marts) |
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

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Nicholas_Hidalgo-0A66C2?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/nicholashidalgo)&nbsp;
[![Website](https://img.shields.io/badge/Website-nicholashidalgo.com-000000?style=for-the-badge)](https://nicholashidalgo.com)&nbsp;
[![Email](https://img.shields.io/badge/Email-analytics@nicholashidalgo.com-EA4335?style=for-the-badge&logo=gmail)](mailto:analytics@nicholashidalgo.com)

</div>
