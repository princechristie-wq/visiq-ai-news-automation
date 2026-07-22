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

SUPPORTED_VISUAL_TYPES = [
    "image",
    "stock"
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
    "image_prompt": "A cinematic photorealistic robot inside a futuristic laboratory.",
    "negative_prompt": "blurry, watermark, logo, text, low quality, deformed anatomy",
    "visual_keywords": [
        "robot",
        "AI",
        "laboratory",
        "future"
    ],
    "generation_model": "flux"
}
"""

# ============================================================
# GENERATE VISUAL DECISION
# ============================================================

def _call_visual_ai(prompt):
    """
    Sends the visual prompt to the AI provider.
    Returns the raw AI response.
    """

    return generate_text(
        prompt,
        temperature=VISUAL_TEMPERATURE,
        max_tokens=VISUAL_MAX_TOKENS
    )

def generate_visual_decision(scene):
    """
    Generate a visual decision for a single
    Director Engine scene.
    """

    prompt = build_visual_prompt(scene)

    try:

        result = _call_visual_ai(
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
    
    visual.setdefault(
        "negative_prompt",
        ""
    )

    visual.setdefault(
        "visual_keywords",
        []
    )

    visual.setdefault(
        "generation_model",
        DEFAULT_IMAGE_PROVIDER
    )
        
    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    if visual["visual_type"] not in SUPPORTED_VISUAL_TYPES:
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

            "enhanced_image_prompt": visual["image_prompt"],

            "negative_prompt": visual["negative_prompt"],

            "visual_keywords": visual["visual_keywords"],

            "generation_model": visual["generation_model"]

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
