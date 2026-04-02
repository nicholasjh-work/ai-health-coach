-- mart_coaching_context.sql
-- One row per member: latest biometrics, trends, top features, segment.
-- This is the primary input to the AI coaching engine.

with members as (
    select * from {{ ref('stg_members') }}
),

latest_health as (
    select *
    from {{ ref('int_member_health_summary') }}
    where recency_rank = 1
),

top_features as (
    select
        member_id,
        array_agg(feature_name order by lifetime_interactions desc) as top_features,
        count(distinct feature_name) as features_used_count
    from {{ ref('int_feature_adoption') }}
    where lifetime_interactions > 0
    group by member_id
),

sessions_summary as (
    select
        member_id,
        count(*) as total_sessions,
        round(avg(duration_seconds)::numeric, 0) as avg_session_duration_sec,
        max(session_date) as last_session_date,
        count(distinct session_date) as active_days
    from {{ ref('stg_sessions') }}
    group by member_id
)

select
    m.member_id,
    m.plan_type,
    m.segment,
    m.age,
    m.gender,
    m.signup_date,
    m.tenure_days,
    m.is_churned,
    m.ab_test_group,

    -- Latest biometrics
    h.metric_date as latest_metric_date,
    h.hrv_ms as latest_hrv,
    h.resting_hr_bpm as latest_rhr,
    h.sleep_hours as latest_sleep_hours,
    h.sleep_score as latest_sleep_score,
    h.recovery_score as latest_recovery,
    h.strain_score as latest_strain,
    h.steps as latest_steps,

    -- Trends
    round(h.hrv_7d_avg::numeric, 1) as hrv_7d_avg,
    round(h.hrv_30d_avg::numeric, 1) as hrv_30d_avg,
    h.hrv_trend,
    round(h.recovery_7d_avg::numeric, 1) as recovery_7d_avg,
    h.recovery_trend,

    -- Engagement
    coalesce(f.features_used_count, 0) as features_used_count,
    f.top_features,
    coalesce(s.total_sessions, 0) as total_sessions,
    coalesce(s.avg_session_duration_sec, 0) as avg_session_duration_sec,
    s.last_session_date,
    coalesce(s.active_days, 0) as session_active_days,

    -- Coaching priority score: higher = needs more attention
    case
        when m.is_churned then 0  -- already lost
        when h.recovery_trend = 'declining' and h.hrv_trend = 'declining' then 95
        when h.recovery_trend = 'declining' then 80
        when h.hrv_trend = 'declining' then 70
        when coalesce(s.active_days, 0) < m.tenure_days * 0.3 then 60
        when h.recovery_trend = 'improving' then 30
        else 50
    end as coaching_priority_score

from members m
left join latest_health h on m.member_id = h.member_id
left join top_features f on m.member_id = f.member_id
left join sessions_summary s on m.member_id = s.member_id
where not m.is_churned
