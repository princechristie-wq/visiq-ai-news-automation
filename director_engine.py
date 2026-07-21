import json
import re

from ai_provider import generate_text

# ============================================================
# DIRECTOR ENGINE CONFIGURATION
# ============================================================

DEFAULT_SCENE_DURATION = 2.5

MIN_SCENES = 8

MAX_SCENES = 15

MAX_RETRY = 3

DIRECTOR_TEMPERATURE = 0.7

DIRECTOR_MAX_TOKENS = 4096

CAMERAS = [

    "static",

    "dolly_in",

    "dolly_out",

    "pan_left",

    "pan_right",

    "tilt_up",

    "tilt_down",

    "orbit",

    "zoom_in",

    "zoom_out",

    "handheld"

]

TRANSITIONS = [

    "cut",

    "fade",

    "flash",

    "glitch",

    "zoom",

    "blur",

    "whip_pan",

    "light_leak",

    "digital_wipe"

]

MOTIONS = [

    "static",

    "slow",

    "medium",

    "fast",

    "cinematic",

    "dynamic"

]

LIGHTING = [

    "natural",

    "studio",

    "soft",

    "dramatic",

    "blue_neon",

    "cyberpunk",

    "golden",

    "dark",

    "high_contrast"

]

EMOTIONS = [

    "neutral",

    "curious",

    "exciting",

    "dramatic",

    "urgent",

    "inspiring",

    "mysterious",

    "futuristic"

]

COLOR_THEMES = [

    "blue",

    "red",

    "orange",

    "purple",

    "green",

    "cyber_blue",

    "cinematic_teal",

    "warm",

    "dark"

]

VISUAL_STYLES = [

    "photorealistic",

    "cinematic",

    "technology",

    "3d_render",

    "documentary",

    "news",

    "minimal",

    "futuristic"

]

SOUND_EFFECTS = [

    "none",

    "whoosh",

    "click",

    "typing",

    "notification",

    "digital",

    "impact",

    "transition"

]

OVERLAYS = [

    "none",

    "hud",

    "particles",

    "grid",

    "arrows",

    "highlight",

    "glow",

    "tech_lines"

]

# ============================================================
# DIRECTOR PLAN SCHEMA
# ============================================================

REQUIRED_SCENE_FIELDS = [

    "scene_number",

    "narration",

    "duration",

    "camera",

    "transition",

    "visual_style",

    "subject",

    "background",

    "lighting",

    "color_theme",

    "motion",

    "effects",

    "overlay",

    "text_overlay",

    "sound_effect",

    "emotion",

    "image_prompt",

    "negative_prompt"

]

REQUIRED_PLAN_FIELDS = [

    "title",

    "hook",

    "total_duration",

    "thumbnail_prompt",

    "scenes"

]

# ============================================================
# CINEMATIC BLUEPRINT TEMPLATE
# ============================================================

BLUEPRINT_VERSION = "1.0"

BLUEPRINT_TEMPLATE = {

    "title": "",

    "hook": "",

    "total_duration": 0,

    "thumbnail_prompt": "",

    "scenes": [

        {

            "scene_number": 1,

            "narration": "",

            "duration": 2.5,

            "camera": "",

            "transition": "",

            "visual_style": "",

            "subject": "",

            "background": "",

            "lighting": "",

            "color_theme": "",

            "motion": "",

            "effects": [],

            "overlay": "",

            "text_overlay": "",

            "sound_effect": "",

            "emotion": "",

            "image_prompt": "",

            "negative_prompt": ""

        }

    ]

}

SUPPORTED_OUTPUT_PROFILES = [

    "youtube_shorts",

    "youtube_long",

    "instagram_reels",

    "facebook_reels",

    "tiktok"

]

DEFAULT_OUTPUT_PROFILE = "youtube_shorts"

# ============================================================
# DIRECTOR ENGINE FUNCTIONS
# ============================================================

