import os
import random
import textwrap
import asyncio

import cv2
import edge_tts
import numpy as np
import requests

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

# ------------------------------------------------------------
# Voice Settings
# ------------------------------------------------------------

VOICE_NAME = "en-US-ChristopherNeural"

VOICE_RATE = "+25%"

# ------------------------------------------------------------
# Image Generation Settings
# ------------------------------------------------------------

IMAGE_MODEL = "flux"

IMAGE_WIDTH = 768

IMAGE_HEIGHT = 1344

IMAGE_TIMEOUT = 120

USER_AGENT = "Mozilla/5.0"

OUTPUT_VIDEO_FILE = "final_video.mp4"


# ============================================================
# VALIDATION
# ============================================================

def validate_package(knowledge):
    """
    Validate that the package contains the minimum
    information required for video generation.
    """

    required_fields = [

        "title",
        "script",
        "scene_plan"

    ]

    for field in required_fields:

        if field not in knowledge:

            raise ValueError(
                f"Missing required field: {field}"
            )

    if not knowledge["script"].strip():

        raise ValueError(
            "Script is empty."
        )

    if not knowledge["scene_plan"]:

        raise ValueError(
            "Scene plan is empty."
        )

# ============================================================
# VOICE GENERATION
# ============================================================

async def _generate_voice_async(
    script
):
    """
    Generate narration using Microsoft Edge TTS.
    """

    communicate = edge_tts.Communicate(

        text=script,

        voice=VOICE_NAME,

        rate=VOICE_RATE

    )

    await communicate.save(
        VOICE_FILE
    )


def generate_voice(
    script
):
    """
    Generate narration audio.

    Returns:
        str : voice.mp3
    """

    if not script.strip():

        raise ValueError(
            "Script is empty."
        )

    print("Generating narration...")

    asyncio.run(
        _generate_voice_async(
            script
        )
    )

    if not os.path.exists(
        VOICE_FILE
    ):

        raise RuntimeError(
            "Voice generation failed."
        )

    print("Narration created.")

    return VOICE_FILE

# ============================================================
# IMAGE GENERATION
# ============================================================

def generate_images(
    scene_plan
):
    """
    Generate one image for every scene.

    Images are saved as:

        image_1.jpg
        image_2.jpg
        ...

    """

    if not scene_plan:

        raise ValueError(
            "Scene plan is empty."
        )

    print("Generating images...")

    for scene in scene_plan:

        scene_number = scene.get(
            "scene_number"
        )

        prompt = scene.get(
            "image_prompt",
            ""
        ).strip()

        if not prompt:

            raise ValueError(
                f"Scene {scene_number} has no image prompt."
            )

        quality_prompt = (
            "masterpiece, best quality, "
            "ultra detailed, photorealistic, "
            "cinematic lighting, "
            "professional photography, "
            "8k, HDR, realistic textures, "
            "award winning photography, "
            + prompt
        )

        negative_prompt = (
            "people, person, humans, face, portrait, "
            "hands, body, crowd, meeting, office, "
            "logo, watermark, text, cartoon, painting"
        )

        final_prompt = (
            quality_prompt
            + ", "
            + negative_prompt
        )

        seed = random.randint(
            1,
            999999999
        )

        url = (

            "https://image.pollinations.ai/prompt/"

            + requests.utils.quote(
                final_prompt
            )

            + f"?model={IMAGE_MODEL}"

            + f"&seed={seed}"

            + f"&width={IMAGE_WIDTH}"

            + f"&height={IMAGE_HEIGHT}"

            + "&nologo=true"

        )

        print(
            f"Generating image {scene_number}"
        )

        response = requests.get(

            url,

            timeout=IMAGE_TIMEOUT,

            headers={

                "User-Agent": USER_AGENT

            }

        )

        if response.status_code != 200:

            raise RuntimeError(
                f"Image generation failed for Scene {scene_number}"
            )

        filename = (
            f"image_{scene_number}.jpg"
        )

        with open(
            filename,
            "wb"
        ) as file:

            file.write(
                response.content
            )

        print(
            f"Saved {filename}"
        )

    print("Image generation complete.")

# ============================================================
# CREATE BACKGROUND
# ============================================================

