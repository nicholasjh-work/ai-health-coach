-- mart_ai_evaluation.sql
-- Tracks AI-generated coaching insights, their quality scores, and A/B test attribution.
-- Populated by the evaluation harness after each coaching generation run.
-- This model reads from a table written by the Python evaluation engine.

with evaluations as (
    select * from {{ source('raw', 'ai_evaluations') }}
)

select
    evaluation_id,
    member_id,
    generated_at::timestamp as generated_at,
    model_name,
    prompt_version,
    insight_type,
    insight_text,
    
    -- Quality scores (0-100)
    relevance_score::integer as relevance_score,
    specificity_score::integer as specificity_score,
    actionability_score::integer as actionability_score,
    safety_score::integer as safety_score,
    
    -- Composite
    round(
        (relevance_score + specificity_score + actionability_score + safety_score)::numeric / 4, 1
    ) as composite_score,
    
    -- Flags
    contains_medical_claim::boolean as contains_medical_claim,
    contains_specific_numbers::boolean as contains_specific_numbers,
    word_count::integer as word_count,
    
    -- A/B context
    ab_test_group,
    prompt_variant
from evaluations
