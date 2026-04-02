---
title: AI Health Coach
---

# AI Health Coach

Personalized coaching insights generated from wearable biometric data using local LLMs.
```sql member_overview
select
    segment,
    count(*) as members,
    round(avg(coaching_priority_score), 0) as avg_priority,
    round(avg(latest_recovery), 0) as avg_recovery,
    round(avg(latest_sleep_hours)::numeric, 1) as avg_sleep_hours,
    round(avg(hrv_7d_avg)::numeric, 0) as avg_hrv_7d
from health_coach.coaching_context
group by segment
order by avg_priority desc
```

<DataTable data={member_overview} />

## Coaching Priority Distribution
```sql priority_distribution
select
    case
        when coaching_priority_score >= 90 then 'Critical (90+)'
        when coaching_priority_score >= 70 then 'High (70-89)'
        when coaching_priority_score >= 50 then 'Medium (50-69)'
        else 'Low (<50)'
    end as priority_band,
    count(*) as member_count,
    round(avg(latest_recovery), 0) as avg_recovery,
    round(avg(hrv_7d_avg)::numeric, 0) as avg_hrv
from health_coach.coaching_context
group by 1
order by min(coaching_priority_score) desc
```

<BarChart
    data={priority_distribution}
    x=priority_band
    y=member_count
    title="Members by Coaching Priority"
/>

## HRV Trends by Segment
```sql segment_trends
select
    segment,
    hrv_trend,
    count(*) as members
from health_coach.coaching_context
group by 1, 2
order by 1, 2
```

<BarChart
    data={segment_trends}
    x=segment
    y=members
    series=hrv_trend
    type=grouped
    title="HRV Trend Distribution by Segment"
/>

## Recent Coaching Insights
```sql recent_insights
select
    member_id,
    prompt_version,
    model_name,
    round((relevance_score + specificity_score + actionability_score + safety_score) / 4.0, 0) as composite_score,
    word_count,
    left(insight_text, 150) || '...' as insight_preview,
    generated_at::date as generated_date
from health_coach.ai_evaluations
order by generated_at desc
limit 20
```

<DataTable data={recent_insights} search=true />
