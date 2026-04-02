"""
Synthetic wearable health data generator.

Produces member profiles, daily biometric readings, feature engagement events,
and session logs. All data is deterministic (seeded) for reproducibility.

Output: PostgreSQL tables in the raw schema.
Scale: 2K members, ~200K daily metrics, ~30K feature events, ~20K sessions.
"""

import logging
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any

import numpy as np
import pandas as pd
from faker import Faker
from sqlalchemy import create_engine, text

logger = logging.getLogger(__name__)

fake = Faker()
Faker.seed(42)
np.random.seed(42)


@dataclass
class GeneratorConfig:
    """Controls data volume and characteristics."""

    n_members: int = 2000
    days_of_history: int = 180
    churn_rate: float = 0.12
    ab_test_allocation: float = 0.50
    start_date: date = date(2025, 7, 1)


PLAN_TYPES = ["one", "peak", "life"]
PLAN_WEIGHTS = [0.35, 0.40, 0.25]
ACQ_CHANNELS = ["organic", "paid_social", "referral", "retail", "affiliate"]
ACQ_WEIGHTS = [0.30, 0.25, 0.20, 0.15, 0.10]
SEGMENTS = ["power", "active", "casual"]
FEATURES = [
    "sleep_coach", "strain_coach", "recovery_insights", "hrv_trends",
    "health_monitor", "hormonal_insights", "healthspan", "journal",
    "activity_goals", "sleep_consistency",
]


def _generate_members(config: GeneratorConfig) -> pd.DataFrame:
    """Generate member profiles with plan, channel, segment, and churn flag."""
    members = []
    for i in range(config.n_members):
        signup = config.start_date + timedelta(days=np.random.randint(0, config.days_of_history))
        is_churned = np.random.random() < config.churn_rate
        churn_day = (
            signup + timedelta(days=np.random.randint(14, 90)) if is_churned else None
        )
        segment = np.random.choice(SEGMENTS, p=[0.15, 0.50, 0.35])

        members.append({
            "member_id": f"M{i+1:05d}",
            "signup_date": signup,
            "plan_type": np.random.choice(PLAN_TYPES, p=PLAN_WEIGHTS),
            "acquisition_channel": np.random.choice(ACQ_CHANNELS, p=ACQ_WEIGHTS),
            "segment": segment,
            "age": np.random.randint(18, 65),
            "gender": np.random.choice(["M", "F", "NB"], p=[0.48, 0.48, 0.04]),
            "is_churned": is_churned,
            "churn_date": churn_day,
            "ab_test_group": np.random.choice(
                ["control", "treatment"],
                p=[1 - config.ab_test_allocation, config.ab_test_allocation],
            ),
        })
    return pd.DataFrame(members)


def _generate_daily_metrics(
    members: pd.DataFrame, config: GeneratorConfig
) -> pd.DataFrame:
    """Generate daily biometric readings per active member per day."""
    rows: list[dict[str, Any]] = []
    end_date = config.start_date + timedelta(days=config.days_of_history)

    segment_profiles = {
        "power": {"hrv_base": 65, "rhr_base": 52, "sleep_base": 7.5, "strain_base": 16},
        "active": {"hrv_base": 50, "rhr_base": 60, "sleep_base": 7.0, "strain_base": 12},
        "casual": {"hrv_base": 40, "rhr_base": 68, "sleep_base": 6.5, "strain_base": 8},
    }

    for _, m in members.iterrows():
        profile = segment_profiles[m["segment"]]
        active_end = m["churn_date"] if m["is_churned"] else end_date
        current = m["signup_date"]

        while current < active_end:
            day_noise = np.random.normal(0, 1)
            weekend = current.weekday() >= 5
            recovery_boost = 5 if weekend else 0

            rows.append({
                "member_id": m["member_id"],
                "metric_date": current,
                "hrv_ms": max(15, profile["hrv_base"] + day_noise * 8 + recovery_boost),
                "resting_hr_bpm": max(40, profile["rhr_base"] + day_noise * 3),
                "sleep_hours": max(3.0, min(12.0, profile["sleep_base"] + day_noise * 0.8)),
                "sleep_score": max(20, min(100, 70 + day_noise * 10 + recovery_boost)),
                "recovery_score": max(10, min(100, 65 + day_noise * 12 + recovery_boost)),
                "strain_score": max(0, min(21, profile["strain_base"] + day_noise * 2.5)),
                "respiratory_rate": max(10, min(25, 15.5 + day_noise * 1.2)),
                "skin_temp_delta_c": round(day_noise * 0.3, 2),
                "spo2_pct": max(92, min(100, 97.5 + day_noise * 0.8)),
                "steps": max(500, int(8000 + day_noise * 2000 + (3000 if not weekend else -1000))),
            })
            current += timedelta(days=1)

    return pd.DataFrame(rows)


