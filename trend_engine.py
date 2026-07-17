import os
import requests

from datetime import datetime, timezone

# ============================================================
# TREND ENGINE CONFIGURATION
# ============================================================

MAX_RESULTS_PER_SEARCH = 5

YOUTUBE_SEARCH_KEYWORDS = [

    # AI News
    "AI News",
    "Artificial Intelligence News",
    "AI Updates",

    # AI Companies
    "OpenAI News",
    "ChatGPT News",
    "Gemini AI News",
    "Claude AI News",
    "Anthropic News",
    "Meta AI News",
    "Llama AI News",
    "Microsoft Copilot News",
    "Perplexity AI News",
    "DeepSeek AI News",
    "Mistral AI News",
    "xAI News",
    "NVIDIA AI News",

    # AI Video Generation
    "AI Video Generator",
    "AI Video Editing",
    "Runway AI",
    "Pika AI",
    "Luma AI",
    "Veo AI",
    "Sora AI",
    "Kling AI",
    "Hailuo AI",

    # AI Image Generation
    "Midjourney",
    "Flux AI",
    "Ideogram AI",
    "Leonardo AI",
    "Stable Diffusion",

    # AI Voice
    "ElevenLabs",
    "AI Voice Generator",
    "AI Voice Cloning",
    "Text to Speech AI",

    # AI Coding
    "Cursor AI",
    "Windsurf AI",
    "GitHub Copilot",
    "Claude Code",
    "AI Coding",

    # AI Agents
    "AI Agents",
    "AI Automation",
    "Manus AI",
    "Agentic AI",

    # Robotics
    "Humanoid Robot",
    "Tesla Optimus",
    "Figure AI",
    "Boston Dynamics",

    # AI Hardware
    "AI Chips",
    "Semiconductor AI",
    "GPU AI",

    # AI Productivity
    "AI Tools",
    "Best AI Tools",
    "New AI Apps",
    "AI Software",
]

# ============================================================
# TREND SCORING CONFIGURATION
# ============================================================
VIDEOS_PER_DAY = 4
VIEW_WEIGHT = 1
LIKE_WEIGHT = 20
COMMENT_WEIGHT = 50

FRESHNESS_24H = 150000
FRESHNESS_48H = 100000
FRESHNESS_72H = 60000
FRESHNESS_WEEK = 25000

# ============================================================
# AUTHORITY CHANNEL BONUS
# ============================================================

AUTHORITY_CHANNELS = {

    "openai": 40000,
    "google": 35000,
    "anthropic": 35000,
    "nvidia": 30000,
    "matt wolfe": 20000,
    "futurepedia": 15000,
    "ai daily brief": 15000,
    "ai revolution": 15000,
    "the ai daily brief": 15000,
    "two minute papers": 20000,
    "all about ai": 15000,
    "cnbc": 10000,
    "bloomberg": 10000,
    "the verge": 10000,
}

# ============================================================
# GET YOUTUBE API KEY
# ============================================================

def get_api_key():

    API_KEY = get_api_key()

    return api_key

def get_video_statistics(video_ids):

    API_KEY = os.getenv("YOUTUBE_API_KEY")

    if not API_KEY:

        raise RuntimeError(
            "YOUTUBE_API_KEY environment variable is missing."
        )

    stats = {}

    # Process IDs in batches of 50
    for i in range(0, len(video_ids), 50):

        batch = video_ids[i:i + 50]

        ids = ",".join(batch)

        print("=" * 80)
        print(f"Processing batch {i//50 + 1}")
        print(f"Videos in batch: {len(batch)}")

        url = (
            "https://www.googleapis.com/youtube/v3/videos"
            "?part=statistics"
            f"&id={ids}"
            f"&key={API_KEY}"
        )

        try:

            response = requests.get(
                url,
                timeout=30
            )

        except requests.RequestException as e:

            print(f"Network error: {e}")

            continue

        if response.status_code != 200:

            print("Statistics API Error")
            print(response.text)
            continue

        data = response.json()

        for item in data.get("items", []):

            stats[item["id"]] = {

                "views": int(
                    item["statistics"].get(
                        "viewCount",
                        0
                    )
                ),

                "likes": int(
                    item["statistics"].get(
                        "likeCount",
                        0
                    )
                ),

                "comments": int(
                    item["statistics"].get(
                        "commentCount",
                        0
                    )
                )

            }

    return stats

