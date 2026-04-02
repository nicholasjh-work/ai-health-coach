"""Tests for synthetic data generator."""

import pandas as pd
import pytest

from src.data_gen.generate import (
    GeneratorConfig,
    _generate_daily_metrics,
    _generate_feature_events,
    _generate_members,
    _generate_sessions,
)


@pytest.fixture
def small_config() -> GeneratorConfig:
    return GeneratorConfig(n_members=50, days_of_history=30)


@pytest.fixture
def members(small_config: GeneratorConfig) -> pd.DataFrame:
    return _generate_members(small_config)


class TestMemberGeneration:
    def test_correct_count(self, members: pd.DataFrame, small_config: GeneratorConfig) -> None:
        assert len(members) == small_config.n_members

    def test_unique_ids(self, members: pd.DataFrame) -> None:
        assert members["member_id"].nunique() == len(members)

    def test_valid_segments(self, members: pd.DataFrame) -> None:
        valid = {"power", "active", "casual"}
        assert set(members["segment"].unique()).issubset(valid)

    def test_valid_plans(self, members: pd.DataFrame) -> None:
        valid = {"one", "peak", "life"}
        assert set(members["plan_type"].unique()).issubset(valid)

    def test_churn_rate_approximate(self, members: pd.DataFrame, small_config: GeneratorConfig) -> None:
        actual_rate = members["is_churned"].mean()
        assert abs(actual_rate - small_config.churn_rate) < 0.15

    def test_churned_members_have_churn_date(self, members: pd.DataFrame) -> None:
        churned = members[members["is_churned"]]
        assert churned["churn_date"].notna().all()

    def test_non_churned_have_no_churn_date(self, members: pd.DataFrame) -> None:
        active = members[~members["is_churned"]]
        assert active["churn_date"].isna().all()


class TestDailyMetrics:
    def test_generates_rows(
        self, members: pd.DataFrame, small_config: GeneratorConfig
    ) -> None:
        metrics = _generate_daily_metrics(members, small_config)
        assert len(metrics) > 0

    def test_hrv_bounds(
        self, members: pd.DataFrame, small_config: GeneratorConfig
    ) -> None:
        metrics = _generate_daily_metrics(members, small_config)
        assert metrics["hrv_ms"].min() >= 15

    def test_sleep_bounds(
        self, members: pd.DataFrame, small_config: GeneratorConfig
    ) -> None:
        metrics = _generate_daily_metrics(members, small_config)
        assert metrics["sleep_hours"].min() >= 3.0
        assert metrics["sleep_hours"].max() <= 12.0

    def test_no_future_dates(
        self, members: pd.DataFrame, small_config: GeneratorConfig
    ) -> None:
        metrics = _generate_daily_metrics(members, small_config)
        end = small_config.start_date + pd.Timedelta(days=small_config.days_of_history)
        assert (metrics["metric_date"] <= end).all()


class TestFeatureEvents:
    def test_generates_rows(
        self, members: pd.DataFrame, small_config: GeneratorConfig
    ) -> None:
        events = _generate_feature_events(members, small_config)
        assert len(events) > 0

    def test_valid_event_types(
        self, members: pd.DataFrame, small_config: GeneratorConfig
    ) -> None:
        events = _generate_feature_events(members, small_config)
        valid = {"view", "interact", "dismiss"}
        assert set(events["event_type"].unique()).issubset(valid)


class TestSessions:
    def test_generates_rows(
        self, members: pd.DataFrame, small_config: GeneratorConfig
    ) -> None:
        sessions = _generate_sessions(members, small_config)
        assert len(sessions) > 0

    def test_valid_platforms(
        self, members: pd.DataFrame, small_config: GeneratorConfig
    ) -> None:
        sessions = _generate_sessions(members, small_config)
        valid = {"ios", "android", "web"}
        assert set(sessions["platform"].unique()).issubset(valid)
