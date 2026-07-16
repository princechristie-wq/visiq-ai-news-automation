from groq import Groq

# ============================================================
# SCRIPT ENGINE CONFIGURATION
# ============================================================

MODEL_NAME = "llama-3.3-70b-versatile"

TARGET_WORDS = 200

VOICE_STYLE = "Energetic"

CHANNEL_NAME = "Visiq AI"

# ============================================================
# CREATE GROQ CLIENT
# ============================================================

def create_client(api_key):

    return Groq(
        api_key=api_key
    )

# ============================================================
# BUILD SCRIPT PROMPT
# ============================================================

def build_script_prompt(knowledge):

    return f"""
You are a professional YouTube Shorts writer.

Channel:
{CHANNEL_NAME}

Topic:
{knowledge['title']}

Description:
{knowledge['description']}

Write a completely original YouTube Shorts script.

Requirements:

- Around {TARGET_WORDS} words
- Strong hook in the first sentence
- Conversational English
- Explain the technology clearly
- Focus on facts
- Avoid speculation
- End with:

Subscribe to Visiq AI for daily AI updates.

Return narration only.
"""

# ============================================================
# GENERATE SCRIPT
# ============================================================

def generate_script(knowledge, api_key):

    client = create_client(api_key)

    prompt = build_script_prompt(
        knowledge
    )

    response = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]

    )

    script = response.choices[0].message.content.strip()

    knowledge["script"] = script

    return knowledge

# ============================================================
# PUBLIC FUNCTION
# ============================================================

def generate_scripts(knowledge_packages, api_key):

    scripts = []

    for knowledge in knowledge_packages:

        script = generate_script(
            knowledge,
            api_key
        )

        scripts.append(
            script
        )

    return scripts
