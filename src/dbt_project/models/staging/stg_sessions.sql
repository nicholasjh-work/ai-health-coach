-- stg_sessions.sql
-- Clean and type-cast raw app sessions.

with source as (
    select * from {{ source('raw', 'sessions') }}
)

select
    member_id,
    session_date::date as session_date,
    session_start::timestamp as session_start,
    duration_seconds::integer as duration_seconds,
    platform
from source
