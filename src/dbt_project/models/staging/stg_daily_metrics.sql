-- stg_daily_metrics.sql
-- Clean and type-cast raw daily biometric readings.

with source as (
    select * from {{ source('raw', 'daily_metrics') }}
)

select
    member_id,
    metric_date::date as metric_date,
    round(hrv_ms::numeric, 1) as hrv_ms,
    round(resting_hr_bpm::numeric, 0) as resting_hr_bpm,
    round(sleep_hours::numeric, 1) as sleep_hours,
    round(sleep_score::numeric, 0) as sleep_score,
    round(recovery_score::numeric, 0) as recovery_score,
    round(strain_score::numeric, 1) as strain_score,
    round(respiratory_rate::numeric, 1) as respiratory_rate,
    round(skin_temp_delta_c::numeric, 2) as skin_temp_delta_c,
    round(spo2_pct::numeric, 1) as spo2_pct,
    steps::integer as steps,
    extract(dow from metric_date::date) as day_of_week,
    case when extract(dow from metric_date::date) in (0, 6) then true else false end as is_weekend
from source
