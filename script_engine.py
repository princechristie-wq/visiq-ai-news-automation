from ai_provider import generate_text
from config import PRIMARY_MODEL

# ============================================================
# SCRIPT ENGINE CONFIGURATION
# ============================================================

TARGET_WORDS = 200

VOICE_STYLE = "Energetic"

CHANNEL_NAME = "Visiq AI"

# ============================================================
# BUILD SCRIPT PROMPT
# ============================================================

def build_script_prompt(knowledge):
    """
    Build the prompt that will be sent to the configured
    AI provider.
    """

    return f"""
You are a professional YouTube Shorts script writer.

Channel Name:
{CHANNEL_NAME}

Target Audience:
People interested in Artificial Intelligence, Automation,
Technology and Future Innovations.

Topic:
{knowledge['title']}

Source Description:
{knowledge['description']}

Instructions:

Write a completely original YouTube Shorts narration.

Requirements:

• Around {TARGET_WORDS} words.
• Start with an extremely strong hook.
• Sound natural and conversational.
• Explain the technology simply.
• Only use factual information from the source.
• Never invent facts.
• Never speculate.
• Never mention that you are an AI.
• Keep the pacing fast.
• Make every sentence valuable.
• Finish with:

"Subscribe to Visiq AI for daily AI updates."

Return ONLY the narration.

Do not include:
- Titles
- Bullet points
- Stage directions
- Markdown
- Explanations
"""

# ============================================================
# GENERATE SCRIPT
# ============================================================

def generate_script(knowledge):
    """
    Generate a YouTube Shorts script using the configured
    AI provider.
    """

    prompt = build_script_prompt(knowledge)

    script = generate_text(prompt).strip()

    knowledge["script"] = script

    return knowledge


# ============================================================
# PUBLIC FUNCTION
# ============================================================

def generate_scripts(knowledge_packages):
    """
    Generate scripts for all researched topics.

    Returns:
        list[dict]: Knowledge packages with generated scripts.
    """

    scripts = []

    total = len(knowledge_packages)

    print("=" * 80)
    print("GENERATING SCRIPTS...")
    print("=" * 80)

    for index, knowledge in enumerate(knowledge_packages, start=1):

        print(f"[{index}/{total}] {knowledge['title']}")

        try:

            script = generate_script(
                knowledge
            )

            scripts.append(script)

        except Exception as e:

            print(
                f"Script generation failed: {e}"
            )

            knowledge["script"] = ""

            knowledge["script_error"] = str(e)

            scripts.append(knowledge)

    print("=" * 80)
    print(f"Successfully generated {len(scripts)} script(s)")
    print("=" * 80)

    return scripts
