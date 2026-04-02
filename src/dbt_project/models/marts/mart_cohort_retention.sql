-- mart_cohort_retention.sql
-- Weekly cohort retention by signup week, plan type, and acquisition channel.
-- Point-in-time retention windows at 7, 14, 30, 60, 90 days.

with members as (
    select * from {{ ref('stg_members') }}
),

sessions as (
    select * from {{ ref('stg_sessions') }}
),

cohorts as (
    select
        member_id,
        date_trunc('week', signup_date)::date as cohort_week,
        plan_type,
        acquisition_channel,
        segment
    from members
),

member_activity as (
    select
        c.member_id,
        c.cohort_week,
        c.plan_type,
        c.acquisition_channel,
        c.segment,
        s.session_date,
        (s.session_date - c.cohort_week::date) as days_since_signup
    from cohorts c
    inner join sessions s on c.member_id = s.member_id
),

retention_flags as (
    select
        cohort_week,
        plan_type,
        acquisition_channel,
        segment,
        member_id,
        max(case when days_since_signup between 1 and 7 then 1 else 0 end) as retained_d7,
        max(case when days_since_signup between 1 and 14 then 1 else 0 end) as retained_d14,
        max(case when days_since_signup between 1 and 30 then 1 else 0 end) as retained_d30,
        max(case when days_since_signup between 1 and 60 then 1 else 0 end) as retained_d60,
        max(case when days_since_signup between 1 and 90 then 1 else 0 end) as retained_d90
    from member_activity
    group by 1, 2, 3, 4, 5
)

select
    cohort_week,
    plan_type,
    acquisition_channel,
    segment,
    count(distinct member_id) as cohort_size,
    round(avg(retained_d7) * 100, 1) as retention_d7_pct,
    round(avg(retained_d14) * 100, 1) as retention_d14_pct,
    round(avg(retained_d30) * 100, 1) as retention_d30_pct,
    round(avg(retained_d60) * 100, 1) as retention_d60_pct,
    round(avg(retained_d90) * 100, 1) as retention_d90_pct
from retention_flags
group by 1, 2, 3, 4
order by cohort_week
