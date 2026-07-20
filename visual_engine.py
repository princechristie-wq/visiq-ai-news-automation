import random

from ai_provider import generate_text
from config import PRIMARY_MODEL

# ============================================================
# VISUAL ENGINE CONFIGURATION
# ============================================================

TOTAL_SCENES = 10

IMAGE_WIDTH = 768

IMAGE_HEIGHT = 1344

IMAGE_MODEL = "flux"

# ============================================================
# SPLIT SCRIPT INTO SCENES
# ============================================================

def split_script_into_scenes(script):
    """
    Divide the narration into evenly sized scenes.
    """

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
    """
    Build the prompt that decides which visual
    should represent the narration.
    """

    return f"""
You are an expert cinematic storyboard artist for YouTube Shorts.

Narration:

{scene_text}

Decide the single best visual.

Rules:

- Use STOCK when real footage exists.
- Use IMAGE for AI concepts, futuristic technology,
  impossible scenes or abstract ideas.
- The visual must directly match the narration.
- Search queries should contain only the essential keywords.
- Image prompts must be cinematic.
- Photorealistic.
- Ultra detailed.
- No text.
- No watermark.
- No logo.

Return EXACTLY:

VISUAL_TYPE: stock OR image
SEARCH_QUERY: ...
IMAGE_PROMPT: ...

Return nothing else.
"""

# ============================================================
# GENERATE VISUAL DECISION
# ============================================================

def generate_visual_decision(scene_text):
    """
    Generate a visual decision for a single scene using
    the configured AI provider.
    """

    prompt = build_visual_prompt(
        scene_text
    )

    try:

        result = generate_text(
            prompt
        ).strip()

    except Exception as e:

        print(
            f"Failed to generate visual for scene: {e}"
        )

        return {

            "visual_type": "image",

            "search_query": "",

            "image_prompt": (
                "A cinematic, photorealistic illustration "
                "matching the narration."
            )

        }

    visual = {

        "visual_type": "image",

        "search_query": "",

        "image_prompt": ""

    }

    for line in result.splitlines():

        line = line.strip()

        if line.startswith("VISUAL_TYPE:"):

            visual["visual_type"] = (
                line.replace(
                    "VISUAL_TYPE:",
                    ""
                )
                .strip()
                .lower()
            )

        elif line.startswith("SEARCH_QUERY:"):

            visual["search_query"] = (
                line.replace(
                    "SEARCH_QUERY:",
                    ""
                )
                .strip()
            )

        elif line.startswith("IMAGE_PROMPT:"):

            visual["image_prompt"] = (
                line.replace(
                    "IMAGE_PROMPT:",
                    ""
                )
                .strip()
            )

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    if visual["visual_type"] not in (
        "stock",
        "image"
    ):

        visual["visual_type"] = "image"

    if (
        visual["visual_type"] == "image"
        and not visual["image_prompt"]
    ):

        visual["image_prompt"] = (
            "A cinematic, photorealistic illustration "
            "matching the narration."
        )

    return visual

# ============================================================
# CREATE SCENE PLAN
# ============================================================

def create_scene_plan(script):
    """
    Create a complete scene-by-scene storyboard for the script.
    """

    scenes = split_script_into_scenes(script)

    plan = []

    previous_motion = None

    total_scenes = len(scenes)

    print(f"Generating storyboard ({total_scenes} scenes)...")

    for scene_number, scene in enumerate(scenes, start=1):

        print(f"  Scene {scene_number}/{total_scenes}")

        visual = generate_visual_decision(scene)

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
    """
    Generate visual storyboards for all scripts.

    Returns:
        list[dict]: Knowledge packages with scene plans.
    """

    visual_packages = []

    total = len(knowledge_packages)

    print("=" * 80)
    print("GENERATING VISUAL PLANS...")
    print("=" * 80)

    for index, knowledge in enumerate(
        knowledge_packages,
        start=1
    ):

        print(f"[{index}/{total}] {knowledge['title']}")

        try:

            script = knowledge.get(
                "script",
                ""
            )

            if not script.strip():

                raise ValueError(
                    "Script is empty."
                )

            knowledge["scene_plan"] = create_scene_plan(
                script
            )

        except Exception as e:

            print(
                f"Visual plan generation failed: {e}"
            )

            knowledge["scene_plan"] = []

            knowledge["visual_error"] = str(e)

        visual_packages.append(
            knowledge
        )

    print("=" * 80)
    print(
        f"Successfully generated {len(visual_packages)} visual plan(s)"
    )
    print("=" * 80)

    return visual_packages
