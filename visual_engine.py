import os
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

def get_api_key():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:

        raise ValueError(
            "GROQ_API_KEY not found."
        )

    return api_key

def create_client(api_key):

    return Groq(
        api_key=get_api_key()
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
You are an expert cinematic storyboard artist for YouTube Shorts.

Narration:

{scene_text}

Your task is to decide the best visual for this narration.

Rules:

- If real-world footage can represent the narration, choose "stock".
- If the narration describes concepts, futuristic technology, AI, imaginary scenes, or anything difficult to film, choose "image".
- The visual must directly match the narration.
- Search queries should contain only the essential keywords.
- Image prompts must be cinematic, photorealistic, detailed, and contain no text, logos, or watermarks.

Return ONLY in exactly this format:

VISUAL_TYPE: stock OR image
SEARCH_QUERY: ...
IMAGE_PROMPT: ...

Do not return any explanation.
Do not add headings.
Do not add markdown.
Do not add extra text.
"""
# ============================================================
# GENERATE VISUAL DECISION
# ============================================================

def generate_visual_decision(scene_text):

    client = create_client()

    prompt = build_visual_prompt(
        scene_text
    )

    try:

        response = client.chat.completions.create(

            model=LLM_MODEL,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        )

        result = response.choices[0].message.content.strip()

    except Exception as e:

        print("Failed to generate visual for scene.")

        print(e)

        return {

            "visual_type": "image",

            "search_query": "",

            "image_prompt": "A cinematic photorealistic illustration matching the narration."

        }

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

    if visual["visual_type"] not in ["stock", "image"]:

        visual["visual_type"] = "image"

    return visual
# ============================================================
# CREATE SCENE PLAN
# ============================================================

def create_scene_plan(script):

    scenes = split_script_into_scenes(
        script
    )

    plan = []

    previous_motion = None

    for scene_number, scene in enumerate(scenes, start=1):

        visual = generate_visual_decision(
            scene
        )

        available_motions = [

            motion

            for motion in MOTION_TYPES

            if motion != previous_motion

        ]

        selected_motion = random.choice(
            available_motions
        )

        previous_motion = selected_motion

        plan.append({

            "scene_number": scene_number,

            "narration": scene,

            "visual_type": visual["visual_type"],

            "search_query": visual["search_query"],

            "image_prompt": visual["image_prompt"],

            "motion": selected_motion

        })

    return plan

# ============================================================
# PUBLIC FUNCTION
# ============================================================

def generate_visual_plan(knowledge_packages):

    visual_packages = []

    for knowledge in knowledge_packages:

        knowledge["scene_plan"] = create_scene_plan(
            knowledge["script"]
        )

        visual_packages.append(
            knowledge
        )

    return visual_packages
