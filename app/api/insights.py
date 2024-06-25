from datetime import datetime

import pandas as pd
from collections import defaultdict
from sqlalchemy.orm import Session
from app.database.models import Channel, Videos, VideoInsight

def extract_keywords(title, description):
    # Dummy implementation for keyword extraction
    keywords = title.split() + description.split()
    return ", ".join(keywords[:5])  # Just returning the first 5 words as keywords

def calculate_engagement(view_count, like_count, comment_count):
    return (like_count + comment_count) / view_count if view_count else 0

def calculate_view_trends(videos):
    df = pd.DataFrame([{
        'published_at': video.published_at,
        'view_count': video.view_count
    } for video in videos])

    df['published_at'] = pd.to_datetime(df['published_at'])
    df.set_index('published_at', inplace=True)

    weekly_view_trends = df['view_count'].resample('W').sum()
    return weekly_view_trends

def calculate_keyword_trends(insights):
    keyword_over_time = defaultdict(list)

    for insight in insights:
        keywords = insight.top_keywords.split(', ')
        date = insight.created_at.date()  # Assuming created_at is a datetime field
        for keyword in keywords:
            keyword_over_time[keyword].append(date)

    keyword_trends = {k: pd.Series(v).value_counts().sort_index() for k, v in keyword_over_time.items()}
    return keyword_trends

def insert_channel(db: Session, channel_id: str, channel_title: str, youtube_video_response):
    if not db.query(Channel).filter_by(channel_id=channel_id).first():
        channel = Channel(
            channel_id=channel_id,
            channel_title=channel_title,
            subscriber_count=youtube_video_response.pageInfo.totalResults,
            video_count=len(youtube_video_response.items),
            view_count=sum(int(video.statistics.viewCount) for video in youtube_video_response.items),
            created_at=datetime.utcnow()
        )
        db.add(channel)
        db.commit()

def insert_video(db: Session, video_id: str, channel_id: str, title: str, description: str, published_at: datetime, view_count: int, like_count: int, comment_count: int):
    if not db.query(Videos).filter_by(video_id=video_id).first():
        video = Videos(
            video_id=video_id,
            channel_id=channel_id,
            title=title,
            description=description,
            published_at=published_at,
            view_count=view_count,
            like_count=like_count,
            comment_count=comment_count,
        )
        db.add(video)
        db.commit()

def insert_video_insight(db: Session, video_id: str, top_keywords: str, engagement_score: float):
    if not db.query(VideoInsight).filter_by(video_id=video_id).first():
        insight = VideoInsight(
            video_id=video_id, top_keywords=top_keywords, engagement_score=engagement_score
        )
        db.add(insight)
        db.commit()