def _generate_feature_events(
    members: pd.DataFrame, config: GeneratorConfig
) -> pd.DataFrame:
    """Generate feature engagement events: which features members use and when."""
    rows: list[dict[str, Any]] = []
    end_date = config.start_date + timedelta(days=config.days_of_history)

    feature_affinity = {
        "power": 0.7,
        "active": 0.4,
        "casual": 0.15,
    }

    for _, m in members.iterrows():
        affinity = feature_affinity[m["segment"]]
        active_end = m["churn_date"] if m["is_churned"] else end_date
        current = m["signup_date"]

        while current < active_end:
            for feature in FEATURES:
                if np.random.random() < affinity:
                    rows.append({
                        "member_id": m["member_id"],
                        "event_date": current,
                        "feature_name": feature,
                        "event_type": np.random.choice(
                            ["view", "interact", "dismiss"], p=[0.5, 0.4, 0.1]
                        ),
                        "duration_seconds": max(1, int(np.random.exponential(45))),
                    })
            current += timedelta(days=int(np.random.choice([1, 2, 3])))

    return pd.DataFrame(rows)


def _generate_sessions(
    members: pd.DataFrame, config: GeneratorConfig
) -> pd.DataFrame:
    """Generate app session logs."""
    rows: list[dict[str, Any]] = []
    end_date = config.start_date + timedelta(days=config.days_of_history)

    sessions_per_day = {"power": 8, "active": 4, "casual": 1.5}

    for _, m in members.iterrows():
        avg_sessions = sessions_per_day[m["segment"]]
        active_end = m["churn_date"] if m["is_churned"] else end_date
        current = m["signup_date"]

        while current < active_end:
            # Skip days based on segment (casual users skip more)
            skip_prob = {"power": 0.05, "active": 0.25, "casual": 0.55}
            if np.random.random() < skip_prob.get(m["segment"], 0.25):
                current += timedelta(days=1)
                continue
            n_sessions = max(0, int(np.random.poisson(avg_sessions)))
            for _ in range(n_sessions):
                hour = np.random.choice(range(6, 23), p=_hour_weights())
                rows.append({
                    "member_id": m["member_id"],
                    "session_date": current,
                    "session_start": datetime.combine(
                        current, datetime.min.time()
                    ).replace(hour=hour, minute=np.random.randint(0, 60)),
                    "duration_seconds": max(5, int(np.random.exponential(120))),
                    "platform": np.random.choice(
                        ["ios", "android", "web"], p=[0.55, 0.38, 0.07]
                    ),
                })
            current += timedelta(days=1)

    return pd.DataFrame(rows)


def _hour_weights() -> list[float]:
    """Realistic hour-of-day distribution for app opens (6am-10pm)."""
    raw = [3, 8, 5, 3, 2, 2, 4, 3, 2, 2, 3, 5, 8, 6, 4, 3, 5]
    total = sum(raw)
    return [x / total for x in raw]


def load_to_postgres(config: GeneratorConfig, connection_string: str) -> dict[str, int]:
    """Generate all data and load into PostgreSQL raw schema."""
    engine = create_engine(connection_string)

    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))

    logger.info("Generating members...")
    members = _generate_members(config)

    logger.info("Generating daily metrics...")
    metrics = _generate_daily_metrics(members, config)

    logger.info("Generating feature events...")
    events = _generate_feature_events(members, config)

    logger.info("Generating sessions...")
    sessions = _generate_sessions(members, config)

    counts = {}
    for name, df in [
        ("raw.members", members),
        ("raw.daily_metrics", metrics),
        ("raw.feature_events", events),
        ("raw.sessions", sessions),
    ]:
        df.to_sql(
            name.split(".")[1],
            engine,
            schema="raw",
            if_exists="replace",
            index=False,
        )
        counts[name] = len(df)
        logger.info(f"Loaded {len(df):,} rows into {name}")

    return counts


if __name__ == "__main__":
    import os
    logging.basicConfig(level=logging.INFO)
    pg_url = os.getenv(
        "DATABASE_URL",
        "postgresql://nickhidalgo@localhost:5432/ai_health_coach",
    )
    config = GeneratorConfig()
    result = load_to_postgres(config, pg_url)
    for table, count in result.items():
        print(f"  {table}: {count:,} rows")
