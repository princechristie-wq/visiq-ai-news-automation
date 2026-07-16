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

