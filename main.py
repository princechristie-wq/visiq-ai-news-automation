import os
from groq import Groq
import asyncio
import edge_tts
import textwrap
import numpy as np
import cv2
import requests

from moviepy import (
    AudioFileClip,
    ImageClip,
    TextClip,
    CompositeVideoClip
)

client = Groq(
api_key=os.environ["GROQ_API_KEY"]
)

print("Starting...")
async def create_voice(script):

    communicate = edge_tts.Communicate(
        text=script,
        voice="en-US-ChristopherNeural",
        rate="+25%"
    )

    await communicate.save(
        "voice.mp3"
    )

def generate_images():

    prompts = scene_prompts.splitlines()

    print(f"Found {len(prompts)} prompts")

    for i, prompt in enumerate(prompts, start=1):
        
        print(f"Generating image {i}")

        url = (
            "https://image.pollinations.ai/prompt/"
            + requests.utils.quote(prompt)
        )

        response = requests.get(
            url,
            timeout=120
        )

       if response.status_code == 200:

           with open(f"image_{i}.jpg", "wb") as f:
               f.write(response.content)

           print(f"Downloaded image_{i}.jpg")

       else:

           print(
               f"Failed image {i} - Status Code: {response.status_code}"
           )
           
def create_background():
    width = 1080
    height = 1920

    image = np.zeros(
        (height, width, 3),
        dtype=np.uint8
    )

    for y in range(height):

        value = int(
            20 + (y / height) * 80
        )

        image[y, :] = (
            value,
            value,
            value + 20
        )

    cv2.rectangle(
        image,
        (0, 0),
        (width, 180),
        (0, 0, 180),
        -1
    )

    cv2.putText(
        image,
        "BREAKING AI NEWS",
        (60, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (255, 255, 255),
        5
    )

    cv2.imwrite(
        "background.jpg",
        image
    )


def create_video(topic):

    audio = AudioFileClip(
        "voice.mp3"
    )

    create_background()

    background = (
        ImageClip("background.jpg")
        .with_duration(audio.duration)
    )

    headline_text = "\n".join(
        textwrap.wrap(
            topic,
            width=18
        )
    )

    headline = TextClip(
        text=headline_text,
        font_size=85,
        color="white",
        size=(900, None),
        method="caption"
    )

    headline = (
        headline
        .with_duration(audio.duration)
        .with_position(
            ("center", 500)
        )
    )

    brand = TextClip(
        text="VISIQ AI",
        font_size=60,
        color="white"
    )

    brand = (
        brand
        .with_duration(audio.duration)
        .with_position(
            ("center", 1650)
        )
    )

    final_video = CompositeVideoClip(
        [
            background,
            headline,
            brand
        ],
        size=(1080, 1920)
    )

    final_video = final_video.with_audio(
        audio
    )

    final_video.write_videofile(
        "final_video.mp4",
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        threads=2
    )
     
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
# SCENE PROMPTS
# =====================================

scene_response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": f"""
You are creating visuals for a YouTube AI News Short.

TOPIC:
{topic}

SCRIPT:
{script}

Create exactly 10 image prompts.

Requirements:
- AI related
- Futuristic
- Cinematic
- Suitable for YouTube Shorts
- One prompt per line
- No numbering

Return only the prompts.
"""
        }
    ]
)

scene_prompts = scene_response.choices[0].message.content.strip()

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

with open("scene_prompts.txt", "w", encoding="utf-8") as f:
    f.write(scene_prompts)

asyncio.run(
    create_voice(script)
)

generate_images()

create_video(topic)

print("VOICE CREATED")
print("SUCCESS")
