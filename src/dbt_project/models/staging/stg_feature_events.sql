-- stg_feature_events.sql
-- Clean and type-cast raw feature engagement events.

with source as (
    select * from {{ source('raw', 'feature_events') }}
)

select
    member_id,
    event_date::date as event_date,
    feature_name,
    event_type,
    duration_seconds::integer as duration_seconds
from source
