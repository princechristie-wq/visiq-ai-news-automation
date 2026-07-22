import json

from ai_provider import generate_text

# ============================================================
# VISUAL ENGINE CONFIGURATION
# ============================================================

DEFAULT_IMAGE_PROVIDER = "flux"

SUPPORTED_IMAGE_PROVIDERS = [

    "flux",

    "stable_diffusion",

    "imagen",

    "dalle"

]

# ============================================================
# BUILD VISUAL PROMPT
# ============================================================

def build_visual_prompt(scene):
    """
    Build the prompt that decides which visual
    should represent the Director Engine scene.
    """

    return f"""
You are an expert cinematic storyboard artist for YouTube Shorts.

Scene Number:
{scene["scene_number"]}

Narration:
{scene["narration"]}

Camera:
{scene["camera"]}

Lighting:
{scene["lighting"]}

Emotion:
{scene["emotion"]}

Base Image Prompt:
{scene["image_prompt"]}

Negative Prompt:
{scene["negative_prompt"]}

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

Return ONLY valid JSON.

Do not use markdown.

Do not explain anything.

Return exactly this structure:

{
    "visual_type": "image",
    "search_query": "robot laboratory",
    "image_prompt": "A cinematic photorealistic robot inside a futuristic laboratory."
}

# ============================================================
# GENERATE VISUAL DECISION
# ============================================================

def generate_visual_decision(scene):
    """
    Generate a visual decision for a single
    Director Engine scene.
    """

    prompt = build_visual_prompt(scene)

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

            "image_prompt": scene.get(
                "image_prompt",
                "A cinematic, photorealistic illustration."
            )

        }

    try:

        visual = json.loads(result)

    except json.JSONDecodeError:

        raise RuntimeError(
            "Visual Engine returned invalid JSON."
        )
    # --------------------------------------------------------
    # Normalize Missing Fields
    # --------------------------------------------------------

    visual.setdefault(
        "visual_type",
        "image"
    )

    visual.setdefault(
        "search_query",
        ""
    )

    visual.setdefault(
        "image_prompt",
        scene.get(
            "image_prompt",
            "A cinematic, photorealistic illustration."
        )
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

        visual["image_prompt"] = scene.get(
            "image_prompt",
            "A cinematic, photorealistic illustration."
        )

    return visual


# ============================================================
# ENHANCE SCENE PLAN
# ============================================================

def enhance_scene_plan(cinematic_blueprint):
    """
    Enhance every Director Engine scene with
    visual generation information.
    """

    plan = []

    scenes = cinematic_blueprint.get(
        "scenes",
        []
    )

    total_scenes = len(scenes)

    print(
        f"Generating storyboard ({total_scenes} scenes)..."
    )

    for scene_number, scene in enumerate(
        scenes,
        start=1
    ):

        print(
            f"  Scene {scene_number}/{total_scenes}"
        )

        visual = generate_visual_decision(scene)

        enhanced_scene = scene.copy()

        enhanced_scene.update({

            "visual_type": visual["visual_type"],

            "search_query": visual["search_query"],

            "enhanced_image_prompt": visual["image_prompt"]

        })

        plan.append(
            enhanced_scene
        )

    return plan


# ============================================================
# PUBLIC FUNCTION
# ============================================================

def create_visual_blueprint(cinematic_blueprint):
    """
    Enhance a Director Engine cinematic blueprint
    with optimized visual generation information.

    Args:
        cinematic_blueprint (dict): Blueprint generated
            by the Director Engine.

    Returns:
        dict: Enhanced cinematic blueprint.
    """

    try:

        enhanced_scene_plan = enhance_scene_plan(
            cinematic_blueprint
        )

        enhanced_blueprint = cinematic_blueprint.copy()

        enhanced_blueprint["scenes"] = (
            enhanced_scene_plan
        )

        return enhanced_blueprint

    except Exception as e:

        print(
            f"Visual blueprint generation failed: {e}"
        )

        cinematic_blueprint["scenes"] = []

        cinematic_blueprint["visual_error"] = str(e)

        return cinematic_blueprint
