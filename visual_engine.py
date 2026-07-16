import requests
import random
from groq import Groq

# ============================================================
# VISUAL ENGINE CONFIGURATION
# ============================================================

TOTAL_SCENES = 10

IMAGE_WIDTH = 768

IMAGE_HEIGHT = 1344

IMAGE_MODEL = "flux"

# ============================================================
# CREATE GROQ CLIENT
# ============================================================

def create_client(api_key):

    return Groq(
        api_key=api_key
    )

# ============================================================
# SPLIT SCRIPT INTO SCENES
# ============================================================

def split_script_into_scenes(script):

    words = script.split()

    words_per_scene = max(
        len(words) // TOTAL_SCENES,
        1
    )

    scenes = []

    for i in range(TOTAL_SCENES):

        start = i * words_per_scene

        if i == TOTAL_SCENES - 1:

            end = len(words)

        else:

            end = start + words_per_scene

        scene_text = " ".join(
            words[start:end]
        )

        scenes.append(scene_text)

    return scenes

# ============================================================
# MOTION TYPES
# ============================================================

MOTION_TYPES = [

    "zoom_in",

    "zoom_out",

    "pan_left",

    "pan_right",

    "tilt_up",

    "tilt_down",

    "push_in",

    "pull_out"

]

# ============================================================
# BUILD VISUAL PROMPT
# ============================================================

def build_visual_prompt(scene_text):

    return f"""
You are an expert cinematic storyboard artist.

Narration:

{scene_text}

Generate ONE visual idea.

Rules:

- Match the narration.
- Prefer stock footage when possible.
- If stock footage is unlikely, use AI image.
- No text.
- No watermark.
- No logos.
- Cinematic.
- Photorealistic.

Return only:

VISUAL_TYPE:
SEARCH_QUERY:
IMAGE_PROMPT:
"""

# ============================================================
# GENERATE VISUAL DECISION
# ============================================================

def generate_visual_decision(scene_text, api_key):

    client = create_client(api_key)

    prompt = build_visual_prompt(scene_text)

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]

    )

    result = response.choices[0].message.content.strip()

    visual = {

        "visual_type": "image",
        "search_query": "",
        "image_prompt": ""

    }

    for line in result.splitlines():

        if line.startswith("VISUAL_TYPE:"):

            visual["visual_type"] = line.replace(
                "VISUAL_TYPE:",
                ""
            ).strip().lower()

        elif line.startswith("SEARCH_QUERY:"):

            visual["search_query"] = line.replace(
                "SEARCH_QUERY:",
                ""
            ).strip()

        elif line.startswith("IMAGE_PROMPT:"):

            visual["image_prompt"] = line.replace(
                "IMAGE_PROMPT:",
                ""
            ).strip()

    return visual

# ============================================================
# CREATE SCENE PLAN
# ============================================================

def create_scene_plan(script, api_key):

    scenes = split_script_into_scenes(
        script
    )

    plan = []

    for scene in scenes:

        visual = generate_visual_decision(
            scene,
            api_key
        )

        plan.append({

            "narration": scene,

            "visual_type": visual["visual_type"],

            "search_query": visual["search_query"],

            "image_prompt": visual["image_prompt"],

            "motion": random.choice(
                MOTION_TYPES
            )

        })

    return plan

# ============================================================
# PUBLIC FUNCTION
# ============================================================

def generate_visual_plan(knowledge_packages, api_key):

    visual_packages = []

    for knowledge in knowledge_packages:

        knowledge["scene_plan"] = create_scene_plan(
            knowledge["script"],
            api_key
        )

        visual_packages.append(
            knowledge
        )

    return visual_packages
