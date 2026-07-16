import requests

# ============================================================
# RESEARCH ENGINE CONFIGURATION
# ============================================================

MAX_DESCRIPTION_LENGTH = 3000

# ============================================================
# CREATE KNOWLEDGE PACKAGE
# ============================================================

def create_knowledge_package(topic):

    return {

        # Trend Engine Data
        "video_id": topic["videoId"],
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

def research_topic(topic, api_key):

    knowledge = create_knowledge_package(topic)

    details = get_video_details(
        topic["videoId"],
        api_key
    )

    knowledge["description"] = details.get(
        "description",
        ""
    )

    return knowledge

# ============================================================
# PUBLIC FUNCTION
# ============================================================

def research_topics(topics, api_key):

    knowledge_packages = []

    for topic in topics:

        package = research_topic(
            topic,
            api_key
        )

        knowledge_packages.append(
            package
        )

    return knowledge_packages

# ============================================================
# GET VIDEO DETAILS
# ============================================================

def get_video_details(video_id, api_key):

    url = (
        "https://www.googleapis.com/youtube/v3/videos"
        "?part=snippet"
        f"&id={video_id}"
        f"&key={api_key}"
    )

    response = requests.get(
        url,
        timeout=30
    )

    if response.status_code != 200:

        return {}

    data = response.json()

    if not data.get("items"):

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
