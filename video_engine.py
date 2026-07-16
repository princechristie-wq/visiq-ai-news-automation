import os
import random
import cv2
import numpy as np
import textwrap

from moviepy import (
    AudioFileClip,
    ImageClip,
    TextClip,
    CompositeVideoClip,
    CompositeAudioClip,
    afx,
)

# ============================================================
# VIDEO ENGINE CONFIGURATION
# ============================================================

VIDEO_WIDTH = 1080

VIDEO_HEIGHT = 1920

FPS = 24

IMAGE_HEIGHT = 1450

CAPTION_FONT_SIZE = 95

HEADLINE_FONT_SIZE = 48

BRAND_FONT_SIZE = 55

# ============================================================
# PUBLIC FUNCTION
# ============================================================

# ============================================================
# PUBLIC FUNCTION
# ============================================================

def create_videos(

    visual_packages,

    music_credits

):

    # Implementation will be connected
    # during final integration.

    return visual_packages
    
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

# ============================================================
# LOAD VOICE
# ============================================================

def load_voice():

    return AudioFileClip(
        "voice.mp3"
    )

# ============================================================
# LOAD BACKGROUND MUSIC
# ============================================================

def load_background_music(audio, music_credits):

    music_files = list(
        music_credits.keys()
    )

    music_file = random.choice(
        music_files
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

    return music, music_file

# ============================================================
# CREATE FINAL AUDIO
# ============================================================

def create_final_audio(
    voice,
    music
):

    return CompositeAudioClip(

        [
            music,
            voice
        ]

    )

# ============================================================
# PREPARE IMAGE CLIPS
# ============================================================

def prepare_image_clips(scene_plan, audio_duration):

    image_clips = []

    scene_duration = audio_duration / max(
        len(scene_plan),
        1
    )

    for index, scene in enumerate(scene_plan):

        image_file = f"image_{index+1}.jpg"

        if not os.path.exists(image_file):

            continue

        clip = (

            ImageClip(image_file)

            .resized(height=IMAGE_HEIGHT)

            .resized(

                lambda t:
                1 + 0.12 * t / scene_duration

            )

            .with_start(
                index * scene_duration
            )

            .with_duration(
                scene_duration
            )

            .with_position(
                ("center",220)
            )

        )

        image_clips.append(
            clip
        )

    return image_clips

# ============================================================
# CREATE HEADLINE
# ============================================================

def create_headline(topic, duration):

    headline = TextClip(

        text=topic,

        font_size=HEADLINE_FONT_SIZE,

        color="white",

        size=(1000, 200),

        method="caption"

    )

    headline = (

        headline

        .with_duration(duration)

        .with_position(("center", 60))

    )

    return headline

# ============================================================
# CREATE CAPTIONS
# ============================================================

def create_captions(script, duration):

    words = script.split()

    caption_clips = []

    chunk_size = 2

    duration_per_word = (

        duration * 0.95

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

            font_size=CAPTION_FONT_SIZE,

            color="white",

            stroke_color="black",

            stroke_width=5,

            size=(950,250),

            method="caption"

        )

        caption = (

            caption

            .with_start(start_time)

            .with_duration(clip_duration)

            .with_position(("center",980))

        )

        caption_clips.append(

            caption

        )

    return caption_clips

# ============================================================
# CREATE BRAND
# ============================================================

def create_brand(duration):

    brand = TextClip(

        text="VISIQ AI",

        font_size=BRAND_FONT_SIZE,

        color="white",

        size=(1080,200),

        method="caption"

    )

    brand = (

        brand

        .with_duration(duration)

        .with_position(("center",1760))

    )

    return brand

# ============================================================
# COMPOSE VIDEO
# ============================================================

def compose_video(

    background,

    image_clips,

    headline,

    captions,

    brand,

    final_audio,

    duration

):

    video = CompositeVideoClip(

        [background]

        + image_clips

        + [headline]

        + captions

        + [brand],

        size=(VIDEO_WIDTH, VIDEO_HEIGHT)

    )

    video = video.with_audio(

        final_audio

    )

    return video

# ============================================================
# EXPORT VIDEO
# ============================================================

def export_video(video):

    video.write_videofile(

        "final_video.mp4",

        fps=FPS,

        codec="libx264",

        audio_codec="aac",

        preset="ultrafast",

        threads=2

    )