def create_background():
    """
    Create the default Visiq AI background.
    """

    width = VIDEO_WIDTH
    height = VIDEO_HEIGHT

    image = np.zeros(
        (height, width, 3),
        dtype=np.uint8
    )

    # --------------------------------------------------------
    # Gradient
    # --------------------------------------------------------

    for y in range(height):

        r = int(20 + (y / height) * 40)
        g = int(20 + (y / height) * 20)
        b = int(60 + (y / height) * 120)

        image[y, :] = (b, g, r)

    # --------------------------------------------------------
    # Decorative particles
    # --------------------------------------------------------

    for _ in range(150):

        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.randint(2, 5)

        cv2.circle(
            image,
            (x, y),
            radius,
            (255, 255, 255),
            -1
        )

    # --------------------------------------------------------
    # Branding strip
    # --------------------------------------------------------

    cv2.rectangle(
        image,
        (0, 1640),
        (width, height),
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

    return BACKGROUND_FILE


# ============================================================
# CREATE THUMBNAIL
# ============================================================

def create_thumbnail(topic):
    """
    Create a thumbnail using the first generated image.
    """

    width = VIDEO_WIDTH
    height = VIDEO_HEIGHT

    image = cv2.imread("image_1.jpg")

    if image is None:

        raise FileNotFoundError(
            "image_1.jpg not found."
        )

    image = cv2.resize(
        image,
        (width, height)
    )

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

    cv2.rectangle(
        image,
        (0, 560),
        (width, 720),
        (255, 60, 60),
        -1
    )

    cv2.putText(
        image,
        BRAND_TEXT,
        (40, 650),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (255, 255, 255),
        4
    )

    headline = textwrap.fill(
        topic,
        width=15
    )

    y = 180

    for line in headline.split("\n"):

        cv2.putText(
            image,
            line,
            (50, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            2.0,
            (255, 255, 255),
            5
        )

        y += 95

    cv2.imwrite(
        THUMBNAIL_FILE,
        image
    )

    print("Thumbnail created.")

    return THUMBNAIL_FILE


# ============================================================
# LOAD VOICE
# ============================================================

def load_voice():
    """
    Load the narration audio.
    """

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
    """
    Load and loop background music.
    """

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
    Combine narration and background music.
    """

    return CompositeAudioClip(
        [
            music,
            voice
        ]
    )

# ============================================================
# PREPARE IMAGE CLIPS
# ============================================================

def prepare_image_clips(
    scene_plan,
    audio_duration
):
    """
    Prepare image clips with simple motion effects.
    """

    image_clips = []

    total_scenes = max(
        len(scene_plan),
        1
    )

    scene_duration = (
        audio_duration / total_scenes
    )

    for index, scene in enumerate(scene_plan):

        scene_number = scene.get(
            "scene_number",
            index + 1
        )

        image_file = f"image_{scene_number}.jpg"

        if not os.path.exists(image_file):

            print(
                f"Warning: {image_file} not found. Skipping."
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
                1 + 0.12 * (t / scene_duration)
            )

        elif motion == "zoom_out":

            clip = clip.resized(
                lambda t:
                1.12 - 0.12 * (t / scene_duration)
            )

        elif motion == "pan_left":

            clip = clip.with_position(
                lambda t: (
                    -80 * (t / scene_duration),
                    220
                )
            )

        elif motion == "pan_right":

            clip = clip.with_position(
                lambda t: (
                    80 * (t / scene_duration),
                    220
                )
            )

        elif motion == "pan_up":

            clip = clip.with_position(
                lambda t: (
                    "center",
                    220 - 80 * (t / scene_duration)
                )
            )

        elif motion == "pan_down":

            clip = clip.with_position(
                lambda t: (
                    "center",
                    220 + 80 * (t / scene_duration)
                )
            )

        clip = (
            clip
            .with_start(
                index * scene_duration
            )
            .with_duration(
                scene_duration
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
    Create the headline displayed at the top.
    """

    return (
        TextClip(
            text=topic,
            font_size=HEADLINE_FONT_SIZE,
            color="white",
            size=(
                HEADLINE_WIDTH,
                HEADLINE_HEIGHT
            ),
            method="caption"
        )
        .with_duration(duration)
        .with_position(
            ("center", HEADLINE_Y_POSITION)
        )
    )


# ============================================================
# CREATE CAPTIONS
# ============================================================

def create_captions(
    script,
    duration
):
    """
    Create animated caption clips.
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

        chunk = words[
            i:i + CAPTION_WORDS_PER_CHUNK
        ]

        caption = " ".join(chunk)

        start_time = (
            i * duration_per_word
        )

        clip_duration = (
            len(chunk)
            * duration_per_word
        )

        clip = (
            TextClip(
                text=caption,
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
            .with_start(start_time)
            .with_duration(clip_duration)
            .with_position(
                (
                    "center",
                    CAPTION_Y_POSITION
                )
            )
        )

        caption_clips.append(
            clip
        )

    return caption_clips


# ============================================================
# CREATE BRAND
# ============================================================

def create_brand(
    duration
):
    """
    Create bottom branding.
    """

    return (
        TextClip(
            text=BRAND_TEXT,
            font_size=BRAND_FONT_SIZE,
            color="white",
            size=(
                BRAND_WIDTH,
                BRAND_HEIGHT
            ),
            method="caption"
        )
        .with_duration(duration)
        .with_position(
            (
                "center",
                BRAND_Y_POSITION
            )
        )
    )

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
    Combine all visual and audio elements into the final video.
    """

    clips = [background]

    clips.extend(image_clips)

    clips.append(headline)

    clips.extend(captions)

    clips.append(brand)

    video = CompositeVideoClip(
        clips,
        size=(
            VIDEO_WIDTH,
            VIDEO_HEIGHT
        )
    )

    video = (
        video
        .with_duration(duration)
        .with_audio(final_audio)
    )

    return video

def create_videos(
    visual_packages,
    music_credits
):
    """
    Generate finished videos for every knowledge package.
    """

    print("=" * 80)
    print("VIDEO GENERATION")
    print("=" * 80)

    total = len(visual_packages)

    completed = []

    for index, knowledge in enumerate(
        visual_packages,
        start=1
    ):

        title = knowledge.get(
            "title",
            "Untitled"
        )

        print()
        print("=" * 80)
        print(f"[{index}/{total}] {title}")
        print("=" * 80)

        voice = None
        music = None
        final_audio = None
        video = None

        try:

            validate_package(
                knowledge
            )

            print("Creating background...")
            create_background()

            print("Generating images...")

            generate_images(
            knowledge["scene_plan"]
            )

            print("Creating thumbnail...")

            create_thumbnail(
            title
            )

            print("Generating narration...")

            generate_voice(
            knowledge["script"]
            )

            print("Loading narration...")

            voice = load_voice()
            
            print("Loading background music...")
            music, music_file = load_background_music(
                voice,
                music_credits
            )

            print("Mixing audio...")
            final_audio = create_final_audio(
                voice,
                music
            )

            duration = voice.duration

            print("Preparing background clip...")

            background = (
                ImageClip(BACKGROUND_FILE)
                .with_duration(duration)
            )

            print("Preparing image clips...")

            image_clips = prepare_image_clips(
                knowledge["scene_plan"],
                duration
            )

            print("Creating headline...")
            headline = create_headline(
                title,
                duration
            )

            print("Creating captions...")
            captions = create_captions(
                knowledge["script"],
                duration
            )

            print("Creating branding...")
            brand = create_brand(
                duration
            )

            print("Compositing video...")

            video = compose_video(
                background,
                image_clips,
                headline,
                captions,
                brand,
                final_audio,
                duration
            )

            print("Exporting...")

            export_video(
                video
            )

            knowledge["video_file"] = OUTPUT_VIDEO_FILE
            knowledge["thumbnail_file"] = THUMBNAIL_FILE
            knowledge["background_music"] = music_file

            print("Video completed successfully.")

        except Exception as e:

            print(f"Video generation failed: {e}")

            knowledge["video_error"] = str(e)

        finally:

            try:

                if video is not None:
                    video.close()

                if final_audio is not None:
                    final_audio.close()

                if voice is not None:
                    voice.close()

                if music is not None:
                    music.close()

            except Exception:
                pass

        completed.append(
            knowledge
        )

    print()
    print("=" * 80)
    print("VIDEO GENERATION COMPLETE")
    print("=" * 80)

    return completed

# ============================================================
# EXPORT VIDEO
# ============================================================

def export_video(
    video
):
    """
    Export the final video.
    """

    print(
        f"Exporting {OUTPUT_VIDEO_FILE}..."
    )

    video.write_videofile(

        OUTPUT_VIDEO_FILE,

        fps=FPS,

        codec=VIDEO_CODEC,

        audio_codec=AUDIO_CODEC,

        preset=EXPORT_PRESET,

        threads=EXPORT_THREADS,

        logger="bar"

    )

    print("Export complete.")
