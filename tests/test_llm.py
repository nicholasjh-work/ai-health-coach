"""Tests for prompt generation and router configuration."""

import pytest

from src.llm.prompts import MemberContext, build_evaluation_prompt, build_insight_prompt
from src.llm.router import ComplianceTier, RouterConfig, _select_model


@pytest.fixture
def sample_context() -> MemberContext:
    return MemberContext(
        member_id="M00001",
        segment="active",
        plan_type="peak",
        age=32,
        gender="F",
        tenure_days=90,
        hrv_ms=52.0,
        resting_hr=61.0,
        sleep_hours=7.2,
        sleep_score=78.0,
        recovery_score=65.0,
        strain_score=12.5,
        steps=9200,
        hrv_7d_avg=50.0,
        hrv_30d_avg=48.0,
        hrv_trend="improving",
        recovery_7d_avg=62.0,
        recovery_trend="stable",
        features_used_count=5,
        top_features=["sleep_coach", "recovery_insights", "strain_coach"],
        total_sessions=180,
        coaching_priority_score=50,
    )


class TestPromptGeneration:
    def test_v1_includes_biometrics(self, sample_context: MemberContext) -> None:
        prompt = build_insight_prompt(sample_context, "v1")
        assert "52" in prompt  # HRV
        assert "7.2" in prompt  # sleep hours
        assert "active" in prompt  # segment

    def test_v2_includes_structure(self, sample_context: MemberContext) -> None:
        prompt = build_insight_prompt(sample_context, "v2")
        assert "OBSERVATION" in prompt
        assert "CONTEXT" in prompt
        assert "ACTION" in prompt

    def test_power_segment_gets_direct_tone(self) -> None:
        ctx = MemberContext(
            member_id="M00002", segment="power", plan_type="life",
            age=28, gender="M", tenure_days=200,
            hrv_ms=70, resting_hr=50, sleep_hours=8.0, sleep_score=90,
            recovery_score=85, strain_score=18, steps=12000,
            hrv_7d_avg=68, hrv_30d_avg=65, hrv_trend="improving",
            recovery_7d_avg=82, recovery_trend="improving",
            features_used_count=8, top_features=["strain_coach"],
            total_sessions=500, coaching_priority_score=30,
        )
        prompt = build_insight_prompt(ctx, "v1")
        assert "precision" in prompt.lower() or "data-rich" in prompt.lower()

    def test_casual_segment_gets_warm_tone(self) -> None:
        ctx = MemberContext(
            member_id="M00003", segment="casual", plan_type="one",
            age=45, gender="F", tenure_days=30,
            hrv_ms=38, resting_hr=70, sleep_hours=6.0, sleep_score=55,
            recovery_score=45, strain_score=6, steps=4000,
            hrv_7d_avg=36, hrv_30d_avg=40, hrv_trend="declining",
            recovery_7d_avg=43, recovery_trend="declining",
            features_used_count=1, top_features=[],
            total_sessions=20, coaching_priority_score=95,
        )
        prompt = build_insight_prompt(ctx, "v1")
        assert "encouraging" in prompt.lower() or "warm" in prompt.lower()

    def test_evaluation_prompt_contains_insight(self, sample_context: MemberContext) -> None:
        prompt = build_evaluation_prompt("Your HRV is trending up.", "active segment")
        assert "Your HRV is trending up." in prompt
        assert "RELEVANCE" in prompt
        assert "SAFETY" in prompt


class TestRouter:
    def test_restricted_routes_local(self) -> None:
        model = _select_model(ComplianceTier.RESTRICTED)
        assert "ollama" in model

    def test_standard_routes_local(self) -> None:
        model = _select_model(ComplianceTier.STANDARD)
        assert "ollama" in model

    def test_evaluation_routes_local(self) -> None:
        model = _select_model(ComplianceTier.EVALUATION)
        assert "ollama" in model

    def test_default_config(self) -> None:
        config = RouterConfig()
        assert config.primary_model == "ollama/llama3"
        assert config.fallback_model == "ollama/phi3"
        assert config.max_tokens == 512
