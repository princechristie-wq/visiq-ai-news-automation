"""
============================================================
Visiq AI
Central Configuration
Version : 1.0.0
============================================================
"""

import os
from pathlib import Path

# ----------------------------------------------------------
# Project Information
# ----------------------------------------------------------

PROJECT_NAME = "Visiq AI"

PROJECT_VERSION = "1.0.0"

# ----------------------------------------------------------
# AI Provider Configuration
# ----------------------------------------------------------

# Supported:
# groq
# openrouter
# gemini
# openai

AI_PROVIDER = "groq"

PRIMARY_MODEL = "llama-3.3-70b-versatile"

# ----------------------------------------------------------
# API Keys
# ----------------------------------------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")

YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")

YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN")

# ----------------------------------------------------------
# Project Directories
# ----------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "output"

CACHE_DIR = BASE_DIR / "cache"

TEMP_DIR = BASE_DIR / "temp"

VOICE_DIR = OUTPUT_DIR / "voice"

IMAGE_DIR = OUTPUT_DIR / "images"

VIDEO_DIR = OUTPUT_DIR / "videos"

# ----------------------------------------------------------
# Automatically create folders
# ----------------------------------------------------------

for folder in [
    OUTPUT_DIR,
    CACHE_DIR,
    TEMP_DIR,
    VOICE_DIR,
    IMAGE_DIR,
    VIDEO_DIR,
]:
    folder.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------
# Video Settings
# ----------------------------------------------------------

VIDEO_WIDTH = 1920

VIDEO_HEIGHT = 1080

VIDEO_FPS = 30

# ----------------------------------------------------------
# Voice Settings
# ----------------------------------------------------------

VOICE_LANGUAGE = "en-US"

VOICE_NAME = "en-US-ChristopherNeural"

# ----------------------------------------------------------
# Image Settings
# ----------------------------------------------------------

IMAGE_WIDTH = 1920

IMAGE_HEIGHT = 1080

# ----------------------------------------------------------
# YouTube Settings
# ----------------------------------------------------------

YOUTUBE_CATEGORY = "28"

YOUTUBE_PRIVACY = "public"

# ----------------------------------------------------------
# Validation
# ----------------------------------------------------------

def validate_provider():

    providers = [
        "groq",
        "openrouter",
        "gemini",
        "openai",
    ]

    if AI_PROVIDER not in providers:
        raise ValueError(
            f"Unsupported AI Provider: {AI_PROVIDER}"
        )

def get_current_api_key():

    if AI_PROVIDER == "groq":
        key = GROQ_API_KEY

    elif AI_PROVIDER == "openrouter":
        key = OPENROUTER_API_KEY

    elif AI_PROVIDER == "gemini":
        key = GEMINI_API_KEY

    elif AI_PROVIDER == "openai":
        key = OPENAI_API_KEY

    else:
        key = None

    if not key:
        raise ValueError(
            f"Missing API key for provider: {AI_PROVIDER}"
        )

    return key
    
# ----------------------------------------------------------
# Startup Validation
# ----------------------------------------------------------

validate_provider()
