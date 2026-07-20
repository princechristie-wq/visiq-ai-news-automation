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

# ------------------------------------------------------------
# Video Settings
# ------------------------------------------------------------

VIDEO_WIDTH = 1080

VIDEO_HEIGHT = 1920

FPS = 24


# ------------------------------------------------------------
# Image Settings
# ------------------------------------------------------------

IMAGE_DISPLAY_HEIGHT = 1450


# ------------------------------------------------------------
# Headline Settings
# ------------------------------------------------------------

HEADLINE_FONT_SIZE = 48

HEADLINE_WIDTH = 1000

HEADLINE_HEIGHT = 200

HEADLINE_Y_POSITION = 60


# ------------------------------------------------------------
# Caption Settings
# ------------------------------------------------------------

CAPTION_FONT_SIZE = 95

CAPTION_WIDTH = 950

CAPTION_HEIGHT = 250

CAPTION_Y_POSITION = 980

CAPTION_STROKE_WIDTH = 5

CAPTION_WORDS_PER_CHUNK = 2

CAPTION_DURATION_FACTOR = 0.95


# ------------------------------------------------------------
# Branding Settings
# ------------------------------------------------------------

BRAND_TEXT = "VISIQ AI"

BRAND_FONT_SIZE = 55

BRAND_WIDTH = VIDEO_WIDTH

BRAND_HEIGHT = 200

BRAND_Y_POSITION = 1760


# ------------------------------------------------------------
# Export Settings
# ------------------------------------------------------------

VIDEO_CODEC = "libx264"

AUDIO_CODEC = "aac"

EXPORT_PRESET = "ultrafast"

EXPORT_THREADS = 2


# ------------------------------------------------------------
# File Names
# ------------------------------------------------------------

BACKGROUND_FILE = "background.jpg"

THUMBNAIL_FILE = "thumbnail.jpg"

VOICE_FILE = "voice.mp3"

OUTPUT_VIDEO_FILE = "final_video.mp4"

# ============================================================
# PUBLIC FUNCTION
# ============================================================

def create_videos(

    visual_packages,

    music_credits

):

    print(

        f"Creating {len(visual_packages)} video(s)..."

    )

    # Full implementation will be added
    # after all helper functions are reviewed.

    return visual_packages


# ============================================================
# CREATE BACKGROUND
# ============================================================

def create_background():

    width = VIDEO_WIDTH

    height = VIDEO_HEIGHT

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

        BACKGROUND_FILE,

        image

    )


# ============================================================
# CREATE THUMBNAIL
# ============================================================

def create_thumbnail(topic):

    width = VIDEO_WIDTH

    height = VIDEO_HEIGHT

    image = cv2.imread(

        "image_1.jpg"

    )

    if image is None:

        raise FileNotFoundError(

            "image_1.jpg not found."

        )

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

        (width, 720),

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

        THUMBNAIL_FILE,

        image

    )

    print(

        "THUMBNAIL CREATED"

    )

# ============================================================
# LOAD VOICE
# ============================================================

def load_voice():

    if not os.path.exists(
        VOICE_FILE
    ):

        raise FileNotFoundError(

            f"Voice file not found: {VOICE_FILE}"

        )

    return AudioFileClip(

        VOICE_FILE

    )

# ============================================================
# LOAD BACKGROUND MUSIC
# ============================================================

