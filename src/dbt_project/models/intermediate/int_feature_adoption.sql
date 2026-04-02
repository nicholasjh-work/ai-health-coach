-- int_feature_adoption.sql
-- Weekly feature adoption rates and engagement depth per member.

with events as (
    select * from {{ ref('stg_feature_events') }}
),

weekly_adoption as (
    select
        member_id,
        feature_name,
        date_trunc('week', event_date)::date as week_start,
        count(*) as total_events,
        count(*) filter (where event_type = 'interact') as interactions,
        count(*) filter (where event_type = 'dismiss') as dismissals,
        sum(duration_seconds) as total_duration_seconds,
        count(distinct event_date) as active_days
    from events
    group by 1, 2, 3
),

member_feature_summary as (
    select
        member_id,
        feature_name,
        count(distinct week_start) as weeks_used,
        sum(total_events) as lifetime_events,
        sum(interactions) as lifetime_interactions,
        sum(dismissals) as lifetime_dismissals,
        round(
            sum(interactions)::numeric / nullif(sum(total_events), 0) * 100, 1
        ) as interaction_rate_pct,
        round(avg(total_duration_seconds)::numeric, 0) as avg_weekly_duration_sec
    from weekly_adoption
    group by 1, 2
)

select * from member_feature_summary
