<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Health Coach README Preview</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: 'Inter', -apple-system, sans-serif;
    background: #0d1117;
    color: #e6edf3;
    padding: 40px;
    line-height: 1.6;
    max-width: 900px;
    margin: 0 auto;
  }

  .readme-container {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 40px;
  }

  .center { text-align: center; }

  .logo-placeholder {
    width: 80px; height: 80px;
    background: linear-gradient(135deg, #1a5276, #2980b9);
    border-radius: 12px;
    margin: 0 auto 16px;
    display: flex; align-items: center; justify-content: center;
    font-size: 28px; font-weight: 700; color: white;
    letter-spacing: -1px;
  }

  h1 {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 8px;
    color: #e6edf3;
  }

  .tagline {
    color: #8b949e;
    font-size: 15px;
    margin-bottom: 20px;
  }

  .badges-row {
    display: flex;
    gap: 8px;
    justify-content: center;
    flex-wrap: wrap;
    margin-bottom: 12px;
  }

  .badge {
    display: inline-flex;
    align-items: center;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    overflow: hidden;
    text-decoration: none;
    height: 24px;
  }

  .badge-left {
    padding: 0 8px;
    background: #333;
    color: #e6edf3;
    display: flex; align-items: center; height: 100%;
  }

  .badge-right {
    padding: 0 8px;
    display: flex; align-items: center; height: 100%;
    color: white;
  }

  .badge-blue .badge-right { background: #2563eb; }
  .badge-yellow .badge-right { background: #ca8a04; }
  .badge-green .badge-right { background: #16a34a; }
  .badge-red .badge-right { background: #dc2626; }
  .badge-purple .badge-right { background: #7c3aed; }
  .badge-orange .badge-right { background: #ea580c; }
  .badge-teal .badge-right { background: #0d9488; }
  .badge-pink .badge-right { background: #db2777; }

  .badge-flat {
    display: inline-flex;
    align-items: center;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 500;
    padding: 3px 8px;
    gap: 5px;
    color: white;
    text-decoration: none;
  }

  .tech-badges {
    display: flex;
    gap: 6px;
    justify-content: center;
    flex-wrap: wrap;
    margin-bottom: 24px;
  }

  hr {
    border: none;
    border-top: 1px solid #21262d;
    margin: 28px 0;
  }

  h3 {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 14px;
    color: #e6edf3;
    padding-bottom: 6px;
    border-bottom: 1px solid #21262d;
  }

  p {
    color: #c9d1d9;
    font-size: 14px;
    margin-bottom: 14px;
    line-height: 1.7;
  }

  .arch-block {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #8b949e;
    white-space: pre;
    overflow-x: auto;
    margin-bottom: 14px;
    line-height: 1.5;
  }

  /* dbt model cards */
  .model-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 10px;
    margin-bottom: 14px;
  }

  .model-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 14px 16px;
    display: flex;
    align-items: flex-start;
    gap: 12px;
  }

  .model-layer-badge {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding: 3px 8px;
    border-radius: 3px;
    white-space: nowrap;
    min-width: 85px;
    text-align: center;
    flex-shrink: 0;
    margin-top: 2px;
  }

  .layer-staging { background: rgba(56, 139, 253, 0.15); color: #58a6ff; border: 1px solid rgba(56, 139, 253, 0.3); }
  .layer-intermediate { background: rgba(210, 153, 34, 0.15); color: #d29922; border: 1px solid rgba(210, 153, 34, 0.3); }
  .layer-mart { background: rgba(63, 185, 80, 0.15); color: #3fb950; border: 1px solid rgba(63, 185, 80, 0.3); }

  .model-info { flex: 1; }

  .model-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    font-weight: 600;
    color: #e6edf3;
    margin-bottom: 2px;
  }

  .model-grain {
    font-size: 11px;
    color: #8b949e;
    margin-bottom: 3px;
  }

  .model-purpose {
    font-size: 12px;
    color: #c9d1d9;
  }

  /* LLM routing cards */
  .routing-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 14px;
  }

  .routing-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 14px 16px;
  }

  .routing-tier {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding: 3px 8px;
    border-radius: 3px;
    display: inline-block;
    margin-bottom: 6px;
  }

  .tier-restricted { background: rgba(248, 81, 73, 0.15); color: #f85149; border: 1px solid rgba(248, 81, 73, 0.3); }
  .tier-standard { background: rgba(56, 139, 253, 0.15); color: #58a6ff; border: 1px solid rgba(56, 139, 253, 0.3); }
  .tier-evaluation { background: rgba(210, 153, 34, 0.15); color: #d29922; border: 1px solid rgba(210, 153, 34, 0.3); }
  .tier-fallback { background: rgba(139, 148, 158, 0.15); color: #8b949e; border: 1px solid rgba(139, 148, 158, 0.3); }

  .routing-model {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #e6edf3;
    margin-bottom: 3px;
  }

  .routing-desc {
    font-size: 11px;
    color: #8b949e;
  }

  /* Eval table */
  .eval-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 14px;
  }

  .eval-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 14px 16px;
  }

  .eval-dim {
    font-size: 13px;
    font-weight: 600;
    color: #e6edf3;
    margin-bottom: 4px;
  }

  .eval-desc {
    font-size: 11px;
    color: #8b949e;
    margin-bottom: 6px;
  }

  .eval-target {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #3fb950;
    font-weight: 600;
  }

  /* Dashboard pages */
  .dash-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
    margin-bottom: 14px;
  }

  .dash-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 14px 16px;
    text-align: center;
  }

  .dash-icon {
    font-size: 24px;
    margin-bottom: 8px;
  }

  .dash-title {
    font-size: 13px;
    font-weight: 600;
    color: #e6edf3;
    margin-bottom: 4px;
  }

  .dash-desc {
    font-size: 11px;
    color: #8b949e;
  }

  /* code block */
  .code-block {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #c9d1d9;
    white-space: pre;
    overflow-x: auto;
    margin-bottom: 14px;
    line-height: 1.6;
  }

  .cmd { color: #79c0ff; }
  .comment { color: #8b949e; }

  /* Tech stack table */
  .stack-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 14px;
  }

  .stack-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 12px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .stack-label {
    font-size: 12px;
    color: #8b949e;
    font-weight: 500;
  }

  .stack-value {
    font-size: 12px;
    color: #e6edf3;
    font-weight: 600;
  }

  .footer-badges {
    display: flex;
    gap: 8px;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 24px;
  }

  .footer-badge {
    display: inline-flex;
    align-items: center;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    overflow: hidden;
    text-decoration: none;
    height: 28px;
  }

  .footer-badge .badge-left {
    padding: 0 10px;
    background: #333;
    color: #e6edf3;
    height: 100%;
    display: flex; align-items: center;
  }

  .footer-badge .badge-right {
    padding: 0 10px;
    height: 100%;
    display: flex; align-items: center;
    color: white;
  }

  .note-box {
    font-size: 12px;
    color: #8b949e;
    font-style: italic;
    margin-bottom: 14px;
  }
</style>
</head>
<body>
<div class="readme-container">

  <!-- HEADER -->
  <div class="center">
    <div class="logo-placeholder">NH</div>
    <h1>AI Health Coach</h1>
    <p class="tagline">Personalized health coaching from wearable biometric data using local LLMs</p>

    <div class="badges-row">
      <a class="badge badge-blue" href="#">
        <span class="badge-left">Demo</span>
        <span class="badge-right">coach.nicholashidalgo.com</span>
      </a>
      <a class="badge badge-yellow" href="#">
        <span class="badge-left">License</span>
        <span class="badge-right">MIT</span>
      </a>
      <a class="badge badge-green" href="#">
        <span class="badge-left">Tests</span>
        <span class="badge-right">15 passing</span>
      </a>
      <a class="badge badge-purple" href="#">
        <span class="badge-left">Models</span>
        <span class="badge-right">9 dbt</span>
      </a>
    </div>

    <div class="tech-badges">
      <span class="badge-flat" style="background:#3776AB;">Python 3.11+</span>
      <span class="badge-flat" style="background:#4169E1;">PostgreSQL</span>
      <span class="badge-flat" style="background:#FF694B;">dbt</span>
      <span class="badge-flat" style="background:#1C3C3C;">LiteLLM</span>
      <span class="badge-flat" style="background:#000;">Ollama</span>
      <span class="badge-flat" style="background:#2563EB;">Evidence.dev</span>
      <span class="badge-flat" style="background:#F48120;">Cloudflare Pages</span>
    </div>
  </div>

  <hr>

  <!-- WHAT THIS DOES -->
  <h3>What This Does</h3>
  <p>Generates personalized health coaching insights from synthetic wearable biometric data (HRV, sleep, recovery, strain) using locally-hosted LLMs. No paid API keys. No data leaves the machine.</p>
  <p>The pipeline: synthetic data generator loads 2K members and 200K+ daily biometric readings into PostgreSQL. dbt transforms raw data into coaching context windows with rolling 7/30-day averages and trend detection. LiteLLM routes prompts to local Ollama models with compliance-tier routing. A separate evaluation model scores each insight on relevance, specificity, actionability, and safety. Evidence.dev renders three dashboard pages showing coaching priorities, cohort retention, and AI quality metrics.</p>

  <hr>

  <!-- ARCHITECTURE -->
  <h3>Architecture</h3>
  <div class="arch-block">Synthetic Data Generator (Python, NumPy, Faker)
        |
        v
   PostgreSQL (raw schema)
        |
        v
   dbt (staging -> intermediate -> marts)
   - stg_members, stg_daily_metrics, stg_feature_events, stg_sessions
   - int_member_health_summary (7d/30d rolling avgs, trend detection)
   - int_feature_adoption (weekly engagement depth)
   - mart_coaching_context (biometrics + trends + engagement + priority)
   - mart_cohort_retention (D7/D14/D30/D60/D90)
   - mart_ai_evaluation (quality scores)
        |
        v
   LiteLLM Router (compliance tiers -> Ollama local models)
        |
        v
   Coaching Engine (segment-aware prompts, A/B variants, eval harness)
        |
        v
   Evidence.dev Dashboard (Cloudflare Pages)</div>

  <hr>

  <!-- dbt MODELS -->
  <h3>dbt Models</h3>
  <div class="model-grid">

    <div class="model-card">
      <span class="model-layer-badge layer-staging">Staging</span>
      <div class="model-info">
        <div class="model-name">stg_members</div>
        <div class="model-grain">1 row per member</div>
        <div class="model-purpose">Clean profiles with tenure calculation</div>
      </div>
    </div>

    <div class="model-card">
      <span class="model-layer-badge layer-staging">Staging</span>
      <div class="model-info">
        <div class="model-name">stg_daily_metrics</div>
        <div class="model-grain">1 row per member per day</div>
        <div class="model-purpose">Typed biometric readings with weekend flag</div>
      </div>
    </div>

    <div class="model-card">
      <span class="model-layer-badge layer-staging">Staging</span>
      <div class="model-info">
        <div class="model-name">stg_feature_events</div>
        <div class="model-grain">1 row per event</div>
        <div class="model-purpose">Clean engagement events</div>
      </div>
    </div>

    <div class="model-card">
      <span class="model-layer-badge layer-staging">Staging</span>
      <div class="model-info">
        <div class="model-name">stg_sessions</div>
        <div class="model-grain">1 row per session</div>
        <div class="model-purpose">Clean app sessions</div>
      </div>
    </div>

    <div class="model-card">
      <span class="model-layer-badge layer-intermediate">Intermediate</span>
      <div class="model-info">
        <div class="model-name">int_member_health_summary</div>
        <div class="model-grain">1 row per member per day</div>
        <div class="model-purpose">7d/30d rolling averages, HRV and recovery trends</div>
      </div>
    </div>

    <div class="model-card">
      <span class="model-layer-badge layer-intermediate">Intermediate</span>
      <div class="model-info">
        <div class="model-name">int_feature_adoption</div>
        <div class="model-grain">1 row per member per feature</div>
        <div class="model-purpose">Lifetime adoption depth and interaction rates</div>
      </div>
    </div>

    <div class="model-card">
      <span class="model-layer-badge layer-mart">Mart</span>
      <div class="model-info">
        <div class="model-name">mart_coaching_context</div>
        <div class="model-grain">1 row per active member</div>
        <div class="model-purpose">Full coaching input: biometrics + trends + engagement + priority</div>
      </div>
    </div>

    <div class="model-card">
      <span class="model-layer-badge layer-mart">Mart</span>
      <div class="model-info">
        <div class="model-name">mart_cohort_retention</div>
        <div class="model-grain">1 row per cohort-week / plan / channel / segment</div>
        <div class="model-purpose">Point-in-time retention at D7/D14/D30/D60/D90</div>
      </div>
    </div>

    <div class="model-card">
      <span class="model-layer-badge layer-mart">Mart</span>
      <div class="model-info">
        <div class="model-name">mart_ai_evaluation</div>
        <div class="model-grain">1 row per generated insight</div>
        <div class="model-purpose">Quality scores from evaluation model</div>
      </div>
    </div>

  </div>

  <hr>

  <!-- LLM ROUTING -->
  <h3>LLM Routing</h3>
  <p class="note-box">All models run locally via Ollama. No API keys needed.</p>
  <div class="routing-grid">
    <div class="routing-card">
      <span class="routing-tier tier-restricted">Restricted</span>
      <div class="routing-model">ollama/gemma3:12b</div>
      <div class="routing-desc">PHI-adjacent context. Health data never leaves local machine.</div>
    </div>
    <div class="routing-card">
      <span class="routing-tier tier-standard">Standard</span>
      <div class="routing-model">ollama/gemma3:12b</div>
      <div class="routing-desc">Primary coaching generation model.</div>
    </div>
    <div class="routing-card">
      <span class="routing-tier tier-evaluation">Evaluation</span>
      <div class="routing-model">ollama/gemma3:12b</div>
      <div class="routing-desc">Separate evaluation pass for quality scoring.</div>
    </div>
    <div class="routing-card">
      <span class="routing-tier tier-fallback">Fallback</span>
      <div class="routing-model">ollama/llama3.1:8b</div>
      <div class="routing-desc">Lighter backup when primary model is down.</div>
    </div>
  </div>

  <hr>

  <!-- EVALUATION FRAMEWORK -->
  <h3>Evaluation Framework</h3>
  <p class="note-box">Each generated insight is scored by a separate LLM call on four dimensions:</p>
  <div class="eval-grid">
    <div class="eval-card">
      <div class="eval-dim">Relevance</div>
      <div class="eval-desc">Does it reference the member's actual data?</div>
      <div class="eval-target">Target: >70</div>
    </div>
    <div class="eval-card">
      <div class="eval-dim">Specificity</div>
      <div class="eval-desc">Does it include specific numbers and timeframes?</div>
      <div class="eval-target">Target: >60</div>
    </div>
    <div class="eval-card">
      <div class="eval-dim">Actionability</div>
      <div class="eval-desc">Can the member act on this in 48 hours?</div>
      <div class="eval-target">Target: >70</div>
    </div>
    <div class="eval-card">
      <div class="eval-dim">Safety</div>
      <div class="eval-desc">Does it avoid medical claims or dangerous advice?</div>
      <div class="eval-target">Target: >90</div>
    </div>
  </div>

  <hr>

  <!-- DASHBOARD -->
  <h3>Evidence Dashboard</h3>
  <div class="dash-grid">
    <div class="dash-card">
      <div class="dash-icon">📊</div>
      <div class="dash-title">Coaching Insights</div>
      <div class="dash-desc">Priority distribution, segment trends, recent generated insights</div>
    </div>
    <div class="dash-card">
      <div class="dash-icon">📈</div>
      <div class="dash-title">Cohort Retention</div>
      <div class="dash-desc">Retention curves by plan, channel, segment at D7-D90</div>
    </div>
    <div class="dash-card">
      <div class="dash-icon">🤖</div>
      <div class="dash-title">AI Evaluation</div>
      <div class="dash-desc">A/B comparison, quality scores, safety flag rates</div>
    </div>
  </div>

  <hr>

  <!-- QUICK START -->
  <h3>Quick Start</h3>
  <div class="code-block"><span class="cmd">git clone</span> https://github.com/nicholasjh-work/ai-health-coach.git
<span class="cmd">cd</span> ai-health-coach

<span class="cmd">python -m venv</span> .venv && <span class="cmd">source</span> .venv/bin/activate
<span class="cmd">pip install</span> -e ".[dev]"
<span class="cmd">cp</span> .env.example .env

<span class="comment"># Create database</span>
<span class="cmd">createdb</span> ai_health_coach

<span class="comment"># Load synthetic data</span>
<span class="cmd">python -m</span> src.data_gen.generate

<span class="comment"># Run dbt transformations</span>
<span class="cmd">cd</span> src/dbt_project && <span class="cmd">dbt run</span> --profiles-dir . && <span class="cmd">cd</span> ../..

<span class="comment"># Generate coaching insights</span>
<span class="cmd">python -m</span> src.cli insights --n 20 --version v1

<span class="comment"># Run A/B variant</span>
<span class="cmd">python -m</span> src.cli insights --n 20 --version v2

<span class="comment"># View evaluation summary</span>
<span class="cmd">python -m</span> src.cli evaluate

<span class="comment"># Launch Evidence dashboard</span>
<span class="cmd">cd</span> evidence && <span class="cmd">npx evidence dev</span></div>

  <hr>

  <!-- TECH STACK -->
  <h3>Tech Stack</h3>
  <div class="stack-grid">
    <div class="stack-card">
      <span class="stack-label">Database</span>
      <span class="stack-value">PostgreSQL</span>
    </div>
    <div class="stack-card">
      <span class="stack-label">Transformations</span>
      <span class="stack-value">dbt</span>
    </div>
    <div class="stack-card">
      <span class="stack-label">LLM Routing</span>
      <span class="stack-value">LiteLLM + Ollama</span>
    </div>
    <div class="stack-card">
      <span class="stack-label">Evaluation</span>
      <span class="stack-value">Structured LLM + JSON</span>
    </div>
    <div class="stack-card">
      <span class="stack-label">Dashboard</span>
      <span class="stack-value">Evidence.dev</span>
    </div>
    <div class="stack-card">
      <span class="stack-label">Deployment</span>
      <span class="stack-value">Cloudflare Pages</span>
    </div>
    <div class="stack-card">
      <span class="stack-label">Language</span>
      <span class="stack-value">Python 3.11</span>
    </div>
    <div class="stack-card">
      <span class="stack-label">CI</span>
      <span class="stack-value">GitHub Actions</span>
    </div>
  </div>

  <hr>

  <!-- TESTS -->
  <h3>Tests</h3>
  <div class="code-block"><span class="cmd">pytest</span> tests/ -v</div>
  <p>15 unit tests covering data generation bounds, prompt construction, router compliance tier routing, and segment-aware tone matching.</p>

  <hr>

  <!-- FOOTER -->
  <div class="center">
    <div class="footer-badges">
      <a class="footer-badge" href="#">
        <span class="badge-left">LinkedIn</span>
        <span class="badge-right" style="background:#0A66C2;">Nicholas Hidalgo</span>
      </a>
      <a class="footer-badge" href="#">
        <span class="badge-left">Website</span>
        <span class="badge-right" style="background:#000;">nicholashidalgo.com</span>
      </a>
      <a class="footer-badge" href="#">
        <span class="badge-left">Email</span>
        <span class="badge-right" style="background:#EA4335;">analytics@nicholashidalgo.com</span>
      </a>
    </div>
  </div>

</div>
</body>
</html>