def load_background_music(
    audio,
    music_credits
):

    if not music_credits:

        raise ValueError(
            "No background music available."
        )

    music_files = list(
        music_credits.keys()
    )

    music_file = random.choice(
        music_files
    )

    if not os.path.exists(
        music_file
    ):

        raise FileNotFoundError(

            f"Music file not found: {music_file}"

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
    """
    Combine voice narration and background music
    into a single audio track.
    """

    final_audio = CompositeAudioClip(

        [
            music,
            voice
        ]

    )

    return final_audio

# ============================================================
# PREPARE IMAGE CLIPS
# ============================================================

def prepare_image_clips(
    scene_plan,
    audio_duration
):

    image_clips = []

    scene_duration = audio_duration / max(
        len(scene_plan),
        1
    )

    for index, scene in enumerate(scene_plan):

        scene_number = scene.get(
            "scene_number",
            index + 1
        )

        image_file = (
            f"image_{scene_number}.jpg"
        )

        if not os.path.exists(
            image_file
        ):

            print(
                f"Warning: {image_file} not found. Skipping scene."
            )

            continue

        motion = scene.get(
            "motion",
            "zoom_in"
        )

        clip = ImageClip(
            image_file
        ).resized(
            height=IMAGE_DISPLAY_HEIGHT
        )

        if motion == "zoom_in":

            clip = clip.resized(

                lambda t:
                1 + 0.12 * t / scene_duration

            )

        elif motion == "zoom_out":

            clip = clip.resized(

                lambda t:
                1.12 - 0.12 * t / scene_duration

            )

        # Future motion support
        # pan_left
        # pan_right
        # pan_up
        # pan_down
        # rotate

        clip = (

            clip

            .with_start(
                index * scene_duration
            )

            .with_duration(
                scene_duration
            )

            .with_position(
                ("center", 220)
            )

        )

        image_clips.append(
            clip
        )

    return image_clips

# ============================================================
# CREATE HEADLINE
# ============================================================

def create_headline(
    topic,
    duration
):
    """
    Create the headline shown at the top
    of the video.
    """

    headline = TextClip(

        text=topic,

        font_size=HEADLINE_FONT_SIZE,

        color="white",

        size=(1000, 200),

        method="caption"

    )

    headline = (

        headline

        .with_duration(
            duration
        )

        .with_position(
            ("center", 60)
        )

    )

    return headline

# ============================================================
# CREATE CAPTIONS
# ============================================================

def create_captions(
    script,
    duration
):
    """
    Create timed caption clips from the
    narration script.
    """

    words = script.split()

    caption_clips = []

    duration_per_word = (

        duration * CAPTION_DURATION_FACTOR

    ) / max(

        len(words),
        1

    )

    for i in range(

        0,

        len(words),

        CAPTION_WORDS_PER_CHUNK

    ):

        caption_text = " ".join(

            words[
                i:i + CAPTION_WORDS_PER_CHUNK
            ]

        )

        start_time = (

            i * duration_per_word

        )

        clip_duration = (

            len(

                words[
                    i:i + CAPTION_WORDS_PER_CHUNK
                ]

            )

            * duration_per_word

        )

        caption = TextClip(

            text=caption_text,

            font_size=CAPTION_FONT_SIZE,

            color="white",

            stroke_color="black",

            stroke_width=CAPTION_STROKE_WIDTH,

            size=(

                CAPTION_WIDTH,

                CAPTION_HEIGHT

            ),

            method="caption"

        )

        caption = (

            caption

            .with_start(

                start_time

            )

            .with_duration(

                clip_duration

            )

            .with_position(

                (

                    "center",

                    CAPTION_Y_POSITION

                )

            )

        )

        caption_clips.append(

            caption

        )

    return caption_clips

# ============================================================
# CREATE BRAND
# ============================================================

def create_brand(
    duration
):
    """
    Create the channel branding displayed
    at the bottom of the video.
    """

    brand = TextClip(

        text=BRAND_TEXT,

        font_size=BRAND_FONT_SIZE,

        color="white",

        size=(

            BRAND_WIDTH,

            BRAND_HEIGHT

        ),

        method="caption"

    )

    brand = (

        brand

        .with_duration(

            duration

        )

        .with_position(

            (

                "center",

                BRAND_Y_POSITION

            )

        )

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
    """
    Assemble all visual elements into the
    final video composition.
    """

    video_layers = (

        [background]

        + image_clips

        + [headline]

        + captions

        + [brand]

    )

    video = CompositeVideoClip(

        video_layers,

        size=(

            VIDEO_WIDTH,

            VIDEO_HEIGHT

        )

    )

    video = (

        video

        .with_duration(

            duration

        )

        .with_audio(

            final_audio

        )

    )

    return video

# ============================================================
# EXPORT VIDEO
# ============================================================

def export_video(
    video
):
    """
    Export the final video to disk.
    """

    print(

        f"Exporting video to {OUTPUT_VIDEO_FILE}..."

    )

    video.write_videofile(

        OUTPUT_VIDEO_FILE,

        fps=FPS,

        codec=VIDEO_CODEC,

        audio_codec=AUDIO_CODEC,

        preset=EXPORT_PRESET,

        threads=EXPORT_THREADS

    )

    print(

        "Video export completed."

    )
