import os
from groq import Groq
import asyncio
import edge_tts
import textwrap
import random
import numpy as np
import cv2
import requests
import moviepy

print("MOVIEPY VERSION:", 
moviepy.__version__)

from moviepy import (
    AudioFileClip,
    ImageClip,
    TextClip,
    CompositeVideoClip,
    ColorClip,
    concatenate_videoclips
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
            timeout=120,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        if response.status_code == 200:

            with open(
                f"image_{i}.jpg",
                "wb"
            ) as f:

                f.write(
                    response.content
                )

            print(
                f"Downloaded image_{i}.jpg"
            )

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

        r = int(
            20 + (y / height) * 40
        )

        g = int(
            20 + (y / height) * 20
        )

        b = int(
            60 + (y / height) * 120
        )

        image[y, :] = (
            b,
            g,
            r
        )

    for _ in range(150):

        x = random.randint(
            0,
            width
        )

        y = random.randint(
            0,
            height
        )

        radius = random.randint(
            2,
            5
        )

        cv2.circle(
            image,
            (x, y),
            radius,
            (255, 255, 255),
            -1
        )

    cv2.rectangle(
        image,
        (0, 1740),
        (width, 1920),
        (255, 60, 60),
       -1
)

    cv2.putText(
        image,
        "VISIQ AI NEWS",
        (50, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (255, 255, 255),
        4
    )

    cv2.imwrite(
        "background.jpg",
        image
    )

def create_video(topic):

    audio = AudioFileClip("voice.mp3")

    create_background()

    background = (
        ImageClip("background.jpg")
        .with_duration(audio.duration)
    )

    with open(
        "scene_prompts.txt",
        "r",
        encoding="utf-8"
    ) as f:
        scenes = f.read().splitlines()

    print("Scenes loaded:", len(scenes))

    clips = []
    image_clips = []

    scene_duration = audio.duration / max(
        len(scenes),
        1
    )

    for index, scene in enumerate(scenes):

        image_file = f"image_{index + 1}.jpg"

        if os.path.exists(image_file):

            print("Using image:", image_file)

            img = (
                ImageClip(image_file)
               .resized(height=1450)
               .resized(
                   lambda t: 1 + 0.08 * t / scene_duration
               )    
                .with_start(index * scene_duration)
                .with_duration(scene_duration)
                .with_position(("center", 220))
            )

            image_clips.append(img)

        else:

            print("Missing image:", image_file)

    # ==========================
    # HEADLINE
    # ==========================

    headline = TextClip(
        text=topic,
        font_size=48,
        color="white",
        size=(1000, 200),
        method="caption"
    )

    headline = (
        headline
        .with_duration(audio.duration)
        .with_position(("center", 60))
    )

    # ==========================
    # BRAND
    # ==========================

    brand = TextClip(
        text="VISIQ AI",
        font_size=70,
        color="white"
    )

    brand = (
        brand
        .with_duration(audio.duration)
        .with_position(("center", 1780))
    )

    # ==========================
    # COMPOSITION
    # ==========================

    final_video = CompositeVideoClip(
        [background]
        + image_clips
        + [headline]
        + [brand],
        size=(1080, 1920)
    )

    final_video = final_video.with_audio(audio)

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
