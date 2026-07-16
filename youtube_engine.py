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

# ============================================================
# AUTHENTICATE
# ============================================================

def create_youtube_service():

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

    return build(

        "youtube",

        "v3",

        credentials=creds

    )

# ============================================================
# UPLOAD VIDEO
# ============================================================

def upload_video(

    title,

    description,

    hashtags

):

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

            "final_video.mp4",

            resumable=True

        )

    )

    response = request.execute()

    return response["id"]

# ============================================================
# PUBLIC FUNCTION
# ============================================================

def upload_videos(video_packages):

    uploaded = []

    for package in video_packages:

        video_id = upload_video(

            package["title"],

            package["description"],

            package["hashtags"]

        )

        package["youtube_video_id"] = video_id

        uploaded.append(package)

    return uploaded
