---
title: Cohort Retention
---

# Cohort Retention Analysis
```sql retention_by_plan
select
    plan_type,
    sum(cohort_size) as total_members,
    round(avg(retention_d7_pct), 1) as d7,
    round(avg(retention_d14_pct), 1) as d14,
    round(avg(retention_d30_pct), 1) as d30,
    round(avg(retention_d60_pct), 1) as d60,
    round(avg(retention_d90_pct), 1) as d90
from health_coach.cohort_retention
group by plan_type
order by plan_type
```

<DataTable data={retention_by_plan} />

## Retention Curves by Plan Type
```sql retention_curve
select plan_type, 'D7' as period, avg(retention_d7_pct) as retention_pct from health_coach.cohort_retention group by 1
union all
select plan_type, 'D14', avg(retention_d14_pct) from health_coach.cohort_retention group by 1
union all
select plan_type, 'D30', avg(retention_d30_pct) from health_coach.cohort_retention group by 1
union all
select plan_type, 'D60', avg(retention_d60_pct) from health_coach.cohort_retention group by 1
union all
select plan_type, 'D90', avg(retention_d90_pct) from health_coach.cohort_retention group by 1
order by plan_type, period
```

<LineChart
    data={retention_curve}
    x=period
    y=retention_pct
    series=plan_type
    title="Retention Curves by Plan Type"
    yAxisTitle="Retention %"
/>

## Retention by Acquisition Channel
```sql retention_by_channel
select
    acquisition_channel,
    sum(cohort_size) as total_members,
    round(avg(retention_d7_pct), 1) as d7,
    round(avg(retention_d30_pct), 1) as d30,
    round(avg(retention_d90_pct), 1) as d90
from health_coach.cohort_retention
group by acquisition_channel
order by d90 desc
```

<BarChart
    data={retention_by_channel}
    x=acquisition_channel
    y={["d7", "d30", "d90"]}
    type=grouped
    title="Retention by Acquisition Channel"
/>

## Retention by Segment
```sql retention_by_segment
select
    segment,
    sum(cohort_size) as total_members,
    round(avg(retention_d7_pct), 1) as d7,
    round(avg(retention_d30_pct), 1) as d30,
    round(avg(retention_d90_pct), 1) as d90
from health_coach.cohort_retention
group by segment
order by d90 desc
```

<BarChart
    data={retention_by_segment}
    x=segment
    y={["d7", "d30", "d90"]}
    type=grouped
    title="Retention by Member Segment"
/>
