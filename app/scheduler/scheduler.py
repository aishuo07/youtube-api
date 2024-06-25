import schedule
import time
from app.api.youtube_api import fetch_youtube_data
from config import CHANNEL_IDS


def job():
    fetch_youtube_data(CHANNEL_IDS)

schedule.every().day.at("10:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
