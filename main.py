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
    CompositeAudioClip,
    ColorClip,
    concatenate_videoclips,
    afx,
)

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

client = Groq(
api_key=os.environ["GROQ_API_KEY"]
)

music_credits = {
    "Music_1.mp3":
"""Music: Robots and Aliens - Joel Cummins 01
License: YouTube Audio Library""",

    "Music_2.mp3":
"""Music: Blue Moon - JVNA
License: YouTube Audio Library""",

    "Music_3.mp3":
"""Music: Giving Up - JVNA
License: YouTube Audio Library""",

    "Music_4.mp3":
"""Music: News Room News - Spence
License: YouTube Audio Library""",

    "Music_5.mp3":
"""Music: Odd News - Twin Musicom
Odd News by Twin Musicom is licensed under a Creative Commons Attribution 4.0 licence.
https://creativecommons.org/licenses/by/4.0/

Artist: http://www.twinmusicom.org/
License: YouTube Audio Library""",

    "Music_6.mp3":
"""Music: News Theme 2 - Audionautix
News Theme 2 by Audionautix is licensed under a Creative Commons Attribution 4.0 licence.
https://creativecommons.org/licenses/by/4.0/

Artist: http://audionautix.com/
License: YouTube Audio Library""",

    "Music_7.mp3":
"""Music: News Theme 1 - Audionautix
News Theme 1 by Audionautix is licensed under a Creative Commons Attribution 4.0 licence.
https://creativecommons.org/licenses/by/4.0/

Artist: http://audionautix.com/
License: YouTube Audio Library""",

    "Music_8.mp3":
"""Music: Newsreel - Max Surla_Media Right Productions
License: YouTube Audio Library""",

    "Music_9.mp3":
"""Music: Newsroom - Riot
License: YouTube Audio Library"""
}

print("Starting...")

import urllib.request

for i in range(1, 10):

    url = f"https://github.com/princechristie-wq/visiq-ai-news-automation/releases/download/Music-v1/Music_{i}.mp3"

    urllib.request.urlretrieve(
        url,
        f"Music_{i}.mp3"
    )

    print(f"Downloaded Music_{i}.mp3")
    
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
        (0, 1640),
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
def create_thumbnail(topic):

    width = 1080
    height = 1920

    # Use first AI image as thumbnail background
    image = cv2.imread("image_1.jpg")

    image = cv2.resize(
        image,
        (width, height)
    )

    # Dark overlay for text readability
    overlay = image.copy()

    cv2.rectangle(
        overlay,
        (0, 0),
        (width, height),
        (0, 0, 0),
        -1
    )

    image = cv2.addWeighted(
        overlay,
        0.45,
        image,
        0.55,
        0
    )

    # Bottom branding bar
    cv2.rectangle(
        image,
        (0, 560),
        (1280, 720),
        (255, 60, 60),
        -1
    )

    # Channel branding
    cv2.putText(
        image,
        "VISIQ AI",
        (40, 650),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (255, 255, 255),
        4
    )

    # Thumbnail headline
    headline = textwrap.fill(
        "BREAKING AI NEWS",
        width=15
    )

    y0 = 180

    for line in headline.split("\n"):

        cv2.putText(
            image,
            line,
            (50, y0),
            cv2.FONT_HERSHEY_SIMPLEX,
            2.2,
            (255, 255, 255),
            5
        )

        y0 += 100

    cv2.imwrite(
        "thumbnail.jpg",
        image
    )

    print("THUMBNAIL CREATED")
