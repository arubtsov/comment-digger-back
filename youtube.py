import os
import googleapiclient.discovery

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = os.environ['YOUTUBE_DATA_API_KEY']

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)

def get_comments_byt_id(id):
    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=id
    )

    return request.execute()