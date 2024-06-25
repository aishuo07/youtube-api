import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"  # Replace with your API URL

def load_data():
    videos_response = requests.get(f"{API_URL}/videos/")
    insights_response = requests.get(f"{API_URL}/insights/")
    return videos_response.json(), insights_response.json()

def create_dataframe(videos, insights):
    video_data = [
        {
            "Video ID": video['video_id'],
            "Channel ID": video['channel_id'],
            "Title": video['title'],
            "Description": video['description'],
            "Published At": video['published_at'],
            "View Count": video['view_count'],
            "Like Count": video['like_count'],
            "Comment Count": video['comment_count'],
        }
        for video in videos
    ]
    insight_data = [
        {
            "Video ID": insight['video_id'],
            "Top Keywords": insight['top_keywords'],
            "Engagement Score": insight['engagement_score'],
        }
        for insight in insights
    ]
    return pd.DataFrame(video_data), pd.DataFrame(insight_data)

def main():
    st.title("YouTube Data Insights")
    videos, insights = load_data()
    video_df, insight_df = create_dataframe(videos, insights)

    st.header("Videos")
    st.write(video_df)

    st.header("Video Insights")
    st.write(insight_df)

    st.header("View Trends")
    view_trends = requests.get(f"{API_URL}/view_trends/").json()
    st.line_chart(view_trends)

    st.header("Keyword Trends")
    keyword_trends = requests.get(f"{API_URL}/keyword_trends/").json()
    for keyword, trend in keyword_trends.items():
        st.write(keyword)
        st.line_chart(trend)  # Remove `key=keyword`

if __name__ == "__main__":
    main()
