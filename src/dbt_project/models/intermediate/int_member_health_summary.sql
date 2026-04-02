-- int_member_health_summary.sql
-- Rolling 7-day and 30-day biometric averages per member.
-- Computes trend direction for coaching context.

with daily as (
    select * from {{ ref('stg_daily_metrics') }}
),

rolling as (
    select
        member_id,
        metric_date,
        hrv_ms,
        resting_hr_bpm,
        sleep_hours,
        sleep_score,
        recovery_score,
        strain_score,
        steps,

        -- 7-day rolling averages
        avg(hrv_ms) over (
            partition by member_id order by metric_date
            rows between 6 preceding and current row
        ) as hrv_7d_avg,
        avg(sleep_hours) over (
            partition by member_id order by metric_date
            rows between 6 preceding and current row
        ) as sleep_7d_avg,
        avg(recovery_score) over (
            partition by member_id order by metric_date
            rows between 6 preceding and current row
        ) as recovery_7d_avg,
        avg(strain_score) over (
            partition by member_id order by metric_date
            rows between 6 preceding and current row
        ) as strain_7d_avg,

        -- 30-day rolling averages
        avg(hrv_ms) over (
            partition by member_id order by metric_date
            rows between 29 preceding and current row
        ) as hrv_30d_avg,
        avg(recovery_score) over (
            partition by member_id order by metric_date
            rows between 29 preceding and current row
        ) as recovery_30d_avg,

        -- Row number for recency
        row_number() over (
            partition by member_id order by metric_date desc
        ) as recency_rank

    from daily
)

select
    *,
    -- Trend: compare 7-day avg to 30-day avg
    case
        when hrv_7d_avg > hrv_30d_avg * 1.05 then 'improving'
        when hrv_7d_avg < hrv_30d_avg * 0.95 then 'declining'
        else 'stable'
    end as hrv_trend,
    case
        when recovery_7d_avg > recovery_30d_avg * 1.05 then 'improving'
        when recovery_7d_avg < recovery_30d_avg * 0.95 then 'declining'
        else 'stable'
    end as recovery_trend
from rolling
