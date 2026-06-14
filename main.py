import os
from groq import Groq

client = Groq(
api_key=os.environ["GROQ_API_KEY"]
)

print("Starting...")

# =====================================

# TOPIC

# =====================================

topic_response = client.chat.completions.create(
model="llama-3.3-70b-versatile",
messages=[
{
"role": "user",
"content": """
Give one trending AI news topic.

Return only the topic.
"""
}
]
)

topic = topic_response.choices[0].message.content.strip()

# =====================================

# SCRIPT

# =====================================

script_response = client.chat.completions.create(
model="llama-3.3-70b-versatile",
messages=[
{
"role": "user",
"content": f"""
Write a YouTube Shorts narration.

TOPIC:
{topic}

Requirements:

* 120 to 150 words
* Strong hook
* Explain the news
* Explain why it matters
* End with:
  Follow Visiq AI for daily AI news.

Return narration only.
"""
}
]
)

script = script_response.choices[0].message.content.strip()

# =====================================

# METADATA

# =====================================

metadata_response = client.chat.completions.create(
model="llama-3.3-70b-versatile",
messages=[
{
"role": "user",
"content": f"""
Create YouTube Shorts metadata.

TOPIC:
{topic}

Return exactly:

TITLE: ...
DESCRIPTION: ...
HASHTAGS: ...
"""
}
]
)

metadata = metadata_response.choices[0].message.content.strip()

title = ""
description = ""
hashtags = ""

for line in metadata.splitlines():

    if line.startswith("TITLE:"):
        title = line.replace(
            "TITLE:",
            ""
        ).strip()

    elif line.startswith("DESCRIPTION:"):
        description = line.replace(
            "DESCRIPTION:",
            ""
        ).strip()

    elif line.startswith("HASHTAGS:"):
        hashtags = line.replace(
            "HASHTAGS:",
            ""
        ).strip()

with open("topic.txt", "w", encoding="utf-8") as f:
    f.write(topic)
with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script)

with open("title.txt", "w", encoding="utf-8") as f:
    f.write(title)

with open("description.txt", "w", encoding="utf-8") as f:
    f.write(description)

with open("hashtags.txt", "w", encoding="utf-8") as f:
    f.write(hashtags)

print("SUCCESS")
