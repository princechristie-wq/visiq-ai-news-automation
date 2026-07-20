"""
============================================================
Visiq AI
Main Application
Version : 2.0.0
============================================================

Master Workflow Controller

This file coordinates the complete workflow.

Business logic belongs inside the individual engines.

Workflow

1. Discover Trending Topics
2. Research Topics
3. Generate Script
4. Generate Visual Plan
5. Generate Video
6. Upload to YouTube
"""

from pathlib import Path
import traceback

from config import (
    PROJECT_NAME,
    PROJECT_VERSION,
    OUTPUT_DIR,
)

from trend_engine import get_trending_topics

from research_engine import research_topics

from script_engine import generate_scripts

from visual_engine import generate_visual_plan

from video_engine import create_videos

from youtube_engine import upload_to_youtube


# ==========================================================
# Helper Functions
# ==========================================================

def print_banner():

    print("\n" + "=" * 80)
    print(f"{PROJECT_NAME}  v{PROJECT_VERSION}")
    print("=" * 80)
    print("Visiq AI Automation Pipeline")
    print("=" * 80)


def save_text(filename, content):

    path = OUTPUT_DIR / filename

    path.write_text(
        content,
        encoding="utf-8"
    )

    print(f"Saved : {filename}")


def verify_file(filepath):

    file = Path(filepath)

    if not file.exists():

        raise FileNotFoundError(
            f"Missing file : {filepath}"
        )

    if file.stat().st_size == 0:

        raise RuntimeError(
            f"Empty file : {filepath}"
        )

    return file


# ==========================================================
# Main Pipeline
# ==========================================================

def run_pipeline():

    print_banner()

    print("\nSTEP 1 : Discovering Trending AI Topics\n")

    topics = get_trending_topics()

    if not topics:

        raise RuntimeError(
            "No trending topics found."
        )

    print(f"Topics Found : {len(topics)}")

    print("\nSTEP 2 : Researching Topics\n")

    research = research_topics(
        topics
    )

    if not research:

        raise RuntimeError(
            "Research engine returned no data."
        )

    print("Research Complete")

    print("\nSTEP 3 : Generating Scripts\n")

    scripts = generate_scripts(
        research
    )

    if not scripts:

        raise RuntimeError(
            "Script generation failed."
        )

    print("Scripts Generated")

    print("\nSTEP 4 : Generating Visual Storyboards\n")

    visual_plan = generate_visual_plan(
        scripts
    )

    if not visual_plan:

        raise RuntimeError(
            "Visual plan generation failed."
        )

    print("Storyboard Generated")
