# main.py

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.api.insights import calculate_view_trends, calculate_keyword_trends
from app.database.db_setup import SessionLocal, init_db
from app.database.models import Channel, Videos, VideoInsight

init_db()

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/channels/")
def read_channels(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    channels = db.query(Channel).offset(skip).limit(limit).all()
    return channels

@app.get("/videos/")
def read_videos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    videos = db.query(Videos).offset(skip).limit(limit).all()
    return videos

@app.get("/insights/")
def read_insights(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    insights = db.query(VideoInsight).offset(skip).limit(limit).all()
    return insights

@app.get("/channels/{channel_id}/videos/")
def get_channel_videos(channel_id: str, db: Session = Depends(get_db)):
    videos = db.query(Videos).filter_by(channel_id=channel_id).all()
    return videos

@app.get("/videos/{video_id}/insights/")
def get_video_insights(video_id: str, db: Session = Depends(get_db)):
    insights = db.query(VideoInsight).filter_by(video_id=video_id).first()
    if insights is None:
        return {"error": "Insights not found"}
    return insights

@app.get("/channels/{channel_id}/insights")
def get_channel_insights(channel_id: str, db: Session = Depends(get_db)):
    channel = db.query(Channel).filter_by(channel_id=channel_id).first()
    if channel:
        return {
            "channel_id": channel.channel_id,
            "channel_title": channel.channel_title,
            "overall_view_count": channel.view_count,
            "overall_video_count": channel.video_count
        }
    return {"error": "Channel not found"}

@app.get("/view_trends/")
def get_view_trends(db: Session = Depends(get_db)):
    videos = db.query(Videos).all()
    trends = calculate_view_trends(videos)
    return trends.to_dict()

@app.get("/keyword_trends/")
def get_keyword_trends(db: Session = Depends(get_db)):
    insights = db.query(VideoInsight).all()
    trends = calculate_keyword_trends(insights)
    return {k:v.to_dict() for k, v in trends.items()}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
