# YouTube Data Insights

## Overview

This project collects data from the YouTube API, stores it in a PostgreSQL database, and displays insights using a Streamlit app.

## Setup

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd pythonProject
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the PostgreSQL database:
    - Update the database URL in `app/database/db_setup.py`.
        - Run the following to initialize the database:
      ```bash
        CREATE TABLE channels (
        channel_id VARCHAR PRIMARY KEY,
        channel_title VARCHAR NOT NULL,
        subscriber_count INTEGER NOT NULL DEFAULT 0,
        video_count INTEGER NOT NULL DEFAULT 0,
        view_count INTEGER NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
      
        CREATE TABLE videos (
        video_id VARCHAR PRIMARY KEY,
        channel_id VARCHAR NOT NULL,
        title VARCHAR NOT NULL,
        description TEXT NOT NULL,
        published_at TIMESTAMP NOT NULL,
        view_count INTEGER NOT NULL,
        like_count INTEGER,
        comment_count INTEGER,
        FOREIGN KEY (channel_id) REFERENCES channels (channel_id));
      
        CREATE TABLE video_insights (
        id SERIAL PRIMARY KEY,
        video_id VARCHAR NOT NULL,
        top_keywords TEXT NOT NULL,
        engagement_score FLOAT NOT NULL,
        FOREIGN KEY (video_id) REFERENCES videos (video_id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
      ```

5. Update `app/config.py` with your YouTube API key.

6. Run the scheduler to fetch data periodically:
    ```bash
    python app/scheduler/scheduler.py
    ```

7. Start the FastApi app:
    ```bash
    uvicorn main:app --reload
    ```

8. Start the Streamlit app:
    ```bash
    streamlit run streamlit_app.py
    ```

## Usage

- The Streamlit app will display the YouTube data, including trends in views and keywords or you can hit the APIs.