def create_video(topic):

    audio = AudioFileClip("voice.mp3")

    music_files = [
        "Music_1.mp3",
        "Music_2.mp3",
        "Music_3.mp3",
        "Music_4.mp3",
        "Music_5.mp3",
        "Music_6.mp3",
        "Music_7.mp3",
        "Music_8.mp3",
        "Music_9.mp3"
    ]

    music_file = random.choice(music_files)

    selected_music = os.path.basename(
        music_file
    )

    music_credit = music_credits[
        selected_music
    ]

    print(
        "Selected Music:",
        selected_music
    )
    music = AudioFileClip(
        music_file
    )

    music = music.with_effects(
        [
            afx.AudioLoop(
                duration=audio.duration
            )
        ]
    )

    music = music.with_volume_scaled(
    0.12
    )

    final_audio = CompositeAudioClip(
        [music, audio]
    )
    print("Current directory:", os.getcwd())
    print("Files in repository:")
    print(os.listdir("."))
    print("Selected music:", music_file)

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
                   lambda t: 1 + 0.12 * t / scene_duration
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
    words = script.split()

    caption_clips = []

    chunk_size = 2

    duration_per_word = (
        audio.duration * 0.95
    ) / max(
        len(words),
        1
    )

    for i in range(
        0,
        len(words),
        chunk_size
    ):

        caption_text = " ".join(
            words[i:i + chunk_size]
        )

        start_time = (
            i * duration_per_word
        )

        clip_duration = (
            len(words[i:i + chunk_size])
            * duration_per_word
        )

        caption = TextClip(
            text=caption_text,
            font_size=70,
            color="white",
            stroke_color="black",
            stroke_width=3,
            size=(1000, 200),
            method="caption"
        )

        caption = (
            caption
            .with_start(start_time)
            .with_duration(clip_duration)
            .with_position(("center", 1450))
        )

        caption_clips.append(
            caption
        )
    # ==========================
    # BRAND
    # ==========================

    brand = TextClip(
        text="VISIQ AI",
        font_size=55,
        color="white",
        size=(1080, 200),
        method="caption"
    )

    brand = (
        brand
        .with_duration(audio.duration)
        .with_position(("center", 1760))
    )

    # ==========================
    # COMPOSITION
    # ==========================

    final_video = CompositeVideoClip(
        [background]
        + image_clips
        + [headline]
        + caption_clips
        + [brand],
        size=(1080, 1920)
    )

    final_video = final_video.with_audio(final_audio)

    final_video.write_videofile(
        "final_video.mp4",
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        threads=2
    )     

def upload_to_youtube():

    creds = Credentials(
        None,
        refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YOUTUBE_CLIENT_ID"],
        client_secret=os.environ["YOUTUBE_CLIENT_SECRET"]
    )

    youtube = build(
        "youtube",
        "v3",
        credentials=creds
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": final_description,
                "tags": hashtags.split(),
                "categoryId": "28"
            },
            "status": {
                "privacyStatus": "private"
            }
        },
        media_body=MediaFileUpload(
            "final_video.mp4",
            resumable=True
        )
    )

    response = request.execute()

    print(
        "YOUTUBE VIDEO ID:",
        response["id"]
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
You are an expert YouTube Shorts creator.

Generate ONE viral AI news headline.

Rules:
- 6 to 12 words only
- Create curiosity
- Create urgency
- Sound like a YouTube Shorts title
- No colons
- No quotation marks
- No corporate language
- No clickbait that is false
- Return headline only

Good examples:

Google Just Changed Search Forever

OpenAI Reveals Its Most Powerful AI Yet

This New AI Tool Is Going Viral

Claude AI Beats Expectations Again

Nvidia's Latest AI Chip Breaks Records
"""
        }
    ]
)

topic = topic_response.choices[0].message.content.strip()# =====================================

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

* 220 to 260 words
* Strong hook
* Explain the news
* Explain why it matters
* End with:
  Subscribe Visiq AI for daily AI news.

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

selected_music = "Music_1.mp3"
music_credit = music_credits[selected_music]
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

final_description = (
    description
    + "\n\n--------------------\n"
    + "Music Credits\n"
    + "--------------------\n"
    + music_credit
)

with open("description.txt", "w", encoding="utf-8") as f:
    f.write(final_description)

with open("hashtags.txt", "w", encoding="utf-8") as f:
    f.write(hashtags)

with open("scene_prompts.txt", "w", encoding="utf-8") as f:
    f.write(scene_prompts)

asyncio.run(
    create_voice(script)
)

generate_images()

create_video(topic)

upload_to_youtube()

print("VOICE CREATED")
print("VIDEO UPLOADED")
print("SUCCESS")
