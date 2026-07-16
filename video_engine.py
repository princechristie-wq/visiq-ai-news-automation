import os
import random

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

def create_videos(visual_packages):

    pass

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
