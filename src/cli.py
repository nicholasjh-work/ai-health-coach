"""
CLI for ai-health-coach.

Commands:
  coach generate   -- Load synthetic data into PostgreSQL
  coach dbt        -- Run dbt transformations
  coach insights   -- Generate AI coaching insights for top-priority members
  coach evaluate   -- Show evaluation summary
"""

import asyncio
import logging
import os
import subprocess
import sys

import typer
from dotenv import load_dotenv

load_dotenv()

app = typer.Typer(
    name="coach",
    help="AI Health Coach: personalized coaching insights from wearable biometric data.",
    no_args_is_help=True,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("coach")


def _pg_url() -> str:
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "ai_health_coach")
    user = os.getenv("POSTGRES_USER", "nickhidalgo")
    pw = os.getenv("POSTGRES_PASSWORD", "")
    if pw:
        return f"postgresql://{user}:{pw}@{host}:{port}/{db}"
    return f"postgresql://{user}@{host}:{port}/{db}"


@app.command()
def generate(
    members: int = typer.Option(2000, help="Number of members to generate"),
    days: int = typer.Option(180, help="Days of history"),
) -> None:
    """Load synthetic wearable health data into PostgreSQL."""
    from src.data_gen.generate import GeneratorConfig, load_to_postgres

    config = GeneratorConfig(n_members=members, days_of_history=days)
    logger.info(f"Generating data: {members} members, {days} days of history")

    counts = load_to_postgres(config, _pg_url())
    for table, count in counts.items():
        typer.echo(f"  {table}: {count:,} rows")
    typer.echo("Done.")


@app.command()
def dbt(
    full_refresh: bool = typer.Option(False, help="Run with --full-refresh"),
) -> None:
    """Run dbt transformations."""
    dbt_bin = "/opt/anaconda3/bin/dbt"
    project_dir = os.path.join(os.path.dirname(__file__), "dbt_project")

    if not os.path.exists(dbt_bin):
        dbt_bin = "dbt"

    cmd = [dbt_bin, "run", "--project-dir", project_dir]
    if full_refresh:
        cmd.append("--full-refresh")

    logger.info(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False)
    sys.exit(result.returncode)


@app.command()
def insights(
    n: int = typer.Option(20, help="Number of members to coach"),
    version: str = typer.Option("v1", help="Prompt version (v1 or v2)"),
) -> None:
    """Generate AI coaching insights for top-priority members."""
    from src.llm.coach import run_coaching_batch

    logger.info(f"Generating insights for top {n} members (prompt {version})")
    results = asyncio.run(run_coaching_batch(_pg_url(), n_members=n, prompt_version=version))

    for r in results:
        composite = (
            r["relevance_score"] + r["specificity_score"]
            + r["actionability_score"] + r["safety_score"]
        ) / 4
        typer.echo(f"\n--- {r['member_id']} (composite: {composite:.0f}/100) ---")
        typer.echo(r["insight_text"])

    typer.echo(f"\nGenerated {len(results)} insights. Stored in raw.ai_evaluations.")


@app.command()
def evaluate() -> None:
    """Show evaluation summary from stored results."""
    import pandas as pd
    from sqlalchemy import create_engine, text

    engine = create_engine(_pg_url())
    try:
        with engine.connect() as conn:
            df = pd.read_sql(text("SELECT * FROM raw.ai_evaluations"), conn)
    except Exception:
        typer.echo("No evaluations found. Run 'coach insights' first.")
        raise typer.Exit(1)

    if df.empty:
        typer.echo("No evaluations found.")
        raise typer.Exit(0)

    score_cols = ["relevance_score", "specificity_score", "actionability_score", "safety_score"]
    typer.echo(f"\nEvaluations: {len(df)}")
    typer.echo(f"Models used: {df['model_name'].unique().tolist()}")
    typer.echo(f"\nAverage scores:")
    for col in score_cols:
        typer.echo(f"  {col.replace('_score',''):>15}: {df[col].mean():.1f}/100")

    composite = df[score_cols].mean(axis=1)
    typer.echo(f"  {'composite':>15}: {composite.mean():.1f}/100")
    typer.echo(f"\nBy prompt version:")
    typer.echo(df.groupby("prompt_version")[score_cols].mean().round(1).to_string())


if __name__ == "__main__":
    app()