DIRECTOR_SYSTEM_ROLE = """
You are an award-winning AI Film Director and Storyboard Artist.

Your responsibility is to transform a completed narration into a cinematic
scene-by-scene production blueprint.

Your output must be visually engaging, technically consistent,
and optimized for short-form videos.

Never explain your reasoning.

Never add markdown.

Return JSON only.
"""

DIRECTOR_RULES = """
Rules:

• Every scene must match the narration.

• Every scene should introduce a new visual.

• Avoid repetitive imagery.

• Camera movement should enhance storytelling.

• Keep pacing fast.

• Scenes should flow naturally.

• Image prompts must be highly descriptive.

• Negative prompts should remove unwanted artifacts.

• Use only approved camera values.

• Use only approved transitions.

• Use only approved lighting.

• Use only approved emotions.

"""

JSON_RULES = """
Return ONLY valid JSON.

Do not wrap JSON inside markdown.

Do not explain anything.

Do not include comments.

The JSON must follow the Cinematic Blueprint template exactly.
"""

def build_director_prompt(
    topic,
    research,
    script,
    output_profile=DEFAULT_OUTPUT_PROFILE
):
    """
    Build the AI prompt that instructs the model to generate
    a Cinematic Blueprint.
    """
    prompt = f"""
{DIRECTOR_SYSTEM_ROLE}

{DIRECTOR_RULES}

{JSON_RULES}

Output Profile:
{output_profile}

Topic:
{topic}

Research:
{research}

Narration:
{script}

Return a complete Cinematic Blueprint.
"""

    return prompt


def call_ai_director(prompt):
    """
    Send the prompt to the configured AI provider
    and return the raw AI response.
    """

    response = generate_text(
        prompt=prompt,
        temperature=DIRECTOR_TEMPERATURE,
        max_tokens=DIRECTOR_MAX_TOKENS,
    )

    return response


def normalize_cinematic_blueprint(raw_response):
    """
    Convert the raw AI response into a Python dictionary.
    """

    # Remove markdown code fences if present
    cleaned = re.sub(
        r"^```(?:json)?|```$",
        "",
        raw_response.strip(),
        flags=re.MULTILINE,
    ).strip()

    try:
        blueprint = json.loads(cleaned)

    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Invalid JSON returned by AI: {e}"
        ) from e

    return blueprint


def validate_cinematic_blueprint(blueprint):
    """
    Validate the Cinematic Blueprint structure.
    """

    # Validate top-level fields
    for field in REQUIRED_PLAN_FIELDS:

        if field not in blueprint:

            raise RuntimeError(
                f"Missing required blueprint field: {field}"
            )

    # Validate scenes
    scenes = blueprint.get("scenes")

    if not isinstance(scenes, list):

        raise RuntimeError(
            "'scenes' must be a list."
        )

    if len(scenes) == 0:

        raise RuntimeError(
            "Blueprint contains no scenes."
        )

    # Validate every scene
    for index, scene in enumerate(scenes, start=1):

        for field in REQUIRED_SCENE_FIELDS:

            if field not in scene:

                raise RuntimeError(
                    f"Scene {index} is missing required field: {field}"
                )

    return True


def create_cinematic_blueprint(
    topic,
    research,
    script,
    output_profile=DEFAULT_OUTPUT_PROFILE,
):
    """
    Generate a validated Cinematic Blueprint.
    """

    # Step 1 - Build prompt
    prompt = build_director_prompt(
        topic=topic,
        research=research,
        script=script,
        output_profile=output_profile,
    )

    # Step 2 - Generate AI response
    raw_response = call_ai_director(prompt)

    # Step 3 - Convert JSON to dictionary
    blueprint = normalize_cinematic_blueprint(raw_response)

    # Step 4 - Validate blueprint
    validate_cinematic_blueprint(blueprint)

    # Step 5 - Return final blueprint
    return blueprint
