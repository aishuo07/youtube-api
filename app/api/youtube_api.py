import requests
from datetime import datetime
from app.database.db_setup import SessionLocal
from app.api.insights import extract_keywords, calculate_engagement, insert_channel, insert_video, insert_video_insight
from app.utils.helpers import from_dict
from config import API_KEY
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Snippet:
    publishedAt: str
    channelId: str
    title: str
    description: str
    channelTitle: str
    liveBroadcastContent: str
    publishTime: Optional[str] = None

@dataclass
class Id:
    kind: str
    videoId: str

@dataclass
class SearchResult:
    kind: str
    etag: str
    id: Id
    snippet: Snippet

@dataclass
class PageInfo:
    totalResults: int
    resultsPerPage: int

@dataclass
class YouTubeSearchResponse:
    kind: str
    etag: str
    nextPageToken: Optional[str] = None
    regionCode: str = ""
    pageInfo: PageInfo = field(default_factory=PageInfo)
    items: List[SearchResult] = field(default_factory=list)

@dataclass
class Statistics:
    viewCount: str
    likeCount: Optional[str] = None
    favoriteCount: Optional[str] = None
    commentCount: Optional[str] = None

@dataclass
class Video:
    kind: str
    etag: str
    id: str
    snippet: Snippet
    statistics: Statistics

@dataclass
class YouTubeVideoListResponse:
    kind: str
    etag: str
    items: List[Video]
    pageInfo: PageInfo

def collect_video_ids(youtube_response):
    return [item.id.videoId for item in youtube_response.items]

def fetch_youtube_data(channel_ids):
    db = SessionLocal()

    for channel_id in channel_ids:
        try:
            response = requests.get(
                f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={channel_id}&part=snippet,id&order=date&maxResults=50"
            )
            response.raise_for_status()
            youtube_response = from_dict(YouTubeSearchResponse, response.json())
            videos = collect_video_ids(youtube_response)

            if videos:
                response = requests.get(
                    f"https://youtube.googleapis.com/youtube/v3/videos?part=statistics,snippet&id={','.join(videos)}&key={API_KEY}"
                )
                response.raise_for_status()
                youtube_video_response = from_dict(YouTubeVideoListResponse, response.json())

                channel_title = youtube_response.items[0].snippet.channelTitle
                insert_channel(db, channel_id, channel_title, youtube_video_response)

                for video in youtube_video_response.items:
                    published_at = datetime.strptime(video.snippet.publishedAt, "%Y-%m-%dT%H:%M:%SZ")
                    insert_video(
                        db, video.id, video.snippet.channelId, video.snippet.title, video.snippet.description,
                        published_at, int(video.statistics.viewCount), int(video.statistics.likeCount),
                        int(video.statistics.commentCount)
                    )

                    keywords = extract_keywords(video.snippet.title, video.snippet.description)
                    engagement_score = calculate_engagement(
                        int(video.statistics.viewCount), int(video.statistics.likeCount), int(video.statistics.commentCount)
                    )

                    insert_video_insight(db, video.id, keywords, engagement_score)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for channel {channel_id}: {e}")
    db.close()
