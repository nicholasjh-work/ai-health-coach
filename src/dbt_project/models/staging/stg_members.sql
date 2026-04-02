-- stg_members.sql
-- Clean and type-cast raw member profiles.

with source as (
    select * from {{ source('raw', 'members') }}
)

select
    member_id,
    signup_date::date as signup_date,
    plan_type,
    acquisition_channel,
    segment,
    age,
    gender,
    is_churned::boolean as is_churned,
    churn_date::date as churn_date,
    ab_test_group,
    case
        when churn_date is not null
        then (churn_date::date - signup_date::date)
        else (current_date - signup_date::date)
    end as tenure_days
from source
