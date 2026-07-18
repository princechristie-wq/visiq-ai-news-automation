import os

from google.oauth2.credentials import Credentials

from googleapiclient.discovery import build

from googleapiclient.http import MediaFileUpload


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
# AUTHENTICATE
# ============================================================

def create_youtube_service():
    """
    Create and return an authenticated
    YouTube Data API service.
    """

    creds = Credentials(

        None,

        refresh_token=os.environ[
            "YOUTUBE_REFRESH_TOKEN"
        ],

        token_uri="https://oauth2.googleapis.com/token",

        client_id=os.environ[
            "YOUTUBE_CLIENT_ID"
        ],

        client_secret=os.environ[
            "YOUTUBE_CLIENT_SECRET"
        ]

    )

    youtube = build(

        YOUTUBE_API_NAME,

        YOUTUBE_API_VERSION,

        credentials=creds

    )

    return youtube


# ============================================================
# UPLOAD VIDEO
# ============================================================

def upload_video(

    title,

    description,

    hashtags

):
    """
    Upload a single video to YouTube.
    """

    if not os.path.exists(

        VIDEO_FILE

    ):

        raise FileNotFoundError(

            f"Video file not found: {VIDEO_FILE}"

        )

    print(

        f"Uploading '{title}'..."

    )

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

            VIDEO_FILE,

            resumable=True

        )

    )

    response = request.execute()

    print(

        f"Upload completed: {response['id']}"

    )

    return response["id"]


# ============================================================
# PUBLIC FUNCTION
# ============================================================

def upload_videos(
    video_packages
):
    """
    Upload all generated videos.
    """

    print(

        f"Uploading {len(video_packages)} video(s)..."

    )

    uploaded = []

    for index, package in enumerate(

        video_packages,

        start=1

    ):

        print(

            f"Uploading video {index}/{len(video_packages)}"

        )

        video_id = upload_video(

            package["title"],

            package["description"],

            package["hashtags"]

        )

        package["youtube_video_id"] = video_id

        uploaded.append(

            package

        )

    print(

        "All uploads completed."

    )

    return uploaded
