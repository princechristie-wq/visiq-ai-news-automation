import os

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from config import (
    YOUTUBE_CLIENT_ID,
    YOUTUBE_CLIENT_SECRET,
    YOUTUBE_REFRESH_TOKEN,
)

# ============================================================
# YOUTUBE ENGINE CONFIGURATION
# ============================================================

CATEGORY_ID = "28"

DEFAULT_LANGUAGE = "en"

PRIVACY_STATUS = "public"

VIDEO_FILE = "final_video.mp4"

YOUTUBE_API_NAME = "youtube"

YOUTUBE_API_VERSION = "v3"


# ============================================================
# VALIDATION
# ============================================================

def validate_package(package):
    """
    Validate that the package contains all information
    required for uploading to YouTube.
    """

    required_fields = [

        "title",
        "description",
        "hashtags"

    ]

    for field in required_fields:

        if field not in package:

            raise ValueError(
                f"Missing required field: {field}"
            )

        if not str(package[field]).strip():

            raise ValueError(
                f"{field} is empty."
            )

    if not os.path.exists(VIDEO_FILE):

        raise FileNotFoundError(
            f"Video file not found: {VIDEO_FILE}"
        )


# ============================================================
# AUTHENTICATE
# ============================================================

def create_youtube_service():
    """
    Create and return an authenticated
    YouTube Data API service.
    """

    missing = []

    if not YOUTUBE_CLIENT_ID:
        missing.append("YOUTUBE_CLIENT_ID")

    if not YOUTUBE_CLIENT_SECRET:
        missing.append("YOUTUBE_CLIENT_SECRET")

    if not YOUTUBE_REFRESH_TOKEN:
        missing.append("YOUTUBE_REFRESH_TOKEN")

    if missing:

        raise ValueError(
            "Missing YouTube configuration: "
            + ", ".join(missing)
        )

    credentials = Credentials(

        token=None,

        refresh_token=YOUTUBE_REFRESH_TOKEN,

        token_uri="https://oauth2.googleapis.com/token",

        client_id=YOUTUBE_CLIENT_ID,

        client_secret=YOUTUBE_CLIENT_SECRET

    )

    return build(

        YOUTUBE_API_NAME,

        YOUTUBE_API_VERSION,

        credentials=credentials

    )

# ============================================================
# UPLOAD VIDEO
# ============================================================

def upload_video(
    title,
    description,
    hashtags,
    video_file=VIDEO_FILE
):
    """
    Upload a single video to YouTube.

    Returns:
        str: Uploaded YouTube video ID.
    """

    if not os.path.exists(video_file):

        raise FileNotFoundError(
            f"Video file not found: {video_file}"
        )

    print(f"Uploading: {title}")

    youtube = create_youtube_service()

    request = youtube.videos().insert(

        part="snippet,status,paidProductPlacementDetails",

        body={

            "snippet": {

                "title": title,

                "description": description,

                "tags": hashtags.split(),

                "categoryId": CATEGORY_ID,

                "defaultLanguage": DEFAULT_LANGUAGE,

                "defaultAudioLanguage": DEFAULT_LANGUAGE

            },

            "status": {

                "privacyStatus": PRIVACY_STATUS,

                "selfDeclaredMadeForKids": False,

                "containsSyntheticMedia": True

            },

            "paidProductPlacementDetails": {

                "hasPaidProductPlacement": False

            }

        },

        media_body=MediaFileUpload(

            video_file,

            resumable=True

        )

    )

    response = request.execute()

    video_id = response["id"]

    print(f"Upload successful: {video_id}")

    return video_id


# ============================================================
# PUBLIC FUNCTION
# ============================================================

def upload_videos(
    video_packages
):
    """
    Upload all generated videos to YouTube.

    Returns:
        list[dict]
    """

    print("=" * 80)
    print("YOUTUBE UPLOAD")
    print("=" * 80)

    total = len(video_packages)

    uploaded = []

    for index, package in enumerate(
        video_packages,
        start=1
    ):

        title = package.get(
            "title",
            "Untitled"
        )

        print()
        print("=" * 80)
        print(f"[{index}/{total}] {title}")
        print("=" * 80)

        try:

            validate_package(
                package
            )

            video_file = package.get(
                "video_file",
                VIDEO_FILE
            )

            video_id = upload_video(

                title=package["title"],

                description=package["description"],

                hashtags=package["hashtags"],

                video_file=video_file

            )

            package["youtube_video_id"] = video_id

            package["youtube_url"] = (
                f"https://www.youtube.com/watch?v={video_id}"
            )

            package["upload_status"] = "success"

            print("Upload completed successfully.")

        except Exception as e:

            print(f"Upload failed: {e}")

            package["upload_status"] = "failed"

            package["upload_error"] = str(e)

        uploaded.append(
            package
        )

    successful = sum(
        1
        for package in uploaded
        if package.get("upload_status") == "success"
    )

    print()
    print("=" * 80)
    print(
        f"UPLOAD COMPLETE ({successful}/{total} successful)"
    )
    print("=" * 80)

    return uploaded
