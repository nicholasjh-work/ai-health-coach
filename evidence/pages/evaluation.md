---
title: AI Evaluation
---

# AI Coaching Evaluation
```sql eval_summary
select
    prompt_version,
    model_name,
    count(*) as insights_generated,
    round(avg(relevance_score), 1) as avg_relevance,
    round(avg(specificity_score), 1) as avg_specificity,
    round(avg(actionability_score), 1) as avg_actionability,
    round(avg(safety_score), 1) as avg_safety,
    round((avg(relevance_score) + avg(specificity_score) + avg(actionability_score) + avg(safety_score)) / 4, 1) as avg_composite,
    round(avg(word_count), 0) as avg_word_count
from health_coach.ai_evaluations
group by 1, 2
order by avg_composite desc
```

<DataTable data={eval_summary} />

## Prompt Version A/B Comparison
```sql ab_comparison
select
    prompt_version,
    round(avg(relevance_score), 1) as relevance,
    round(avg(specificity_score), 1) as specificity,
    round(avg(actionability_score), 1) as actionability,
    round(avg(safety_score), 1) as safety
from health_coach.ai_evaluations
group by 1
```

<BarChart
    data={ab_comparison}
    x=prompt_version
    y={["relevance", "specificity", "actionability", "safety"]}
    type=grouped
    title="Quality Scores by Prompt Version (A/B Test)"
/>

## Score Distribution
```sql score_distribution
select
    case
        when (relevance_score + specificity_score + actionability_score + safety_score) / 4.0 >= 80 then 'Excellent (80+)'
        when (relevance_score + specificity_score + actionability_score + safety_score) / 4.0 >= 60 then 'Good (60-79)'
        when (relevance_score + specificity_score + actionability_score + safety_score) / 4.0 >= 40 then 'Fair (40-59)'
        else 'Poor (<40)'
    end as quality_band,
    count(*) as insight_count
from health_coach.ai_evaluations
group by 1
order by min((relevance_score + specificity_score + actionability_score + safety_score) / 4.0) desc
```

<BarChart
    data={score_distribution}
    x=quality_band
    y=insight_count
    title="Insight Quality Distribution"
/>

## Top Scored Insights
```sql top_insights
select
    member_id,
    prompt_version,
    round((relevance_score + specificity_score + actionability_score + safety_score) / 4.0, 0) as composite,
    relevance_score,
    specificity_score,
    actionability_score,
    safety_score,
    insight_text
from health_coach.ai_evaluations
order by (relevance_score + specificity_score + actionability_score + safety_score) desc
limit 10
```

<DataTable data={top_insights} search=true />
