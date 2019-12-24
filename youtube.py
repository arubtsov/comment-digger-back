import os
import googleapiclient.discovery

from rq.job import get_current_job

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = os.environ['YOUTUBE_DATA_API_KEY']

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)

def format_comment(youtube_comment):
    comment = youtube_comment["snippet"]["topLevelComment"]
    snippet = comment["snippet"]

    formatted = {
        'id': comment['id'],
        'text': snippet["textOriginal"],
        'author': snippet["authorDisplayName"],
        'likeCount': snippet['likeCount'],
        'publishedAt': snippet['publishedAt']
    }

    return formatted

def get_comments_count (videoId):
    request = youtube.videos().list(
        id=videoId,
        part="statistics"
    )
    response = request.execute()

    return int(response['items'][0]['statistics']['commentCount'])

def get_comments_byt_id(id):
    job = get_current_job()
    total_comments = get_comments_count(id)
    comments_loaded = 0
    comments = []

    request_parameters = {
        'videoId': id,
        'part': 'snippet',
        'textFormat': 'plainText',
        'maxResults': 100
    }

    next_page_token = None

    while True:
        response = youtube.commentThreads().list(**request_parameters).execute()

        comments_loaded += response['pageInfo']['resultsPerPage']

        for item in response['items']:
            comments.append(format_comment(item))

        next_page_token = response.get('nextPageToken')

        if (next_page_token is None):
            break
        else:
            request_parameters['pageToken'] = next_page_token
            job.meta['progress'] = round(comments_loaded / total_comments, 2)
            job.save_meta()

    return comments
