"""
Coaching engine.

Generates personalized health insights for members using their biometric
context from mart_coaching_context, then evaluates output quality using
a separate LLM call through the evaluation tier.
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine, text

from .prompts import (
    SYSTEM_PROMPT,
    MemberContext,
    build_evaluation_prompt,
    build_insight_prompt,
)
from .router import ComplianceTier, generate

logger = logging.getLogger(__name__)


def _row_to_context(row: pd.Series) -> MemberContext:
    """Convert a mart_coaching_context row to MemberContext."""
    top_features = row.get("top_features")
    if isinstance(top_features, str):
        top_features = [f.strip().strip("{}\"'") for f in top_features.split(",")]
    elif top_features is None:
        top_features = []

    return MemberContext(
        member_id=row["member_id"],
        segment=row["segment"],
        plan_type=row["plan_type"],
        age=int(row["age"]),
        gender=row["gender"],
        tenure_days=int(row["tenure_days"]),
        hrv_ms=float(row.get("latest_hrv", 0)),
        resting_hr=float(row.get("latest_rhr", 0)),
        sleep_hours=float(row.get("latest_sleep_hours", 0)),
        sleep_score=float(row.get("latest_sleep_score", 0)),
        recovery_score=float(row.get("latest_recovery", 0)),
        strain_score=float(row.get("latest_strain", 0)),
        steps=int(row.get("latest_steps", 0)),
        hrv_7d_avg=float(row.get("hrv_7d_avg", 0)),
        hrv_30d_avg=float(row.get("hrv_30d_avg", 0)),
        hrv_trend=row.get("hrv_trend", "stable"),
        recovery_7d_avg=float(row.get("recovery_7d_avg", 0)),
        recovery_trend=row.get("recovery_trend", "stable"),
        features_used_count=int(row.get("features_used_count", 0)),
        top_features=top_features,
        total_sessions=int(row.get("total_sessions", 0)),
        coaching_priority_score=int(row.get("coaching_priority_score", 50)),
    )


async def generate_insight(
    ctx: MemberContext,
    prompt_version: str = "v1",
) -> dict:
    """Generate a single coaching insight for a member."""
    prompt = build_insight_prompt(ctx, prompt_version)

    result = await generate(
        prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
        tier=ComplianceTier.STANDARD,
        temperature=0.7,
    )

    return {
        "member_id": ctx.member_id,
        "insight_text": result["text"],
        "model_name": result["model"],
        "prompt_version": prompt_version,
        "insight_type": "daily_coaching",
        "generated_at": datetime.utcnow().isoformat(),
        "ab_test_group": "treatment" if prompt_version == "v2" else "control",
        "prompt_variant": prompt_version,
    }


async def evaluate_insight(
    insight_text: str,
    member_context_summary: str,
) -> dict:
    """Score a generated insight using the evaluation model."""
    prompt = build_evaluation_prompt(insight_text, member_context_summary)

    result = await generate(
        prompt=prompt,
        system_prompt="You are a quality evaluator. Respond only in valid JSON.",
        tier=ComplianceTier.EVALUATION,
        temperature=0.1,
        max_tokens=256,
    )

    try:
        raw = result["text"]
        # Try to extract JSON from the response
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start >= 0 and end > start:
            scores = json.loads(raw[start:end])
        else:
            scores = {}
    except (json.JSONDecodeError, ValueError):
        logger.warning(f"Failed to parse evaluation response: {result['text'][:200]}")
        scores = {
            "relevance": 50, "specificity": 50,
            "actionability": 50, "safety": 50,
            "contains_medical_claim": False,
            "contains_specific_numbers": False,
        }

    return scores


async def run_coaching_batch(
    connection_string: str,
    n_members: int = 20,
    prompt_version: str = "v1",
) -> list[dict]:
    """
    Run coaching generation for a batch of high-priority members.
    Generates insights, evaluates them, and stores results.
    """
    engine = create_engine(connection_string)

    query = text("""
        SELECT * FROM public_marts.mart_coaching_context
        ORDER BY coaching_priority_score DESC
        LIMIT :n
    """)

    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"n": n_members})

    if df.empty:
        logger.warning("No members found in mart_coaching_context. Run dbt first.")
        return []

    results = []
    for _, row in df.iterrows():
        ctx = _row_to_context(row)

        # Generate insight
        insight = await generate_insight(ctx, prompt_version)

        # Evaluate quality
        context_summary = (
            f"Segment: {ctx.segment}, HRV trend: {ctx.hrv_trend}, "
            f"Recovery: {ctx.recovery_score:.0f}%, Sleep: {ctx.sleep_hours:.1f}h"
        )
        scores = await evaluate_insight(insight["insight_text"], context_summary)

        # Combine
        evaluation = {
            "evaluation_id": str(uuid.uuid4()),
            **insight,
            "relevance_score": scores.get("relevance", 50),
            "specificity_score": scores.get("specificity", 50),
            "actionability_score": scores.get("actionability", 50),
            "safety_score": scores.get("safety", 50),
            "contains_medical_claim": scores.get("contains_medical_claim", False),
            "contains_specific_numbers": scores.get("contains_specific_numbers", False),
            "word_count": len(insight["insight_text"].split()),
        }
        results.append(evaluation)
        logger.info(
            f"Generated insight for {ctx.member_id} "
            f"(priority={ctx.coaching_priority_score}, "
            f"composite={sum(scores.get(k, 50) for k in ['relevance','specificity','actionability','safety'])/4:.0f})"
        )

    # Store evaluations
    if results:
        eval_df = pd.DataFrame(results)
        with engine.begin() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))
        eval_df.to_sql(
            "ai_evaluations",
            engine,
            schema="raw",
            if_exists="append",
            index=False,
        )
        logger.info(f"Stored {len(results)} evaluations in raw.ai_evaluations")

    return results
