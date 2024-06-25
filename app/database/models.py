# app/database/models.py

from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db_setup import Base
from datetime import datetime

class Channel(Base):
    __tablename__ = 'channels'
    channel_id = Column(String, primary_key=True, index=True)
    channel_title = Column(String, nullable=False)
    subscriber_count = Column(Integer, nullable=False, default=0)
    video_count = Column(Integer, nullable=False, default=0)
    view_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class Videos(Base):
    __tablename__ = 'videos'
    video_id = Column(String, primary_key=True, index=True)
    channel_id = Column(String, ForeignKey('channels.channel_id'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    published_at = Column(DateTime, nullable=False)
    view_count = Column(Integer, nullable=False)
    like_count = Column(Integer, nullable=True)
    comment_count = Column(Integer, nullable=True)
    channel = relationship("Channel", back_populates="videos")

class VideoInsight(Base):
    __tablename__ = 'video_insights'
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, ForeignKey('videos.video_id'), nullable=False)
    top_keywords = Column(String, nullable=False)
    engagement_score = Column(Float, nullable=False)
    video = relationship("Videos", back_populates="insights")
    created_at = Column(DateTime, default=datetime.utcnow)

Channel.videos = relationship("Videos", order_by=Videos.video_id, back_populates="channel")
Videos.insights = relationship("VideoInsight", order_by=VideoInsight.id, back_populates="video")
