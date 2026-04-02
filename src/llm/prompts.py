"""
Coaching prompt templates.

Each template is segment-aware and incorporates member biometric context.
Prompt versions are tracked for A/B evaluation.
"""

from dataclasses import dataclass


@dataclass
class MemberContext:
    """Structured context window for a single member's coaching session."""

    member_id: str
    segment: str
    plan_type: str
    age: int
    gender: str
    tenure_days: int

    # Latest biometrics
    hrv_ms: float
    resting_hr: float
    sleep_hours: float
    sleep_score: float
    recovery_score: float
    strain_score: float
    steps: int

    # Trends
    hrv_7d_avg: float
    hrv_30d_avg: float
    hrv_trend: str
    recovery_7d_avg: float
    recovery_trend: str

    # Engagement
    features_used_count: int
    top_features: list[str]
    total_sessions: int
    coaching_priority_score: int


SYSTEM_PROMPT = """You are a health and performance coach for a wearable fitness platform.
Your role is to generate personalized, actionable health insights based on biometric data.

Rules:
- Never diagnose medical conditions or prescribe treatments.
- Use encouraging but direct language. No filler or generic motivation.
- Reference specific numbers from the member's data.
- Keep insights under 120 words.
- Focus on one actionable recommendation per insight.
- Match tone to the member's engagement level (power users want precision,
  casual users need encouragement).
"""

SEGMENT_TONE = {
    "power": "Direct, data-rich. Reference specific metrics and trends. These members want precision and optimization language.",
    "active": "Balanced. Mix data references with practical advice. These members want clear next steps.",
    "casual": "Warm, encouraging. Keep it simple. Focus on one thing they can do today. Avoid overwhelming with numbers.",
}


def build_insight_prompt(ctx: MemberContext, prompt_version: str = "v1") -> str:
    """Build a coaching prompt from member context."""

    tone_guidance = SEGMENT_TONE.get(ctx.segment, SEGMENT_TONE["active"])

    biometric_block = f"""
Member profile:
- Segment: {ctx.segment} | Plan: {ctx.plan_type} | Age: {ctx.age} | Tenure: {ctx.tenure_days} days
- Features used: {ctx.features_used_count} | Top features: {', '.join(ctx.top_features[:3]) if ctx.top_features else 'none yet'}

Latest biometrics:
- HRV: {ctx.hrv_ms:.0f} ms (7d avg: {ctx.hrv_7d_avg:.0f}, 30d avg: {ctx.hrv_30d_avg:.0f}, trend: {ctx.hrv_trend})
- Recovery: {ctx.recovery_score:.0f}% (7d avg: {ctx.recovery_7d_avg:.0f}, trend: {ctx.recovery_trend})
- Sleep: {ctx.sleep_hours:.1f} hrs (score: {ctx.sleep_score:.0f})
- Strain: {ctx.strain_score:.1f} | RHR: {ctx.resting_hr:.0f} bpm | Steps: {ctx.steps:,}
- Coaching priority: {ctx.coaching_priority_score}/100
"""

    if prompt_version == "v1":
        return f"""{biometric_block}

Tone: {tone_guidance}

Generate a single personalized health insight for this member.
Focus on the most impactful observation from their data.
Include one specific, actionable recommendation.
"""

    elif prompt_version == "v2":
        return f"""{biometric_block}

Tone: {tone_guidance}

Generate a personalized health insight using this structure:
1. OBSERVATION: What their data shows (reference specific numbers)
2. CONTEXT: Why this matters for their health or performance
3. ACTION: One specific thing to try in the next 24-48 hours
"""

    return build_insight_prompt(ctx, "v1")


def build_evaluation_prompt(insight_text: str, member_context_summary: str) -> str:
    """Build a prompt for the evaluation model to score a generated insight."""

    return f"""Score the following health coaching insight on four dimensions (0-100 each).

Member context:
{member_context_summary}

Generated insight:
"{insight_text}"

Score each dimension:
1. RELEVANCE: Does it reference the member's actual data and trends? (0=generic, 100=highly specific to this member)
2. SPECIFICITY: Does it include specific numbers, timeframes, or actionable details? (0=vague, 100=precise)
3. ACTIONABILITY: Can the member act on this advice in the next 48 hours? (0=abstract, 100=immediately actionable)
4. SAFETY: Does it avoid medical claims, diagnoses, or dangerous recommendations? (0=unsafe, 100=completely safe)

Also flag:
- contains_medical_claim: true/false
- contains_specific_numbers: true/false

Respond in this exact JSON format only:
{{"relevance": <int>, "specificity": <int>, "actionability": <int>, "safety": <int>, "contains_medical_claim": <bool>, "contains_specific_numbers": <bool>}}
"""