# ============================================================
# CALCULATE AUTHORITY BONUS
# ============================================================

def get_authority_bonus(channel_name):

    channel = channel_name.lower()

    for authority, bonus in AUTHORITY_CHANNELS.items():

        if authority in channel:

            return bonus

    return 0

# ============================================================
# CALCULATE FRESHNESS BONUS
# ============================================================

def get_freshness_bonus(published_date):

    published = datetime.fromisoformat(
        published_date.replace("Z", "+00:00")
    )

    hours_old = (
        datetime.now(timezone.utc) - published
    ).total_seconds() / 3600

    if hours_old <= 24:

        return FRESHNESS_24H, round(hours_old, 1)

    elif hours_old <= 48:

        return FRESHNESS_48H, round(hours_old, 1)

    elif hours_old <= 72:

        return FRESHNESS_72H, round(hours_old, 1)

    elif hours_old <= 168:

        return FRESHNESS_WEEK, round(hours_old, 1)

    return 0, round(hours_old, 1)

# ============================================================
# CALCULATE TREND SCORE
# ============================================================

def calculate_trend_score(video, statistics):

    stats = statistics.get(
        video["videoId"],
        {}
    )

    views = stats.get("views", 0)
    likes = stats.get("likes", 0)
    comments = stats.get("comments", 0)

    freshness_bonus, hours_old = get_freshness_bonus(
        video["published"]
    )

    authority_bonus = get_authority_bonus(
        video["channel"]
    )

    trend_score = (
        (views * VIEW_WEIGHT)
        + (likes * LIKE_WEIGHT)
        + (comments * COMMENT_WEIGHT)
        + freshness_bonus
        + authority_bonus
    )

    video["views"] = views
    video["likes"] = likes
    video["comments"] = comments
    video["hours_old"] = hours_old
    video["freshness_bonus"] = freshness_bonus
    video["authority_bonus"] = authority_bonus
    video["trend_score"] = trend_score

    return video

# ============================================================
# SEARCH YOUTUBE
# ============================================================

def get_youtube_trending_topics():

    print("=" * 80)
    print("SEARCHING YOUTUBE...")
    print("=" * 80)

    API_KEY = get_api_key()

    videos = []

    for keyword in YOUTUBE_SEARCH_KEYWORDS:

        print(f"Searching: {keyword}")

        url = (
            "https://www.googleapis.com/youtube/v3/search"
            "?part=snippet"
            "&type=video"
            f"&maxResults={MAX_RESULTS_PER_SEARCH}"
            "&order=date"
            "&relevanceLanguage=en"
            f"&q={requests.utils.quote(keyword)}"
            f"&key={API_KEY}"
        )

        try:

            response = requests.get(
                url,
                timeout=30
            )

        except requests.RequestException as e:

            print(f"Network error: {e}")

            continue

        if response.status_code != 200:

            print("Search failed.")
            continue

        data = response.json()

        for item in data.get("items", []):

            videos.append({

                "title": item["snippet"]["title"],
                "channel": item["snippet"]["channelTitle"],
                "published": item["snippet"]["publishedAt"],
                "videoId": item["id"]["videoId"]

            })

    return videos

# ============================================================
# PUBLIC FUNCTION
# ============================================================

def get_trending_topics():

    videos = get_youtube_trending_topics()
    unique_videos = {}

    for video in videos:

        unique_videos[video["videoId"]] = video

    videos = list(unique_videos.values())
    
    if not videos:

    print("No trending videos found.")

    return []
    video_ids = []

    for video in videos:

        video_ids.append(
            video["videoId"]
        )

    statistics = get_video_statistics(
        video_ids
    )

    scored_videos = []

    for video in videos:

        scored_video = calculate_trend_score(
            video,
            statistics
        )

        scored_videos.append(
            scored_video
        )

    scored_videos.sort(
        key=lambda x: x["trend_score"],
        reverse=True
    )

    return scored_videos[:VIDEOS_PER_DAY]
