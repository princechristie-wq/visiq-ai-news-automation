import requests

from config import YOUTUBE_API_KEY

# ============================================================
# RESEARCH ENGINE CONFIGURATION
# ============================================================

MAX_DESCRIPTION_LENGTH = 3000

# ============================================================
# GET YOUTUBE API KEY
# ============================================================

def get_api_key():
    """
    Return the configured YouTube API key.

    Raises:
        RuntimeError: If the API key is missing.
    """

    if not YOUTUBE_API_KEY:

        raise RuntimeError(
            "YOUTUBE_API_KEY is missing in config.py"
        )

    return YOUTUBE_API_KEY


# ============================================================
# CREATE KNOWLEDGE PACKAGE
# ============================================================

def create_knowledge_package(topic):
    """
    Create the base knowledge package that will be
    passed to later engines.
    """

    return {

        # Trend Engine Data
        "video_id": topic["videoId"],

        "video_url": (
            f"https://www.youtube.com/watch?v={topic['videoId']}"
        ),

        "title": topic["title"],
        "channel": topic["channel"],
        "published": topic["published"],
        "views": topic["views"],
        "likes": topic["likes"],
        "comments": topic["comments"],
        "trend_score": topic["trend_score"],

        # Research Engine Data
        "description": "",
        "summary": "",
        "keywords": [],
        "facts": [],
        "visuals": [],
        "references": []
    }

# ============================================================
# RESEARCH SINGLE TOPIC
# ============================================================

def research_topic(topic):
    """
    Retrieve additional information for a single
    trending topic and return a populated
    knowledge package.
    """

    knowledge = create_knowledge_package(topic)

    details = get_video_details(
        topic["videoId"]
    )

    knowledge["description"] = details.get(
        "description",
        ""
    ).strip()

    return knowledge


# ============================================================
# PUBLIC FUNCTION
# ============================================================

def research_topics(topics):
    """
    Research a list of trending topics.
    """

    knowledge_packages = []

    for topic in topics:

        package = research_topic(topic)

        knowledge_packages.append(package)

    return knowledge_packages


# ============================================================
# GET VIDEO DETAILS
# ============================================================

def get_video_details(video_id):
    """
    Retrieve video metadata from the YouTube Data API.
    """

    api_key = get_api_key()

    url = (
        "https://www.googleapis.com/youtube/v3/videos"
        "?part=snippet"
        f"&id={video_id}"
        f"&key={api_key}"
    )

    try:

        response = requests.get(
            url,
            timeout=30
        )

    except requests.RequestException as e:

        print(
            f"Failed to fetch video details: {e}"
        )

        return {}

    if response.status_code != 200:

        print(
            f"Failed to fetch details for video "
            f"{video_id} "
            f"({response.status_code})"
        )

        print(response.text)

        return {}

    data = response.json()

    if not data.get("items"):

        print(
            f"No details found for video: {video_id}"
        )

        return {}

    snippet = data["items"][0]["snippet"]

    return {

        "title": snippet.get(
            "title",
            ""
        ),

        "description": snippet.get(
            "description",
            ""
        )[:MAX_DESCRIPTION_LENGTH],

        "channel": snippet.get(
            "channelTitle",
            ""
        ),

        "published": snippet.get(
            "publishedAt",
            ""
        )

    }
